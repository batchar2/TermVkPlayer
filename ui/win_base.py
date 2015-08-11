# -*- coding: utf-8 -*-

""" Базовый клас для окон """
__metaclass__ = type

class BaseWin:
    def __init__(self, parent_win, rows, cols, x, y):
        self.parent_win = parent_win
        self.rows, self.cols, self.x, self.y = rows, cols, x, y 
        self.win = self.parent_win.subwin(rows, cols, x, y)

        #curses.wattron()
        self.win.box()

    def refresh(self):
        if self.win is not None:
            self.win.refresh()

    def win_set_title(self, title):
        pass
        # !!!!!!!!!!
        #self.win.addstr(0, 2, "|%s|" % title, curses.color_pair(6)) 

