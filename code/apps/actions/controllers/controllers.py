import time
import RPi.GPIO as GPIO
import config_controllers

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def turnon(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

def turnoff(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 1)

def get_all_values_list():
    all_values_list = config_controllers.controllers_list
    print(all_values_list)
    return all_values_list
