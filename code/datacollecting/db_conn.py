import config
import sensors
from datetime import datetime
from pymongo import MongoClient
import db_credentials

nreadingsDHT = 2
nreadingsGH = 3

client = MongoClient(db_credentials.url, db_credentials.port)

db = client["greenhouseDB"]
collection = db['sensors_data']


def insert_ground_hum():
    for h in config.hygros_list:
        ground_humidity = sensors.read_ground_humidity(h.pin)

        if (ground_humidity == -1) or (ground_humidity > 1.0) or (ground_humidity < 0.0):
            print("Ground humidity reading failed in " + str(h.pin) + " sensor")
            ground_humidity = -1

        now = datetime.now()

        item = {"type": "ground humidity", "value": ground_humidity, "sensorID": h.pin, "location": h.location,
                "date": now}
        collection.insert_one(item)
        print(item)


def insert_amb_hum():
    for d in config.dht_list:
        ambient_humidity = sensors.read_ambient_humidity(d.pin)
        if (ambient_humidity == -1) or (ambient_humidity > 100) or (ambient_humidity < 0):
            print("Ambient humidity reading failed in " + str(d.pin) + " sensor")
            ambient_humidity = -1

        now = datetime.now()

        item = {"type": "ambient humidity", "value": ambient_humidity, "sensorID": d.pin, "location": d.location,
                "date": now}
        collection.insert_one(item)
        print(item)


def insert_amb_temp():
    for d in config.dht_list:
        ambient_temperature = sensors.read_ambient_temperature(d.pin)
        if (ambient_temperature == -1) or (ambient_temperature > 70) or (ambient_temperature < -40):
            print("Ambient temperature reading failed in " + str(d.pin) + " sensor")
            ambient_temperature = -1

        now = datetime.now()

        item = {"type": "ambient temperature", "value": ambient_temperature, "sensorID": d.pin, "location": d.location,
                "date": now}
        collection.insert_one(item)
        print(item)


def insert_ground_temp():
    for d in config.ds18b20_list:
        ground_temperature = sensors.read_ground_temperature(d.pin)
        if (ground_temperature == -1) or (ground_temperature < -10) or (ground_temperature > 100):
            print("Ground temperature reading failed in " + str(d.pin) + " sensor")
            ground_temperature = -1

        now = datetime.now()
        item = {"type": "ground temperature", "value": ground_temperature, "sensorID": d.pin, "location": d.location,
                "date": now}
        collection.insert_one(item)
        print(item)


insert_ground_hum()
insert_amb_hum()
insert_amb_temp()
insert_ground_temp()
