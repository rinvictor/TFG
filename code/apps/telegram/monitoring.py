#!/usr/bin/env python3
import telepot
import telepot.namedtuple
from telepot.loop import MessageLoop
from pymongo import MongoClient
import db_credentials
import time
import sys

try:
    f = open('/home/pi/TFG/code/apps/telegram/token.txt')
    TOKEN = f.read()
    TOKEN = TOKEN.strip()
except Exception as e:
    print('Cannot open telegram token file' + e)
    sys.exit(1)

try:
    bot = telepot.Bot(TOKEN)
    client = MongoClient(db_credentials.url, db_credentials.port)
    db = client["greenhouseDB"]
    collection = db['sensors_data']
except Exception as e:
    print('Cannot access to database' + e)
    sys.exit(1)


def handle():
    chat_id = '5046790101'
    for type in ['ground humidity', 'ground temperature', 'ambient humidity', 'ambient temperature']:
        try:
            results = collection.find({'type':type}, sort=[("_id", -1)]).limit(2)
        except Exception as e:
            print('Cannot access to database' + e)
            sys.exit(1)
        for r in results:
            value = r.get('value')
            if str(value) == "-1":
                response = "Error in sensor reading" + '\n'
                response = response + "Sensor "+ str(r.get('sensorID')) + ", type: " + str(r.get('type')) + ", location: " + str(r.get('location')) + ", failed at " + str(r.get('date').strftime("%d-%m-%y %H:%M:%S"))
                bot.sendMessage(chat_id, response)

def main():
    handle()

if __name__ == '__main__':
    main()
