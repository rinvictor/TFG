import pymongo
from pymongo import MongoClient
import db_credentials
import pandas as pd
import datetime

client = MongoClient(db_credentials.url, db_credentials.port)
db = client["greenhouseDB"]
collection = db['sensors_data']

# results = collection.find().sort([("_id", pymongo.ASCENDING)]).limit(8)
results = collection.find({'type':'ground humidity'}, sort=[("_id", -1)]).limit(2)


def getdataframe(sensor_type):
    client=MongoClient(db_credentials.url, db_credentials.port)
    db=client["greenhouseDB"]
    collection=db['sensors_data']
    results=collection.find({'type': sensor_type})
    df = pd.DataFrame(list(results))
    return df


if __name__ == '__main__':
    for r in results:
        print(r)
    # df = getdataframe("ambient temperature")
    # today = datetime.date.today()
    # tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    # #value = df.loc[(df['date'] >= str(today)) & (df['date'] <= str(tomorrow))]
    # df = df.loc[(df['date'] >= "2022-03-25") & (df['date'] <= "2022-03-26")]
    # print(df)

    # now = str(datetime.datetime.now())
    # today = now.split()[0]
    # tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    # print(tomorrow)