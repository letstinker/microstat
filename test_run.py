import time
from microstat import MicroStat


if __name__ == "__main__":
    ms = MicroStat()
    
    print('Menu Mode: {}'.format(ms.get_menu_mode()))
    print('Desired temperature: {}'.format(ms.get_desired_temp()))
    print('System Mode: {}'.format(ms.get_system_mode()))

    while True:
        ms.action_check()
        time.sleep(0.01)