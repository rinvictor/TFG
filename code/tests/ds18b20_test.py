import w1thermsensor
import time

'''
while True:
    for sensor in w1thermsensor.get_available_sensors():
        print(sensor.id, sensor.get_temperature())
        time.sleep(1)
'''
for sensor in w1thermsensor.W1ThermSensor.get_available_sensors():
    id = sensor.id
    temp = sensor.get_temperature(id)
    print(temp)

