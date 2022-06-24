# Fichero de configuración de sensores

class Sensor:
    def __init__(self, pin, location):
        self.pin = pin
        self.location = location


pin_dht22_1 = Sensor(22, "outdoor")  # GPIO 4 es el pin número 7
pin_dht22_2 = Sensor(27, "indoor")  # GPIO 27 es el pin número 13

# Los higronometros estan conectados al arduino por lo que se corresponden con los pines A0 y A1 de dicha placa
pin_hygro_1 = Sensor(0, "indoor")
pin_hygro_2 = Sensor(1, "indoor")

#ds18b20
ID_ds18b20_1 = Sensor("325a0f1e64ff", "indoor")
ID_ds18b20_2 = Sensor("32360c1e64ff", "indoor")

# Cada vez que se añada un sensor debemos actualizar estas listas
dht_list = [pin_dht22_1, pin_dht22_2]
hygros_list = [pin_hygro_1, pin_hygro_2]
ds18b20_list = [ID_ds18b20_1, ID_ds18b20_2]
