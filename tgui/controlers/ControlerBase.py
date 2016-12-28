class ControlerBase:
    _curses_instance = None

    def __init__(self, curses_instance):
        self._curses_instance = curses_instance

    def view_gui(self):
        pass

    def curses_instance(self):
        return self._curses_instance

    """ Получаем сообщения от интерфейса """ 
    def __call__(self, ch):
        print(ch)
