# -*- coding: utf-8 -*-

from win_base import BaseWin

"""
Окно с информацией о треке.
Название, альбом (если есть) и проч.
"""
class TrackInfoWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y, color_content):
        super(TrackInfoWin, self).__init__(parent_win, rows, cols, x, y)

        self.win_set_title(u"Info track")
        self.__tmpl = "{0:7} {1:>%d}" % (self.cols-11)
        self.color_content = color_content
        self.refresh()

    def set_data(self, trak):
        self.win.addstr(2, 2, self.__tmpl.format('Title:', trak.get_title()), self.color_content)
        self.win.addstr(3, 2, self.__tmpl.format('Artist:', trak.get_artist()), self.color_content)
        self.win.addstr(4, 2, self.__tmpl.format('Albom:', "  "), self.color_content)
        self.refresh()

    def set_data_undef(self):
        
        self.win.addstr(2, 2, self.__tmpl.format(' ', ' '), self.color_content)
        self.win.addstr(2, 3, self.__tmpl.format(' ', ' '), self.color_content)
        self.win.addstr(2, 2, self.__tmpl.format(' ', ' '), self.color_content)
        
        self.refresh()
