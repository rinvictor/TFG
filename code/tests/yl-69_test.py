import pyfirmata2
from time import sleep

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
    return hum

print(read_ground_humidity(0))
print(read_ground_humidity(1))
#print(read_ground_humidity(2))
#print(read_ground_humidity(3))
#print(read_ground_humidity(4))
#print(read_ground_humidity(5))
