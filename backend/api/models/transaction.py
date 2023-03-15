from collections import OrderedDict
from datetime import datetime, timedelta

import joblib
import numpy as np
import requests
from ..extensions import db, ma
import warnings

CURRENCY_DICT = {'EUR': 0, 'MXN': 1, 'USD': 2}
STD_DEV = np.load('api/ai_model/std_scaler.npy')
MEAN = np.load('api/ai_model/mean_scaler.npy')

class Transaction(db.Model):
    # Each record is an analysis of a robot during match
    __tablename__ = 'transaction'
    # ID    
    transaction_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # ATTRIBUTES    
    consumer_id = db.Column(db.String(50), nullable=False)
    beneficiary_id = db.Column(db.String(50), nullable=False)        
    send_amount = db.Column(db.String(1000), nullable=False) 
    send_currency = db.Column(db.String(1000), nullable=False)
    transaction_datetime = db.Column(db.String(1000), nullable=False) 
    is_recent_transaction = db.Column(db.Boolean, nullable=False)
    is_valid_transaction =  db.Column(db.Boolean, nullable=False)
    is_fraudulent_transaction =  db.Column(db.Boolean, nullable=False)
    # Standard attributes    
    created_at = db.Column(db.DateTime,  default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(db.DateTime,  default=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, nullable=False)  
        
    def is_recent(self):
        current_time = datetime.now()
        transaction_time = datetime.strptime(self.transaction_datetime, '%Y-%m-%d %H:%M:%S.%f')
        fourteen_days_ago = current_time - timedelta(days=14)
        if transaction_time > fourteen_days_ago:
            self.is_recent_transaction = True
        else:
            self.is_recent_transaction = False

    def is_valid(self):
        
        if float(self.send_amount) < 100 or float(self.send_amount) > 10000:
            self.is_valid_transaction = False
        else:
            self.is_valid_transaction = True

    def is_fraudulent(self):
        # Machine learning algorithm
        transaction_time = datetime.strptime(self.transaction_datetime, '%Y-%m-%d %H:%M:%S.%f')

        send_amount = float(self.send_amount)
        if self.send_currency != 'USD':
            # Rates By Exchange Rate API at https://www.exchangerate-api.com
            response = requests.get(
                f'https://api.exchangerate-api.com/v4/latest/USD?base={self.send_currency}&symbols=USD&date={transaction_time.date()}')
            exchange_rate = response.json()['rates']['USD']
            send_amount *= exchange_rate
        data_point = OrderedDict({"usd_amount": ((np.array([[send_amount]])-MEAN)/STD_DEV)[0][0],
                                "send_currency": CURRENCY_DICT[self.send_currency],
                                "is_recent": False,
                                "is_valid": False,
                                "hour": transaction_time.hour,
                                "dayofweek": transaction_time.weekday(),
                                "month": transaction_time.month})

        loaded_model = joblib.load("../backend/api/ai_model/rfc_opt.pkl")
        warnings.filterwarnings('ignore', message='X does not have valid feature names')
        self.is_fraudulent = loaded_model.predict([list(data_point.values())])[0]
        

        
class TransactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaction

    # ID    
    transaction_id = ma.auto_field()
    # ATTRIBUTES    
    consumer_id = ma.auto_field()
    beneficiary_id = ma.auto_field()    
    send_amount = ma.auto_field()
    send_currency = ma.auto_field()
    transaction_datetime = ma.auto_field()
    is_recent_transaction = ma.auto_field()
    is_valid_transaction = ma.auto_field()
    is_fraudulent_transaction = ma.auto_field()
    # Standard attributes    
    created_at = ma.DateTime(format='%Y-%m-%d %H:%M:%S.%f')
    created_by = ma.auto_field()
    updated_at = ma.DateTime(format='%Y-%m-%d %H:%M:%S.%f')
    updated_by = ma.auto_field()
    available = ma.auto_field()
    
