import sys
import time
from machine import Pin
from configstore import ConfigStore
from util import blink_led, clamp, next_item, prev_item


class MicroStat():

    CONFIG_DEFAULTS = {
        'temp_desired': 75.0,
        'temp_sensed': None,
        'temp_mode': 'OFF',
        'menu_mode': 'TEMP'
    }
    CONFIG = {}

    # Temp settings
    TEMP_BUFFER = 1.0
    TEMP_COOLDOWN = 60 # Cooldown in seconds
    TEMP_FILE = './temp.txt'
    TEMP_LOWER_LIMIT = 60.0
    TEMP_UPPER_LIMIT = 80.0

    # AC pins and settings
    SYSTEM_HEAT_PIN = 0
    SYSTEM_COOL_PIN = 0
    SYSTEM_MODES = ['COOL', 'HEAT', 'DUAL', 'OFF']

    # UP Button
    BUTTON_UP = None
    BUTTON_UP_PIN = 14
    BUTTON_UP_LAST_VALUE = 1

    # Down Button
    BUTTON_DOWN = None
    BUTTON_DOWN_PIN = 12
    BUTTON_DOWN_LAST_VALUE = 1

    # Menu Button
    BUTTON_MENU_MODE = None
    BUTTON_MENU_MODE_PIN = 13
    BUTTON_MENU_MODE_LAST_VALUE = 1
    MENU_MODES = ['TEMP', 'SYSTEM']

    def __init__(self):
        self.BUTTON_UP = Pin(self.BUTTON_UP_PIN, Pin.IN, Pin.PULL_UP)
        self.BUTTON_DOWN = Pin(self.BUTTON_DOWN_PIN, Pin.IN, Pin.PULL_UP)
        self.BUTTON_MENU_MODE = Pin(self.BUTTON_MENU_MODE_PIN, Pin.IN, Pin.PULL_UP)
        self.CONFIG = ConfigStore(defaults=self.CONFIG_DEFAULTS)

        # For debugging
        # self.CONFIG.reset()

    '''
                TEMP CODE
    '''
    def increase_desired_temp(self):
        return self.set_desired_temp(self.get_desired_temp()+1)
    def decrease_desired_temp(self):
        return self.set_desired_temp(self.get_desired_temp()-1)
    def set_desired_temp(self, temp):
        self.CONFIG.set('temp_desired', clamp(temp, self.TEMP_UPPER_LIMIT, self.TEMP_LOWER_LIMIT))
        return self.get_desired_temp()
    def get_desired_temp(self):
        return self.CONFIG.get('temp_desired')

    '''
                SYSTEM MODE CODE
    '''
    def set_system_mode(self, mode):
        self.CONFIG.set('temp_mode', mode)
        return self.get_system_mode()
    def get_system_mode(self):
        return self.CONFIG.get('temp_mode')
    def get_system_modes(self):
        return self.SYSTEM_MODES
    def next_system_mode(self):
        next_mode = next_item(self.get_system_mode(), self.get_system_modes())
        return self.set_system_mode(next_mode)
    def prev_system_mode(self):
        prev_mode = prev_item(self.get_system_mode(), self.get_system_modes())
        return self.set_system_mode(prev_mode)

    '''
        CONTROL CODE
    '''
    def get_sensed_temp(self):
        self.TEMP_SENSED = 72
        self.CONFIG.set('temp_sensed', self.TEMP_SENSED)
        return self.TEMP_SENSED

    '''
                MENU MODE CODE
    '''
    def set_menu_mode(self, mode):
        print('Setting menu mode tp', mode)
        self.CONFIG.set('menu_mode', mode)
        return self.get_menu_mode()
    def get_menu_mode(self):
        return self.CONFIG.get('menu_mode')
    def get_menu_modes(self):
        return self.MENU_MODES

    '''
        BUTTON CODE
    '''
    def check_which_buttons_pressed(self):
        UP_VALUE = self.BUTTON_UP.value()
        DOWN_VALUE = self.BUTTON_DOWN.value()
        MENU_MODE_VALUE = self.BUTTON_MENU_MODE.value()
        UP_PRESSED = False
        DOWN_PRESSED = False
        MENU_MODE_PRESSED = False

        if UP_VALUE != self.BUTTON_UP_LAST_VALUE and UP_VALUE == 0:
            UP_PRESSED = True
            self.BUTTON_UP_LAST_VALUE = UP_VALUE
        elif UP_VALUE != self.BUTTON_UP_LAST_VALUE and UP_VALUE == 1:
            self.BUTTON_UP_LAST_VALUE = UP_VALUE

        if DOWN_VALUE != self.BUTTON_DOWN_LAST_VALUE and DOWN_VALUE == 0:
            DOWN_PRESSED = True
            self.BUTTON_DOWN_LAST_VALUE = DOWN_VALUE
        elif DOWN_VALUE != self.BUTTON_DOWN_LAST_VALUE and DOWN_VALUE == 1:
            self.BUTTON_DOWN_LAST_VALUE = DOWN_VALUE

        if MENU_MODE_VALUE != self.BUTTON_MENU_MODE_LAST_VALUE and MENU_MODE_VALUE == 0:
            MENU_MODE_PRESSED = True
            self.BUTTON_MENU_MODE_LAST_VALUE = MENU_MODE_VALUE
        elif MENU_MODE_VALUE != self.BUTTON_MENU_MODE_LAST_VALUE and MENU_MODE_VALUE == 1:
            self.BUTTON_MENU_MODE_LAST_VALUE = MENU_MODE_VALUE

        if UP_PRESSED and not DOWN_PRESSED and not MENU_MODE_PRESSED:
            return 'UP'
        elif not UP_PRESSED and DOWN_PRESSED and not MENU_MODE_PRESSED:
            return 'DOWN'
        elif not UP_PRESSED and not DOWN_PRESSED and MENU_MODE_PRESSED:
            return 'MENU_MODE'
        else:
            return None

    def handle_temp_mode_loop(self, button):
        if button == 'UP':
            cur_desired_temp = self.increase_desired_temp()
            blink_led()
            print('New desired temp: {}'.format(cur_desired_temp))
        if button == 'DOWN':
            cur_desired_temp = self.decrease_desired_temp()
            blink_led()
            print('New desired temp: {}'.format(cur_desired_temp))

    def handle_system_mode_loop(self, button):
        if button == 'UP':
            cur_desired_mode = self.next_system_mode()
            blink_led()
            print('New system mode: {}'.format(cur_desired_mode))
        if button == 'DOWN':
            cur_desired_mode = self.prev_system_mode()
            blink_led()
            print('New system mode: {}'.format(cur_desired_mode))


    def action_check(self):
        self.CONFIG.check_save()

        button = self.check_which_buttons_pressed()
        mode = self.get_menu_mode()

        if button and button == 'MENU_MODE':
            mode = self.set_menu_mode(next_item(mode, self.get_menu_modes()))
            print('Changing menu mode to ({})'.format(mode))
        elif button and mode == 'TEMP':
            self.handle_temp_mode_loop(button)
        elif button and mode == 'SYSTEM':
            self.handle_system_mode_loop(button)

if __name__ == "__main__":

    ms = MicroStat()
    
    print('Menu Mode: {}'.format(ms.get_menu_mode()))
    print('Desired temperature: {}'.format(ms.get_desired_temp()))
    print('System Mode: {}'.format(ms.get_system_mode()))

    while True:
        ms.action_check()
        time.sleep(0.01)