from collections import OrderedDict
from datetime import datetime

import joblib
# import pickle
import numpy as np
import requests

CURRENCY_DICT = {'EUR': 0, 'MXN': 1, 'USD': 2}
STD_DEV = np.load('../backend/api/ai_model/std_scaler.npy')
MEAN = np.load('../backend/api/ai_model/mean_scaler.npy')

date = datetime.strptime("2023-02-15 17:30:39.138799", '%Y-%m-%d %H:%M:%S.%f')
send_amount = float("21014.393400")
currency = 'EUR'
if currency != 'USD':
    # Rates By Exchange Rate API at https://www.exchangerate-api.com
    response = requests.get(
        f'https://api.exchangerate-api.com/v4/latest/USD?base={currency}&symbols=USD&date={date.date()}')
    exchange_rate = response.json()['rates']['USD']


data_point = OrderedDict({"usd_amount": ((np.array([[send_amount * exchange_rate]])-MEAN)/STD_DEV)[0][0],
                          "send_currency": CURRENCY_DICT[currency],
                          "is_recent": False,
                          "is_valid": False,
                          "hour": date.hour,
                          "dayofweek": date.weekday(),
                          "month": date.month})

# with open('../backend/api/ai_model/rfc_opt.pkl', 'rb') as f:
#   loaded_model = pickle.load(f)
loaded_model = joblib.load("../backend/api/ai_model/rfc_opt.pkl")
y_pred = loaded_model.predict([list(data_point.values())])
print(y_pred)
