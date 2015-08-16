# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty

#""" Базовый клас для окон """
#__metaclass__ = type

class BaseWin(object):
    """ Базовый абстрактный класс для окон """
    #__metaclass__ = ABCMeta

    def __init__(self, parent_win, rows, cols, x, y, color_header=None):
        self.parent_win = parent_win
        self.rows, self.cols, self.x, self.y = rows, cols, x, y 
        self.win = self.parent_win.subwin(rows, cols, x, y)
        self.color_header = color_header

        self.win.box()

    def refresh(self):
        if self.win is not None:
            self.win.refresh()

    def win_set_title(self, title):
        self.win.addstr(0, 2, "|%s|" % title)
        # !!!!!!!!!!
        #self.win.addstr(0, 2, "|%s|" % title, curses.color_pair(6)) 

