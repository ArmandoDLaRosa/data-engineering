from random import choice, uniform, randint
from datetime import datetime, timedelta
import uuid
import csv

def is_recent(transaction_datetime):
    current_time = datetime.now()
    transaction_time = datetime.strptime(transaction_datetime, '%Y-%m-%d %H:%M:%S.%f')
    fourteen_days_ago = current_time - timedelta(days=14)
    return True if transaction_time > fourteen_days_ago else False

def is_valid(send_amount):
    return False if ((send_amount < 100) or (send_amount > 10000)) else True

# Generate a sample dataset of 100 transactions

with open('transactions.csv', mode='w', newline='') as file:
    # do nothing, just open and immediately close the file to clear its contents
    pass
    cols_name = ['send_amount', 
                 'send_currency', 
                 'transaction_datetime',
                 'is_recent',
                 'is_valid',
                 'is_fraudulent_transaction']
    writer = csv.writer(file)
    writer.writerow(cols_name)

currencies = ['USD', 'MXN', 'EUR']
transactions = []
for i in range(100):
    send_amount = round(uniform(1, 100000), 2)
    send_currency = choice(currencies)
    transaction_datetime = (datetime.now() - timedelta(days=randint(0, 30), hours=randint(0, 23), minutes=randint(0, 59), seconds=randint(0, 59))).strftime('%Y-%m-%d %H:%M:%S.%f') 
    is_recent_attr = is_recent(transaction_datetime)
    is_valid_attr = is_valid(send_amount)
    is_fraudulent_transaction = choice([True, False])

    with open('transactions.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([send_amount,
                         send_currency,
                         transaction_datetime,
                         is_recent_attr,
                         is_valid_attr,
                         is_fraudulent_transaction])
