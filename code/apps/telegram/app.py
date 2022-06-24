#!/usr/bin/env python3

import telepot
import telepot.namedtuple
from telepot.loop import MessageLoop
import time
import sensors
import config_controllers
from pymongo import MongoClient
import db_credentials
import pandas as pd
import create_figures as figures
from datetime import datetime, timedelta
import dash_utils as du
import os

f = open('token.txt')
TOKEN = f.read()
TOKEN = TOKEN.strip()
bot = telepot.Bot(TOKEN)


def get_title(s):
    if s == "ground_hum" or s == "ground humidity":
        return "Ground humidity"
    if s == "amb_temp" or s == "ambient temperature":
        return "Ambient temperature"
    if s == "amb_hum" or s == "ambient humidity":
        return "Ambient humidity"
    if s == "ground_temp" or s == "ground temperature":
        return "Ground temperature"
    if s == "irrigation":
        return "Irrigation data"
    else:
        return ""


def get_last_read(type):
    client = MongoClient(db_credentials.url, db_credentials.port)
    db = client["greenhouseDB"]
    if type == 'irrigation':
        collection = db['controllers_data']
        results = collection.find({'type': type}, sort=[("_id", -1)]).limit(1)
    else:
        collection = db['sensors_data']
        results = collection.find({'type': type}, sort=[("_id", -1)]).limit(2)

    list = []
    for r in results:
        list.append(r)
    return list


def format_response_real_time(list):
    response = "Your data:\n"
    response = response + get_title(list[0].get('type')) + '\n'
    for i in range(0, len(list)):
        response = response + "Sensor: " + str(list[i].get('sensor')) + ", value: " + str(
            round(list[i].get('value'), 2)) + ", location: " + str(list[i].get('location')) + '\n'
    return response


def format_response_database(list, type=None):
    response = ""
    response = response + get_title(list[0].get('type')) + '\n' + "Last read: " + str(
        list[0].get('date').strftime("%d-%m-%y %H:%M")) + '\n'
    for i in range(0, len(list)):
        if type == "irrigation":
            response = response + "Controller: " + str(list[i].get('controllerID')) + ", value: " + str(
                round(list[i].get('value'), 2)) + '\n'
        else:
            response = response + "Sensor: " + str(list[i].get('sensorID')) + ", value: " + str(
                round(list[i].get('value'), 2)) + ", location: " + str(list[i].get('location')) + '\n'
    return response


def format_response_figure(list, type=None):
    if type == "irrigation":
        response = get_controllers_info()
        return response

    response = ""
    for i in range(0, len(list)):
        response = response + "Sensor: " + str(list[i].get('sensor')) + ", location: " + str(
            list[i].get('location')) + '\n'
    return response


def getdataframe(type):
    client = MongoClient(db_credentials.url, db_credentials.port)
    db = client["greenhouseDB"]

    if type == "irrigation":
        collection = db['controllers_data']
    else:
        collection = db['sensors_data']

    results = collection.find({'type': type})
    df = pd.DataFrame(list(results))
    return df


def send_photo(type, chat_id, startdate=None, enddate=None):
    try:
        title = get_title(type) + " figure"
        print(title)
        df = getdataframe(type)

        if startdate is None:
            startdate = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        if enddate is None:
            enddate = datetime.strftime(datetime.now(), '%Y-%m-%d')

        df = du.date_filter(df, start_date=startdate, end_date=enddate)

        if type == "ground humidity" or type == "ambient humidity":
            figure = figures.create_humidity_fig_telegram(df, title)
        elif type == "ground temperature" or type == "ambient temperature":
            figure = figures.create_temperature_fig_telegram(df, title)
        elif type == "irrigation":
            print("irrigation")
            figure = figures.create_irrigation_data_fig_telegram(df, title)
        else:
            figure = ""
        b = figure.to_image(format="png", engine="kaleido")
        with open("./image.png", "wb") as f:
            f.write(b)
        bot.sendPhoto(chat_id, photo=open("./image.png", "rb"))
        os.remove("./image.png")
    except:
        bot.sendMessage(chat_id, "CRITICAL: Something failed during execution. [send_photo]")


def get_sensors_info():
    list = sensors.get_all_values_list(value=False)
    response = ""
    for l in list:
        response = response + get_title(l[0].get('type')) + ":" + '\n'
        for i in (0, 1):
            response = response + "Sensor: " + str(l[i].get('sensor')) + ", location: " + str(
                l[i].get('location')) + '\n'
    return response


def get_controllers_info():
    c_list = config_controllers.controllers_list
    response = ""
    response = response + get_title('irrigation') + ":" + '\n'
    for c in c_list:
        response = response + "Controller: " + str(c.pin) + ", liters/min: " + str(c.data)
    return response


def validate_date(date):
    format = "%Y-%m-%d"
    try:
        datetime.strptime(date, format)
        return 0
    except ValueError:
        return 1
    except Exception:
        return 2


def check_options(text, chat_id):
    wrong_date_format_msg = "Date format must be yyyy-mm-dd. Wrong format at: "
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    origin = '2022-02-08'
    if "--startdate" in text:
        startdate = text.split("--startdate")
        startdate = startdate[len(startdate) - 1]
        startdate = startdate.split()[0]
    else:
        startdate = None

    if "--enddate" in text:
        enddate = text.split("--enddate")
        enddate = enddate[len(enddate) - 1]
        enddate = enddate.split()[0]
    else:
        enddate = None

    if startdate is not None:
        if validate_date(startdate) != 0:
            bot.sendMessage(chat_id, wrong_date_format_msg + "--startdate")
            startdate = None
        else:
            if startdate > today:
                bot.sendMessage(chat_id, "Error: startdate must be after today's date. By defect values are set")
                startdate = None

    if enddate is not None:
        if validate_date(enddate) != 0:
            bot.sendMessage(chat_id, wrong_date_format_msg + "--enddate")
            enddate = None
        else:
            if enddate > today:
                bot.sendMessage(chat_id, "Error: enddate must be after today's date. By defect values are set")
                enddate = None

    if startdate is None and enddate is not None:
        startdate = origin
        enddate = enddate

    if startdate is not None and enddate is not None:
        if startdate > enddate or startdate > today or enddate > today:
            bot.sendMessage(chat_id, "Error: enddate must be after startdate. By defect values are set")
            startdate = None
            enddate = None

    return startdate, enddate


def handle(msg):
    wait_msg = "Wait a moment please... We are getting your data from the sensors. This may take a few seconds."
    wait_msg_db = "Wait a moment please... We are getting your data from the database. This may take a few seconds."
    wait_msg_fig = "Wait a moment please... We are building your figure. This may take a few seconds."
    help_msg = "This are all the available commands:\n" + '\n' + "/help - Get info about the commands\n" + "/sensorsinfo - Get info about the sensors" + '\n' + \
               "/controllersinfo - Get info about the controllers\n" + '\n' + \
               "/sensorsdata - Get all current data from sensors" + '\n' + \
               "/groundhumidity - Get current ground humidity" + '\n' + "/groundtemperature - Get current ground temperature" + '\n' + "/ambienthumidity - Get current ambient humidity" + '\n' + \
               "/ambienttemperature - Get current ambient temperature\n" + '\n' + \
               "/sensorsdatadb - Get last read from database" + '\n' + \
               "/groundhumiditydb - Get last ground humidity read from database" + '\n' + "/groundtemperaturedb - Get last ground temperature read from database" + '\n' + \
               "/ambienthumiditydb - Get last ambient humidity read from database" + '\n' + "/ambienttemperaturedb - Get last ambient temperature read from database" + '\n' + \
               "/irrigationdb - Get last irrigation data read from database\n" + '\n' + \
               '/getallfigures [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd] - Get all available figures' + '\n' \
               '/groundhumidityfig [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd] - Get ground humidity figure' + '\n' + \
               '/groundtemperaturefig [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd] - Get ground temperature figure' + '\n' + \
               '/ambienthumidityfig [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd] - Get ambient humidity figure' + '\n' + \
               '/ambienttemperaturefig [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd] - Get ambient temperature figure' + '\n' + \
               '/irrigationfig [--startdate yyy-mm-dd][--enddate yyyy-mm-dd] - Get irrigation data figure'

    chat_id = msg["chat"]["id"]
    text = msg["text"]

    if text == "/help" or text=="/start":
        response = help_msg

    elif text == "/sensorsinfo":
        bot.sendMessage(chat_id, "Building your sensors info message...")
        response = get_sensors_info()

    elif text == "/controllersinfo":
        bot.sendMessage(chat_id, "Building your controllers info message...")
        response = get_controllers_info()

    elif text == "/sensorsdata":
        bot.sendMessage(chat_id, wait_msg)
        list = sensors.get_all_values_list()
        response = "Your data:\n"
        for i in range(0, len(list)):
            response = response + get_title(list[i][0].get('type')) + '\n'
            for j in range(0, len(list[i])):
                response = response + "Sensor: " + str(list[i][j].get('sensor')) + ", value: " + str(
                    round(list[i][j].get('value'), 2)) + ", location: " + str(list[i][j].get('location')) + '\n'
            response = response + '\n'

    elif text == "/groundhumidity":
        bot.sendMessage(chat_id, wait_msg)
        list = sensors.get_ground_hum_list()
        response = format_response_real_time(list)

    elif text == "/groundtemperature":
        bot.sendMessage(chat_id, wait_msg)
        list = sensors.get_ground_temp_list()
        response = format_response_real_time(list)

    elif text == "/ambienthumidity":
        bot.sendMessage(chat_id, wait_msg)
        list = sensors.get_amb_hum_list()
        response = format_response_real_time(list)

    elif text == "/ambienttemperature":
        bot.sendMessage(chat_id, wait_msg)
        list = sensors.get_amb_temp_list()
        response = format_response_real_time(list)

    elif text == "/sensorsdatadb":
        bot.sendMessage(chat_id, wait_msg_db)
        list_gh = get_last_read('ground humidity')
        list_at = get_last_read('ambient temperature')
        list_ah = get_last_read('ambient humidity')
        list_gt = get_last_read('ground temperature')
        response = "Your data:" + '\n' + format_response_database(list_gh) + '\n' + format_response_database(
            list_at) + '\n' + format_response_database(list_ah) + '\n' + format_response_database(list_gt)

    elif text == "/groundhumiditydb":
        bot.sendMessage(chat_id, wait_msg_db)
        list = get_last_read('ground humidity')
        response = "Your data:" + '\n' + format_response_database(list)

    elif text == "/groundtemperaturedb":
        bot.sendMessage(chat_id, wait_msg_db)
        list = get_last_read('ground temperature')
        response = "Your data:" + '\n' + format_response_database(list)

    elif text == "/ambienthumiditydb":
        bot.sendMessage(chat_id, wait_msg_db)
        list = get_last_read('ambient humidity')
        response = "Your data:" + '\n' + format_response_database(list)

    elif text == "/ambienttemperaturedb":
        bot.sendMessage(chat_id, wait_msg_db)
        list = get_last_read('ambient temperature')
        response = "Your data:" + '\n' + format_response_database(list)

    elif text == "/irrigationdb":
        bot.sendMessage(chat_id, wait_msg_db)
        list = get_last_read('irrigation')
        response = "Your data:" + '\n' + format_response_database(list, "irrigation")

    elif text.startswith("/getallfigures"):
        if "--startdate" not in text and "--enddate" not in text and text != "/getallfigures":
            response = "Error in params. Usage: /getallfigures [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd]"
        else:
            startdate, enddate = check_options(text, chat_id)
            bot.sendMessage(chat_id,
                            "Wait a moment please... We are building your all your figures. This may take a few seconds.")
            for type in ["ground humidity", "ground temperature", "ambient humidity", "ambient temperature", "irrigation"]:
                send_photo(type, chat_id, startdate, enddate)
                response = "All figures are already sended!"

    elif text.startswith("/groundhumidityfig"):
        if "--startdate" not in text and "--enddate" not in text and text != "/groundhumidityfig":
            response = "Error in params. Usage: /groundhumidityfig [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd]"
        else:
            startdate, enddate = check_options(text, chat_id)
            bot.sendMessage(chat_id, wait_msg_fig)
            send_photo("ground humidity", chat_id, startdate, enddate)
            gh_list = sensors.get_ground_hum_list(value=False)
            response = "Reminder:\n" + format_response_figure(gh_list)

    elif text.startswith("/groundtemperaturefig"):
        if "--startdate" not in text and "--enddate" not in text and text != "/groundtemperaturefig":
            response = "Error in params. Usage: /groundtemperaturefig [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd]"
        else:
            startdate, enddate = check_options(text, chat_id)
            bot.sendMessage(chat_id, wait_msg_fig)
            send_photo("ground temperature", chat_id, startdate, enddate)
            gt_list = sensors.get_ground_temp_list(value=False)
            response = "Reminder:\n" + format_response_figure(gt_list)

    elif text.startswith("/ambienthumidityfig"):
        if "--startdate" not in text and "--enddate" not in text and text != "/ambienthumidityfig":
            response = "Error in params. Usage: /ambienthumidityfig [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd]"
        else:
            startdate, enddate = check_options(text, chat_id)
            bot.sendMessage(chat_id, wait_msg_fig)
            send_photo("ambient humidity", chat_id, startdate, enddate)
            ah_list = sensors.get_amb_hum_list(value=False)
            response = "Reminder:\n" + format_response_figure(ah_list)

    elif text.startswith("/ambienttemperaturefig"):
        if "--startdate" not in text and "--enddate" not in text and text != "/ambienttemperaturefig":
            response = "Error in params. Usage: /ambienttemperaturefig [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd]"
        else:
            startdate, enddate = check_options(text, chat_id)
            bot.sendMessage(chat_id, wait_msg_fig)
            send_photo("ambient temperature", chat_id, startdate, enddate)
            at_list = sensors.get_amb_temp_list(value=False)
            response = "Reminder:\n" + format_response_figure(at_list)

    elif text.startswith("/irrigationfig"):
        if "--startdate" not in text and "--enddate" not in text and text != "/irrigationfig":
            response = "Error in params. Usage: /irrigationfig [--startdate yyyy-mm-dd][--enddate yyyy-mm-dd]"
        else:
            startdate, enddate = check_options(text, chat_id)
            bot.sendMessage(chat_id, wait_msg_fig)
            send_photo("irrigation", chat_id, startdate, enddate)
            response = "Reminder:\n" + format_response_figure(None, type="irrigation")
    else:
        response = "Oops! That's not a command\n" + help_msg
    try:
        bot.sendMessage(chat_id, response)
    except telepot.exception.TelegramError:
        pass
    return


def main():
    MessageLoop(bot, handle).run_as_thread()
    print("Listening...")

    while 1:
        time.sleep(10)
    return


if __name__ == "__main__":
    main()
