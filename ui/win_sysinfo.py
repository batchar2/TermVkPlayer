# -*- coding: utf-8 -*-

from win_base import BaseWin

"""
Окно с системной информацией.
Тут приводится значения громкости, высталвенной для приложения, статус и проч.
"""
class SystemInfoWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y):
        super(SystemInfoWin, self).__init__(parent_win, rows, cols, x, y)
        self.win_set_title(u"System info")
        

        self.__tmpl = "{0:16}  {1:>%d}" % (self.cols - 23)

        #self.win.addstr(2, 2, self.__tmpl.format(PG_NAME, PG_VERSION), curses.color_pair(6))
        self.set_status_undef()

    def set_status_undef(self):
        #self.win.addstr(3, 2, self.__tmpl.format('Status', '-------'), curses.color_pair(6))
        self.refresh()

    def set_status_playning(self):
        #self.win.addstr(3, 2, self.__tmpl.format('Status', 'Playning'), curses.color_pair(6))
        self.refresh()

    def set_status_paused(self):
        #self.win.addstr(3, 2, self.__tmpl.format('Status', 'Paused'), curses.color_pair(6))
        self.refresh()

    def set_sound_volume(self, volume):
        self.volume = "%d%%" % int(float(round(volume, 2))*100)
        #self.win.addstr(4, 2, self.__tmpl.format('Volume', self.volume), curses.color_pair(6))        
        self.refresh()
