import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from util import next_item


class DisplayManager():
    i2c = None
    oled = None
    MAX_ROWS = 4
    MAX_COLS = 16
    CHAR_MULTIPLIER = 8
    LAST_DISPLAYED_SELECTION = {
        'selected': None,
        'choices': [],
        'title': None
    }
    LAST_DISPLAYED_ROWS = []

    def __init__(self, scl=22, sda=21):
        self.i2c = I2C(-1, Pin(scl), Pin(sda))
        self.oled = SSD1306_I2C(128, 32, self.i2c)

    def display_selection(self, selected, choices, title=None):
        # If we get sent the same render ignore
        if self.LAST_DISPLAYED_SELECTION['selected'] == selected and self.LAST_DISPLAYED_SELECTION['choices'] == choices and self.LAST_DISPLAYED_SELECTION['title'] == title:
            return

        self.oled.fill(0)
        col = 0

        # If there is a title display it and set a padding for the rest
        if title:
            self.render_row(title, col, 0)
            col = len(title) + 1

        for c in choices:
            if c == selected:
                choice = c
                self.render_row('>{}'.format(choice), col, 0)
                for cc in range(1, min(self.MAX_ROWS, len(choices))):
                    choice = next_item(choice, choices)
                    self.render_row(' {}'.format(choice), col, cc)

        self.oled.show()

    def display_rows(self, rows):
        if rows == self.LAST_DISPLAYED_ROWS:
            return

        self.oled.fill(0)
        for r in range(0, len(rows)):
            self.render_row(rows[r], 0, r)
        self.oled.show()

    def render_row(self, text, col=0, row=0):
        self.oled.text(text, col*8, row*8)



#
# This is only ran when the script is ran directly and is for testing purposes.
#
if __name__ == "__main__":
    dm = DisplayManager()
    dm.render_selection('COOL', ['HEAT', 'COOL', 'DUAL', 'OFF'], 'Mode:')
    dm.render_selection('COOL', ['HEAT', 'COOL', 'DUAL', 'OFF'], 'Mode:')
    dm.render_selection('COOL', ['HEAT', 'COOL', 'DUAL', 'OFF'], 'Mode:')
    dm.render_selection('COOL', ['HEAT', 'COOL', 'DUAL', 'OFF'], 'Mode:')
    time.sleep(1)
    dm.render_selection('DUAL', ['HEAT', 'COOL', 'DUAL', 'OFF'], 'Mode:')
    time.sleep(1)
    dm.render_selection('OFF', ['HEAT', 'COOL', 'DUAL', 'OFF'], 'Mode:')
    time.sleep(1)
    dm.render_selection('HEAT', ['HEAT', 'COOL', 'DUAL', 'OFF'], 'Mode:')
