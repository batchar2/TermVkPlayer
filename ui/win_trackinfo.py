# -*- coding: utf-8 -*-

from win_base import BaseWin

"""
Окно с информацией о треке.
Название, альбом (если есть) и проч.
"""
class TrackInfoWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y):
        super(TrackInfoWin, self).__init__(parent_win, rows, cols, x, y)

        self.win_set_title(u"Info track")
        self.__tmpl = "{0:7} {1:>%d}" % (self.cols-11)

    def set_data(self, trak_data):
        self.win.addstr(2, 2, self.__tmpl.format('Title:', trak_data[u'title'].encode('utf-8')), curses.color_pair(6))
        self.win.addstr(3, 2, self.__tmpl.format('Artist:', trak_data[u'artist'].encode('utf-8')), curses.color_pair(6))
        self.win.addstr(4, 2, self.__tmpl.format('Albom:', "  "), curses.color_pair(6))
        self.refresh()

    def set_data_undef(self):
        
        self.win.addstr(2, 2, self.__tmpl.format(' ', ' '), curses.color_pair(6))
        self.win.addstr(2, 3, self.__tmpl.format(' ', ' '), curses.color_pair(6))
        self.win.addstr(2, 2, self.__tmpl.format(' ', ' '), curses.color_pair(6))
        #super(TrakInfoWin, self).refresh()
        self.refresh()
