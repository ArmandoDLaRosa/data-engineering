import json
import uuid
from datetime import datetime

from flask import Blueprint
from flask_cors import cross_origin
from sqlalchemy.orm import scoped_session, sessionmaker

from ..extensions import db
from ..models.beneficiary import Beneficiary, BeneficiarySchema

app_be = Blueprint('beneficiary', __name__)


@app_be.before_app_first_request
def initialize_database():
    Session = sessionmaker(bind=db.engine)
    app_be.session = scoped_session(Session)

@app_be.after_request
def commit_database(response):
    if response.status_code >= 400:
        app_be.session.rollback()
    else:
        app_be.session.commit()
    return response


@app_be.route('/get_beneficiary/<beneficiary_id>', methods=['GET'])
@cross_origin()
def get_transaction(beneficiary_id):
    beneficiary = Beneficiary.query.get((beneficiary_id))
    return BeneficiarySchema().dump(beneficiary)