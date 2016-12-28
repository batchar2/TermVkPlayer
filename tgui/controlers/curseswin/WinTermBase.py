import curses

from abc import ABCMeta

"""
Реализация базового класса окна
"""
#class WinTermBase(metaclass=ABCMeta):
class WinTermBase:

    _curses_instance = None
    _win = None

    def __init__(self, curses_instance,
                    x=0, y=0, rows=0, cols=0, parent=None):

        self._curses_instance = curses_instance
        self._x, self._y = x, y
        self._cols, self._rows = cols, rows
        self._parent = parent

        self._win = curses.newwin(self._rows, self._cols, self._x, self._y)
        self._win.box()

        self.refresh()

    def set_title(self, title):
        text = '|{0}|'.format(title)
        self._win.addstr(text)

    @property
    def curses_instance(self):
        return self._curses_instance

    @property
    def win(self):
        return self._win

    def refresh(self):
        self._win.refresh()