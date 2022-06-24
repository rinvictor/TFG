from pymongo import MongoClient
import pandas as pd
import db_credentials
import os

def data_backup(col):
    path = os.path.abspath(os.getcwd())
    client = MongoClient(db_credentials.url, db_credentials.port)
    db = client["greenhouseDB"]
    collection = db[col]
    results = collection.find({})
    df = pd.DataFrame(list(results))
    df.to_csv(path + '/' + col +'_backup.csv')


if __name__ == '__main__':
    data_backup('sensors_data')
    data_backup('controllers_data')
