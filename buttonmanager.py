import time
from machine import Pin


class ButtonManager():
    buttons = []
    def __init__(self, buttons=[]):
        for b in buttons:
            b.update({
                'last_value': 1,
                'data': Pin(b['pin'], Pin.IN, Pin.PULL_UP)
            })
            self.buttons.append(b)

    def check_button_pressed(self):
        for k, b in enumerate(self.buttons):
            v = self.buttons[k]['data'].value()
            if v != self.buttons[k]['last_value'] and v == 0:
                self.buttons[k]['last_value'] = v
                print('{} pressed'.format(self.buttons[k]['name']))
                return self.buttons[k]['name']
            elif v != self.buttons[k]['last_value'] and v == 1:
                print('{} released'.format(self.buttons[k]['name']))
                self.buttons[k]['last_value'] = v
        return None


#
# This is only ran when the script is ran directly and is for testing purposes.
#
if __name__ == "__main__":
    btns = [
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
    bm = ButtonManager(btns)

    while True:
        print('Checking...')
        check = bm.check_button_pressed()
        if check:
            print('Button pressed: {}'.format(check))
        time.sleep(.2)
