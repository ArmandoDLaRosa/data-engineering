import json
import uuid
from datetime import datetime

from flask import Blueprint
from flask_cors import cross_origin
from sqlalchemy.orm import scoped_session, sessionmaker

from ..extensions import db
from ..models.consumer import Consumer, ConsumerSchema

app_co = Blueprint('consumer', __name__)


@app_co.before_app_first_request
def initialize_database():
    Session = sessionmaker(bind=db.engine)
    app_co.session = scoped_session(Session)

@app_co.after_request
def commit_database(response):
    if response.status_code >= 400:
        app_co.session.rollback()
    else:
        app_co.session.commit()
    return response


@app_co.route('/get_consumer/<consumer_id>', methods=['GET'])
@cross_origin()
def get_transaction(consumer_id):
    consumer = Consumer.query.get((consumer_id))
    return ConsumerSchema().dump(consumer)