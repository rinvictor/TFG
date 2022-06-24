# Sensors config file

class Sensor:
    def __init__(self, pin, location):
        self.pin = pin
        self.location = location


pin_dht22_1 = Sensor(22, "outdoor")  # GPIO 4 is pin 7
pin_dht22_2 = Sensor(27, "indoor")  # GPIO 27 is pin 13

# Arduino
pin_hygro_1 = Sensor(0, "indoor")
pin_hygro_2 = Sensor(1, "indoor")

#ds18b20
ID_ds18b20_1 = Sensor("325a0f1e64ff", "indoor")
ID_ds18b20_2 = Sensor("32360c1e64ff", "indoor")


dht_list = [pin_dht22_1, pin_dht22_2]
hygros_list = [pin_hygro_1, pin_hygro_2]
ds18b20_list = [ID_ds18b20_1, ID_ds18b20_2]
