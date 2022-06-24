import config
import Adafruit_DHT as dht
from time import sleep
import pyfirmata2
from w1thermsensor import W1ThermSensor, Sensor


def return_value(value):
    print(value)
    if value:
        return value
    else:
        return -1


def read_ambient_humidity(iddht):
    for i in range(3):
        sleep(0.05)
        hum_sensor, temp_sensor = dht.read_retry(dht.DHT22, iddht)
    return return_value(hum_sensor)


def read_ambient_temperature(iddht):
    for i in range(3):
        sleep(0.05)
        hum_sensor, temp_sensor = dht.read_retry(dht.DHT22, iddht)
    return return_value(temp_sensor)


def read_ground_humidity(hygroid):
    try:
        PORT = pyfirmata2.Arduino.AUTODETECT
        board = pyfirmata2.Arduino(PORT)  # salida a la que esta conectado el arduino

        # pin = board.get_pin('a:0:i')
        string = 'a:' + str(hygroid) + ':1'
        pin = board.get_pin(string)

        it = pyfirmata2.util.Iterator(board)
        it.start()

        nmeasures = 0
        while nmeasures < 5:
            analog_value = pin.read()
            hum = analog_value
            sleep(0.1)
            nmeasures += 1

        it.stop()
        board.exit()
    except UserWarning:
        pass
    return return_value(hum)


def read_ground_temperature(ds18b20ID):
    for i in range(2):
        sleep(0.05)
        sensor = W1ThermSensor(Sensor.DS18B20, ds18b20ID)
        temp = sensor.get_temperature()
    return return_value(temp)


def get_amb_hum_list(value=True):
    ambient_humidity_list = []
    for i in config.dht_list:
        if value:
            d = dict(type="amb_hum", sensor=i.pin, location=i.location, value=read_ambient_humidity(i.pin))
        else:
            d = dict(type="amb_hum", sensor=i.pin, location=i.location)
        ambient_humidity_list.append(d)
    return ambient_humidity_list


def get_amb_temp_list(value=True):
    ambient_temperature_list = []
    for i in config.dht_list:
        if value:
            d = dict(type="amb_temp", sensor=i.pin, location=i.location, value=read_ambient_temperature(i.pin))
        else:
            d = dict(type="amb_temp", sensor=i.pin, location=i.location)
        ambient_temperature_list.append(d)
    return ambient_temperature_list


def get_ground_hum_list(value=True):
    ground_humidity_list = []
    for i in config.hygros_list:
        if value:
            d = dict(type="ground_hum", sensor=i.pin, location=i.location, value=read_ground_humidity(i.pin))
        else:
            d = dict(type="ground_hum", sensor=i.pin, location=i.location)
        ground_humidity_list.append(d)
    return ground_humidity_list


def get_ground_temp_list(value=True):
    ground_temperature_list = []
    for i in config.ds18b20_list:
        if value:
            d = dict(type="ground_temp", sensor=i.pin, location=i.location, value=read_ground_temperature(i.pin))
        else:
            d = dict(type="ground_temp", sensor=i.pin, location=i.location)
        ground_temperature_list.append(d)
    return ground_temperature_list


def get_all_values_list(value=True):
    all_values_list = [get_ground_hum_list(value=value), get_amb_temp_list(value=value), get_amb_hum_list(value=value),
                       get_ground_temp_list(value=value)]
    return all_values_list

