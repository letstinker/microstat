from machine import Pin
from time import sleep

#red = Pin(2, Pin.OUT)
green = Pin(2, Pin.OUT)

while True:
  #red.high()
  print('Turning led on')
  green.value(0)

  sleep(1)

  #red.low()
  print('Turning led off')
  green.value(1)
  sleep(1)


