from controllers.controllers import turnon, turnoff
import db_credentials
from time import sleep
from pymongo import MongoClient
import config
import sensors
from datetime import datetime
from controllers import config_controllers
import telepot
from telepot.loop import MessageLoop

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
    collection = db['controllers_data']
except Exception as e:
    sys.exit(1)


def upload_irrigation_data(controller, liters):
    now = datetime.now()
    item = {"type": "irrigation", "value": liters, "controllerID": controller.pin,"date": now}
    collection.insert_one(item)


def irrigation():
    chat_id = '5046790101'
    controller = config_controllers.bomb
    ground_humidity = sensors.get_ground_hum_list()
    mean_hygro = (ground_humidity[0].get('value') + ground_humidity[1].get('value')) / 2
    if abs(ground_humidity[0].get('value') - ground_humidity[1].get('value')) > 0.1:
        msg = "Warning: Data collected between humidity sensors might be wrong. Sensor: " + str(ground_humidity[0].get('sensor')) +"->"+ str(ground_humidity[0].get('value')) + ", Sensor: " + str(ground_humidity[1].get('sensor')) + "->" + str(ground_humidity[0].get('value'))
        bot.sendMessage(chat_id, msg)

    if mean_hygro > 0.1:
        irrigation_time=(mean_hygro*60)*10
        liters=round(((irrigation_time/60)*controller.data)*1.5 ,1)
        msg="Irrigation in bomb " + str(controller.pin) + " activated. " + str(liters) + " liters used."
        bot.sendMessage(chat_id, msg)
        turnon(controller.pin)
        #sleep(irrigation_time/2)
        sleep(30)
        turnoff(controller.pin)
    upload_irrigation_data(controller, liters)



if __name__ == '__main__':
    irrigation()
