import json
import uuid
from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_cors import cross_origin

from ..extensions import db
from ..models.transaction import Transaction, TransactionSchema
from ..models.beneficiary import Beneficiary
from ..models.consumer import Consumer

import csv

app_tr = Blueprint('transaction', __name__)

@app_tr.before_app_first_request
def initialize_database():
    Session = sessionmaker(bind=db.engine)
    app_tr.session = scoped_session(Session)

@app_tr.after_request
def commit_database(response):
    if response.status_code >= 400:
        app_tr.session.rollback()
    else:
        app_tr.session.commit()
    return response

@app_tr.route('/put_transaction', methods=['POST'])
@cross_origin()
def create_transaction():
    try:
        body =  request.json
        timestamp = datetime.utcnow()
        beneficiary_response = app_tr.session.query(Beneficiary).get(body["beneficiary_id"])
        if not beneficiary_response:
            beneficiary = Beneficiary(beneficiary_id = body["beneficiary_id"],
                                      beneficiary_first_name = body["beneficiary_first_name"],
                                      beneficiary_last_name = body["beneficiary_last_name"],
                                      created_at = timestamp,
                                      created_by = "system",
                                      updated_at = timestamp,
                                      updated_by = "system",
                                      available = True)
            app_tr.session.add(beneficiary)
        consumer_response = app_tr.session.query(Consumer).get(body["consumer_id"])            
        if not consumer_response:     
            consumer = Consumer(consumer_id = body["consumer_id"],
                                consumer_first_name = body["consumer_first_name"],
                                consumer_last_name = body["consumer_last_name"],
                                created_at = timestamp,
                                created_by = "system",
                                updated_at = timestamp,
                                updated_by = "system",
                                available = True)
            app_tr.session.add(consumer)    
        transaction = Transaction(transaction_id = body["transaction_id"],
                                  consumer_id =body["consumer_id"], 
                                  beneficiary_id = body["beneficiary_id"], 
                                  send_amount = body["send_amount"],
                                  send_currency = body["send_currency"],
                                  transaction_datetime = body["transaction_datetime"],
                                  is_recent_transaction = False,
                                  is_valid_transaction = False,
                                  is_fraudulent_transaction = False,
                                  created_at = timestamp, 
                                  created_by = "system", 
                                  updated_at = timestamp, 
                                  updated_by = "system", 
                                  available = True)
        
        transaction.is_recent()
        transaction.is_valid()
        transaction.is_fraudulent()
        
        app_tr.session.add(transaction)
        app_tr.session.commit()
        tr_dict = TransactionSchema().dump(transaction)
        with open('api/data/transactions.csv', mode='a', newline='') as csvfile:
            fieldnames = ['transaction_id', 
                          'consumer_id', 
                          'beneficiary_id', 
                          'send_amount', 
                          'send_currency', 
                          'transaction_datetime',
                          'is_recent_transaction',
                          'is_valid_transaction',
                          'is_fraudulent_transaction']
            
            writer = csv.DictWriter(csvfile, fieldnames= fieldnames )
            if csvfile.tell() == 0:
              writer.writeheader()
            writer.writerow({col:tr_dict[col] for col in fieldnames})
        return tr_dict
    except SQLAlchemyError as e:
        app_tr.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        app_tr.session.close()

@app_tr.route('/get_transaction/<transaction_id>', methods=['GET'])
@cross_origin()
def get_transaction(transaction_id):
    transaction = Transaction.query.get((transaction_id))
    return TransactionSchema().dump(transaction)