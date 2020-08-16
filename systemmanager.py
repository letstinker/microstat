import time
from machine import Pin

class SystemManager():
    heat_pin = None
    cool_pin = None
    fan_pin = None
    def __init__(self, heat_pin, cool_pin, fan_pin):
        self.heat_pin = Pin(heat_pin, Pin.OUT)
        self.cool_pin = Pin(cool_pin, Pin.OUT)
        self.fan_pin = Pin(fan_pin, Pin.OUT)

    def heat_on(self):
        self.fan_on() # Always turn fan on if heat comes on
        self.heat_pin.value(1)
    def heat_off(self):
        self.heat_pin.value(0)

    def cool_on(self):
        self.fan_on() # Always turn fan on if cool comes on
        self.cool_pin.value(1)
    def cool_off(self):
        self.cool_pin.value(0)

    def fan_on(self):
        self.fan_pin.value(1)
    def fan_off(self):
        # If either heat or cool is on we gotta keep the fan on
        if self.heat_pin.value() == 1 or self.cool_pin.value() == 1:
            return
        self.fan_pin.value(0)


if __name__ == "__main__":
    sm = SystemManager(2, 15, 4)

    # Turn all off
    sm.heat_off()
    time.sleep(.2)
    sm.cool_off()
    time.sleep(.2)
    sm.fan_off()

    time.sleep(2)

    # while True:
    #     sm.heat_on()
    #     time.sleep(.2)
    #     sm.cool_on()
    #     time.sleep(.2)
    #     sm.fan_on()

    #     time.sleep(1)
        
    #     sm.heat_off()
    #     time.sleep(.2)
    #     sm.cool_off()
    #     time.sleep(.2)
    #     sm.fan_off()

    #     time.sleep(1)