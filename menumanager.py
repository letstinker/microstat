



class MenuManager():
    menus = None
    selected = None
    def __init__(self, menus):
        self.menus = menus
    def select(self, menu_name):
        self.selected = self.menus[menu_name]
    def handle(self, **kwargs):
        kwargs['menu_name'] = self.selected['name']
        self.selected['method'](**kwargs)






#
# This is only ran when the script is ran directly and is for testing purposes.
#
def menu1(menu_name):
    print('menu 1....')
def menu2(menu_name):
    print('menu 2....')
def menu3(menu_name):
    print('{}....'.format(menu_name))

m = {
    'menu1': {
        'name': 'menu1',
        'method': menu1
    },
    'menu2': {
        'name': 'menu2',
        'method': menu2
    },
    'menu3': {
        'name': 'menu3',
        'method': menu3
    }
}


if __name__ == "__main__":
    mm = MenuManager(m)
    mm.select('menu3')
    mm.handle()
