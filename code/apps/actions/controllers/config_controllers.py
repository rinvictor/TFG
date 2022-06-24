# Config controllers file
class Controller:
    def __init__(self, pin, data):
        self.pin = pin
        self.data = data # In the bomb case, liters per minute

bomb = Controller(24, 4)

controllers_list = [bomb]
