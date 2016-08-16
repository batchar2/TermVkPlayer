# -*- coding: utf-8 -*-
""" Реализуется паттен "Команда". Для упрощения взаимодействия классов и ответственности """





#class Command(metaclass=ABCMeta):
class Command(object):
    """ Базовый класс для всех комманд """
    #@abstractmethod
    #def execute(self):
    pass


class KeyEnterCommand(Command):
    """ Начать воспроизведение  """
    def __init__(self, curses_app):
        self.curses_app = curses_app

    def __call__(self):
        pass


class KeyUpCommand(Command):
    """ Переместить указатель вверх """
    def __init__(self, curses_app):
        self.curses_app = curses_app

    def __call__(self):
        pass


class KeyDownCommand(Command):
    """ Переместить указатель вниз """
    def __init__(self, curses_app):
        self.curses_app = curses_app
    
    def __call__(self):
        pass

class CursesApplicationInterface(object):
    """ Интерфейс команд для приложениея """
    def __init__(self, curses_app):
        self._current_command = None
        self.key_enter = KeyEnterCommand(curses_app)
        self.key_up = KeyUpCommand(curses_app)
        self.key_down = KeyDownCommand(curses_app)

    
    """
    def key_up(self):
        self._key_up()

    def key_down(self):
        self._key_down()

    def play_start(self):
        self._play_start()

    def _play_stop():
        self._play_stop()
    """
