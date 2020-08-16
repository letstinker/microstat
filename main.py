# All commented out for now while testing via test_run.py
import time
from microstat import MicroStat

ms = MicroStat()

print('Menu Mode: {}'.format(ms.get_menu_mode()))
print('Desired temperature: {}'.format(ms.get_desired_temp()))
print('System Mode: {}'.format(ms.get_system_mode()))
print('System Fan Mode: {}'.format(ms.get_system_fan_mode()))

while True:
    ms.loop()
    time.sleep(0.01)