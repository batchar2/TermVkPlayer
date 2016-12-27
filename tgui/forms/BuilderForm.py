from .FormPlayer import FormPlayer

""" Руализую паттерн строитель. Строим интерфейс и возвращаем результат """

""" Базовый класс строителя """
class BuilderBase:
    _curses_instance = None
    def __init__(self, curses_instance):
        self._curses_instance = curses_instance

    def build(self):
        pass

    @property
    def instance(self):
        return self._curses_instance
    

""" Строит интерфейс формы логина """
class BuilderLogin(BuilderBase):
    def __init__(self, curses_instance):
        super(BuilderPlayerInterfaceGUI, self).__init__(curses_instance)
        self.result = PlayerInterface(curses_instance)


""" Строит интерфейс плеера """
class BuilderPlayer(BuilderBase):
    def __init__(self, curses_instance):
        super(BuilderPlayerInterfaceGUI, self).__init__(curses_instance)
        self.result = PlayerInterface(curses_instance)