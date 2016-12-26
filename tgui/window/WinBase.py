
import curses

"""
Реализуем singlton. Инициализация curses происходит ОДИН раз.
"""
class WinBase(object):

    _stdscr = None
    _instance = None
    _init_replaced = False

    def __new__(cls,*dt,**mp):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        elif not cls.__init_replaced:
            # грязный трюк
            cls.__init__ = lambda x: None
            cls.__init_replaced = True  
        
        return cls.__instance

    def __init__(self):
        self._stdscr = curses.initscr()
        self._stdscr.clean()
        
        curses.cbreak()
        curses.noecho()
        
        self._stdscr.keypad(0)

        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()


    @property
    def stdscr(self):
        return self._stdscr
            