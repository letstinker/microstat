import os
import time
import json


class ConfigStore():
    config = {}
    config_file = ''
    defaults = {
        'temp_desired': 75.0,
        'temp_sensed': None,
        'temp_mode': 'OFF'
    }
    last_modify = 0

    def __init__(self, config_file='config.json', defaults=None, realtime_save=False):
        self.config_file = config_file
        self.realtime_save = realtime_save

        if defaults:
            self.defaults = defaults
        self.load_file()

    def check_save(self):
        ''' Check if last_modify has been set and save if its time. '''
        if self.last_modify != 0 and (time.time() - self.last_modify) > 2:
            self.last_modify = 0
            print('Saving...')
            self.save()
    
    def queue_save(self):
        ''' sets last_modify so check_save knows to check it and save if its time. '''
        self.last_modify = time.time()

    def load_file(self):
        ''' Tries to load the file and if it can't it creates it '''
        try:
            with open(self.config_file) as f:
                self.config = json.loads(f.read())
                f.close()
        except OSError:
            # File doesnt Exist but lets try to create it
            self.create_file()

    def create_file(self):
        ''' Creates a new config with defaults then saves the files. '''
        self.config = self.defaults
        self.save()

    def save(self):
        ''' Tries to save the file and throws an error if it can't. '''
        try:
            with open(self.config_file, 'w') as f:
                f.write(json.dumps(self.config))
                f.close()
        except OSError as e:
                print('Writing file error({}): {}'.format(e.errno, e.strerror))

    def reload(self):
        ''' Alias to load_file '''
        self.load_file()

    def reset(self):
        ''' Sets the config to defaults and saves the file. '''
        self.config = self.defaults
        self.save()

    def set(self, name, value, valid_values=None):
        ''' Sets a value in the config then if realtime_save is true saves it. '''

        # Check if validation should be used and if so validate and use default
        # If invalid
        if valid_values:
            values, default = valid_values
            if value not in values:
                value = default

        self.config[name] = value
        if self.realtime_save:
            self.save()
        else:
            self.queue_save()

    def get(self, name):
        ''' Gets a config value, if it cant tries defaults, if it cant then None. '''
        return self.config.get(name, self.defaults.get(name, None))

    def get_all(self):
        ''' Returns the entire config '''
        return self.config

if __name__ == "__main__":
    config = ConfigStore()
    print('Writing...')
    config.set('test', 'VALUE')
    print('Writing...')
    config.set('test1', 'VALUE')
    print('Writing...')
    config.set('test2', 'VALUE')
    print('Writing...')
    config.set('test3', 'VALUE')
    print('Writing...')
    config.set('test4', 'VALUE')
    print('Writing...')
    config.set('test5', 'VALUE')
    print(config.get_all())
    while True:
        print('Looping to let save have a chance to run...')
        config.check_save()
        time.sleep(.5)