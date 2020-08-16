import time
import dht
from machine import Pin


class Temperature():
    current_temp = 0 # Store in Celsius
    system = 'celsius'

    def __init__(self, system='celsius'):
        self.system = system

    def temp(self):
        if self.system == 'fahrenheit':
            return self.fahrenheit()
        return self.celsius()

    def fahrenheit(self, f=None):
        if f:
            self.current_temp = (f - 32) * (5/9)
        return (self.current_temp * (9/5)) + 32
    def symbol(self):
        if self.system == 'fahrenheit':
            return 'F'
        return 'C'

    def celsius(self, c=None):
        if c:
            self.current_temp = c
        return self.current_temp

class TempReader():
    current_temp = None
    sensor = None
    last_measure = 0
    system = 'celsius'
    measure_interval = 10

    def __init__(self, system='celsius', pin=27):
        self.sensor = dht.DHT11(Pin(pin))
        self.system = system
        self.current_temp = Temperature(system=system)
    def symbol(self):
        return self.current_temp.symbol()
    def measure(self):
        if (time.time() - self.last_measure) > self.measure_interval:
            self.last_measure = time.time()
            self.sensor.measure()
    def temperture(self):
        t = self.sensor.temperature()
        self.current_temp.celsius(t)
        return self.current_temp.temp()
    def humidity(self):
        return self.sensor.humidity()
#
# This is only ran when the script is ran directly and is for testing purposes.
#
if __name__ == "__main__":
    tr = TempReader(system='celsius')

    while True:
        print('Measuring...')
        tr.measure()
        temp = tr.temperture()
        symbol = tr.symbol()
        hum = tr.humidity()
        print('Temperature: {}{}'.format(round(temp), symbol))
        print('Humidity: {}%'.format(hum))
        time.sleep(.2)
