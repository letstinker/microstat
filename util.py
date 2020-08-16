import time
from machine import Pin


def blink_led():
    pin = Pin(2, Pin.OUT)
    pin.value(0)
    time.sleep(.1)
    pin.value(1)
    pass

def clamp(val, max_value, min_value):
    return max(min(val, max_value), min_value)

def next_item(cur_item, item_list):
    for k,i in enumerate(item_list):
        if i == cur_item:
            if (k+1) > (len(item_list)-1):
                return item_list[0]
            else:
                return item_list[k+1]
    return None

def prev_item(cur_item, item_list):
    for k,i in enumerate(item_list):
        if i == cur_item:
            if (k-1) < 0:
                return item_list[len(item_list)-1]
            else:
                return item_list[k-1]
    return None

def write_file(file, data):
    try:
        with open(file, 'w') as f:
            f.write(data)
            f.close()
    except OSError as e:
        print('Writing file error({}): {}'.format(e.errno, e.strerror))
    return
