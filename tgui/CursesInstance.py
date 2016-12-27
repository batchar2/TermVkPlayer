
import curses

"""
Инициализация ncurses. Инициализирует цветовую палитру приложения
"""
class CursesInstance(object):

    _stdscr = None
    
    COLOR_BORDER = 1
    COLOR_SELECTED = 2
    COLOR_NON_SELECTED = 3
    COLOR_PLAY_TRACK = 4

    def __init__(self):
        self._stdscr = curses.initscr()
        self._stdscr.clear()
        
        curses.cbreak()
        curses.noecho()
        
        self._stdscr.keypad(0)
        self._init_color_sheme()

        self._stdscr.refresh()

    def _init_color_sheme(self):
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

        COLOR_BORDER_NUMBER = 1
        COLOR_SELECTED_TRACK_NUMBER = 2
        COLOR_NON_SELECTED_TRACK_NUMBER = 3
        COLOR_PLAY_TRACK_NUMBER = 4

        curses.init_pair(COLOR_BORDER_NUMBER, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(COLOR_SELECTED_TRACK_NUMBER, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(COLOR_NON_SELECTED_TRACK_NUMBER, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(COLOR_PLAY_TRACK_NUMBER, curses.COLOR_YELLOW, curses.COLOR_YELLOW)

        self.COLOR_BORDER = curses.color_pair(COLOR_BORDER_NUMBER)
        self.COLOR_SELECTED = curses.color_pair(COLOR_SELECTED_TRACK_NUMBER)
        self.COLOR_NON_SELECTED = curses.color_pair(COLOR_NON_SELECTED_TRACK_NUMBER)
        self.COLOR_PLAY_TRACK = curses.color_pair(COLOR_PLAY_TRACK_NUMBER)

    @property
    def stdscr(self):
        return self._stdscr

    def refresh(self):
        self._stdscr.refresh()
            