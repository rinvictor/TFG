import Adafruit_DHT as dht

def read_ambient_humidity(iddht):
    hum_sensor, temp_sensor = dht.read_retry(dht.DHT22, iddht)
    print("Ambient humidity", iddht, hum_sensor)
    print("Ambient temperature", iddht, temp_sensor)

read_ambient_humidity(27)
read_ambient_humidity(22)
