# -*- coding: utf-8 -*-

from win_base import BaseWin
import curses

class LoginWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y, color):
        super(LoginWin, self).__init__(parent_win, rows, cols, x, y)
        #win = curses.newwin(rows, cols, 0, 0)
        self.parent_win = parent_win

        self.win_set_title(u"System info")
        
        self.win.addstr(2, 2, "Hello!", curses.color_pair(9))
        self.refresh()


    def refresh(self):
        if self.win is not None:
            self.win.refresh()

    def win_set_title(self, title):
        self.win.addstr(0, 2, "|%s|" % title)
