# -*- coding: utf-8 -*-

from win_base import BaseWin

"""
Окно с системной информацией.
Тут приводится значения громкости, выставленной для приложения, статус и проч.
"""
class SystemInfoWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y, pg_name, pg_version, color_content):
        super(SystemInfoWin, self).__init__(parent_win, rows, cols, x, y)
        
        self.color_content = color_content
        self.win_set_title(u"System info")
        
        self.__tmpl = "{0:16}  {1:>%d}" % (self.cols - 23)

        self.win.addstr(2, 2, self.__tmpl.format(pg_name, pg_version), self.color_content)
        self.set_status_undef()
        self.refresh()

    def set_status_undef(self):
        self.win.addstr(3, 2, self.__tmpl.format('Status', '-------'), self.color_content)
        self.refresh()

    def set_status_playning(self):
        self.win.addstr(3, 2, self.__tmpl.format('Status', 'Playning'), self.color_content)
        self.refresh()

    def set_status_paused(self):
        self.win.addstr(3, 2, self.__tmpl.format('Status', 'Paused'), self.color_content)
        self.refresh()

    def set_sound_volume(self, volume):
        self.volume = "%d%%" % int(float(round(volume, 2))*100)
        self.win.addstr(4, 2, self.__tmpl.format('Volume', self.volume), self.color_content)        
        self.refresh()