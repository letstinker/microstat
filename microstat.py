import sys
import time
from machine import Pin
from configstore import ConfigStore
from buttonmanager import ButtonManager
from tempreader import TempReader, Temperature
from displaymanager import DisplayManager
from menumanager import MenuManager
from systemmanager import SystemManager
from util import blink_led, clamp, next_item, prev_item

class MicroStat():

    CONFIG_DEFAULTS = {
        'temp_desired': 75.0,
        'temp_mode': 'OFF',
        'fan_mode': 'AUTO',
        'menu_mode': 'TEMP'
    }
    CONFIG = {}

    BUTTONS = [
        {
            'name': 'UP',
            'pin': 14
        },
        {
            'name': 'DOWN',
            'pin': 12
        },
        {
            'name': 'MENU_MODE',
            'pin': 13
        },
    ]

    # Temp settings
    TEMP_BUFFER = 1.0
    TEMP_COOLDOWN = 60 # Cooldown in seconds
    TEMP_HUMID_ACTIVATE = 80
    TEMP_LOWER_LIMIT = 60.0
    TEMP_UPPER_LIMIT = 80.0
    TEMP_SYSTEM_MEASUREMENT = 'fahrenheit'
    
    # AC pins and settings
    SYSTEM_HEAT_PIN = 16
    SYSTEM_COOL_PIN = 15
    SYSTEM_FAN_PIN = 4
    SYSTEM_MODES = ['COOL', 'HEAT', 'OFF']
    SYSTEM_FAN_MODES = ['AUTO', 'ON']

    MENUS = {}

    def __init__(self):
        self.CONFIG = ConfigStore(defaults=self.CONFIG_DEFAULTS)
        self.bm = ButtonManager(buttons=self.BUTTONS)
        self.tr = TempReader(system=self.TEMP_SYSTEM_MEASUREMENT)
        self.dm = DisplayManager()
        self.sm = SystemManager(self.SYSTEM_HEAT_PIN, self.SYSTEM_COOL_PIN, self.SYSTEM_FAN_PIN)

        self.MENUS = {
            'TEMP': {
                'name' : 'TEMP',
                'method': self.handle_temp_mode_loop
            },
            'SYSTEM': {
                'name' : 'SYSTEM',
                'method': self.handle_system_mode_loop
            },
            'SYSTEM_FAN': {
                'name' : 'SYSTEM_FAN',
                'method': self.handle_system_fan_mode_loop
            }
        }

        self.mm = MenuManager(self.MENUS)
        self.mm.select(self.get_menu_mode())
        # For debugging
        # self.CONFIG.reset()

    #
    # TEMP CODE
    #
    def increase_desired_temp(self):
        return self.set_desired_temp(self.get_desired_temp()+1)
    def decrease_desired_temp(self):
        return self.set_desired_temp(self.get_desired_temp()-1)
    def set_desired_temp(self, temp):
        self.CONFIG.set('temp_desired', clamp(temp, self.TEMP_UPPER_LIMIT, self.TEMP_LOWER_LIMIT))
        return self.get_desired_temp()
    def get_desired_temp(self):
        return self.CONFIG.get('temp_desired')

    #
    # SYSTEM MODE CODE
    #
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

    #
    # SYSTEM FAN MODE CODE
    #
    def set_system_fan_mode(self, mode):
        self.CONFIG.set('fan_mode', mode)
        return self.get_system_fan_mode()
    def get_system_fan_mode(self):
        return self.CONFIG.get('fan_mode')
    def get_system_fan_modes(self):
        return self.SYSTEM_FAN_MODES
    def next_system_fan_mode(self):
        next_mode = next_item(self.get_system_fan_mode(), self.get_system_fan_modes())
        return self.set_system_fan_mode(next_mode)
    def prev_system_fan_mode(self):
        prev_mode = prev_item(self.get_system_fan_mode(), self.get_system_fan_modes())
        return self.set_system_fan_mode(prev_mode)

    #
    # MENU MODE CODE
    #
    def set_menu_mode(self, mode):
        print('Setting menu mode tp', mode)
        self.CONFIG.set('menu_mode', mode)
        return self.get_menu_mode()
    def get_menu_mode(self):
        return self.CONFIG.get('menu_mode')
    def get_menu_modes(self):
        return list(self.MENUS)

    #
    # Loop handlers
    #
    def handle_temp_mode_loop(self, menu_name, button):
        if button:
            if button == 'UP':
                cur_desired_temp = self.increase_desired_temp()
                blink_led()
                print('New desired temp: {}'.format(cur_desired_temp))
            if button == 'DOWN':
                cur_desired_temp = self.decrease_desired_temp()
                blink_led()
                print('New desired temp: {}'.format(cur_desired_temp))
        else:
            temp = self.tr.temperture()
            symbol = self.tr.current_temp.symbol()
            humid = self.tr.humidity()

            rows = [
                'Temp: {}{}'.format(round(temp), symbol),
                'Humidity: {}'.format(humid),
                'Mode: {}'.format(self.get_system_mode()),
                'Desired Temp: {}{}'.format(self.get_desired_temp(), symbol)
            ]
            self.dm.display_rows(rows)

    def handle_system_mode_loop(self, menu_name, button):

        if button:
            if button == 'UP':
                cur_desired_mode = self.next_system_mode()
                blink_led()
                print('New system mode: {}'.format(cur_desired_mode))
            if button == 'DOWN':
                cur_desired_mode = self.prev_system_mode()
                blink_led()
                print('New system mode: {}'.format(cur_desired_mode))
        else:
            self.dm.display_selection(self.get_system_mode(), self.SYSTEM_MODES, 'Mode:')

    def handle_system_fan_mode_loop(self, menu_name, button):
        if button:
            if button == 'UP':
                cur_desired_fan_mode = self.next_system_fan_mode()
                blink_led()
                print('New system fan mode: {}'.format(cur_desired_fan_mode))
            if button == 'DOWN':
                cur_desired_fan_mode = self.prev_system_fan_mode()
                blink_led()
                print('New system fan mode: {}'.format(cur_desired_fan_mode))
        else:
            self.dm.display_selection(self.get_system_fan_mode(), self.SYSTEM_FAN_MODES, 'Fan:')

    def system_status(self):
        system_mode = self.get_system_mode()

        if system_mode == 'OFF':
            self.sm.cool_off()
            self.sm.heat_off()
            self.sm.fan_off()

        system_fan_mode = self.get_system_fan_mode()
        desired_temp = self.get_desired_temp()
        cur_temp = self.tr.temperture()

        # Check if its hot enough to turn the cool on
        if system_mode == 'COOL' and (cur_temp - desired_temp) >= self.TEMP_BUFFER:
            self.sm.cool_on()
        
        #  Check if its cool enough to turn the cool off
        if system_mode == 'COOL' and (desired_temp - cur_temp) >= self.TEMP_BUFFER:
            self.sm.cool_off()
            # If the fan is on auto lets turn it off too if it will let us
            if system_fan_mode == 'AUTO':
                self.sm.fan_off()

        # Check if its cold enough to turn the heat on
        if system_mode == 'HEAT' and (desired_temp - cur_temp) >= self.TEMP_BUFFER:
            self.sm.heat_on()
        
        #  Check if its hot enough to turn the heat off
        if system_mode == 'HEAT' and (cur_temp - desired_temp) >= self.TEMP_BUFFER:
            self.sm.heat_off()
            # If the fan is on auto lets turn it off too if it will let us
            if system_fan_mode == 'AUTO':
                self.sm.fan_off()
        
        # If the fan is set to ON then we should keep it always on
        if system_fan_mode == 'ON' or self.tr.humidity() > self.TEMP_HUMID_ACTIVATE:
            self.sm.fan_on()

    #
    # Main action handler
    #
    def action_check(self):

        button = self.bm.check_button_pressed()
        mode = self.get_menu_mode()

        if button and button == 'MENU_MODE':
            mode = self.set_menu_mode(next_item(mode, self.get_menu_modes()))
            self.mm.select(mode)
            print('Changing menu mode to ({})'.format(mode))
        else:
            self.mm.handle(button=button)

    def loop(self):
        self.CONFIG.check_save()

        # Always try to update temp
        self.tr.measure()

        # See if something needs to be changed with the system
        self.system_status()

        self.action_check()


#
# This is only ran when the script is ran directly and is for testing purposes.
#
if __name__ == "__main__":

    ms = MicroStat()
    
    print('Menu Mode: {}'.format(ms.get_menu_mode()))
    print('Desired temperature: {}'.format(ms.get_desired_temp()))
    print('System Mode: {}'.format(ms.get_system_mode()))
    print('System Fan Mode: {}'.format(ms.get_system_fan_mode()))

    while True:
        ms.loop()
        time.sleep(0.01)