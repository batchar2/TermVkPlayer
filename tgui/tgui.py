from .CursesInstance import CursesInstance

from .forms.BuilderForm import BuilderLogin, BuilderPlayer 



""" Текстовый интерфейс приложения. Реализован на ncurses """
class TerminalGUI:

    _curses_instance = None
    _color_sheme = None

    _builder_login = None
    _builder_player = None

    def __init__(self):
        self._curses_instance = CursesInstance()

        self._builder_login = BuilderLogin(self._curses_instance)
        self._builder_player = BuilderPlayer(self._curses_instance)

        #rows, cols = self._curses_instance.stdscr.getmaxyx()


        #self._info = WinPlayerInfo(self._curses_instance, 0, 0, 10, 10)
        #self._header.refresh()


        #self._header.refresh()

    def __call__(self):
        while True:
            ch = self._curses_instance.stdscr.getch()
            print(ch)


