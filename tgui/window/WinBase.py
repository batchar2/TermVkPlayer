
import curses

"""
Реализуем singlton. Инициализация curses происходит ОДИН раз.
"""
class WinBase(object):

    COLOR_BORDER = 1
    COLOR_SELECTED_TRACK = 2
    COLOR_NON_SELECTED_TRACK = 3
    COLOR_PLAY_TRACK = 4

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
        """ Инициализирую curses. Инициализирую переменные цветов """
        self._stdscr = curses.initscr()
        self._stdscr.clean()
        
        curses.cbreak()
        curses.noecho()
        
        self._stdscr.keypad(0)

        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()


        curses.init_pair(self.COLOR_BORDER, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(self.COLOR_SELECTED_TRACK, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(self.COLOR_NON_SELECTED_TRACK, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(self.COLOR_PLAY_TRACK, curses.COLOR_YELLOW, curses.COLOR_YELLOW)


    @property
    def stdscr(self):
        return self._stdscr
            