# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


from wins.base import BaseWin

import curses
import curses.textpad

class ActionForm(BaseWin):
    __metaclass__ = ABCMeta
    """
    Базовый класс представления сложной логики взаимодействия с пользователем. 
    """

    def __init__(self, parent_win, rows, cols, x, y, color_content):
        super(ActionForm, self).__init__(parent_win, rows, cols, x, y)
        
        self.color_content = color_content
        self.win_set_title(u"Login")
        
        #self.__tmpl = "{0:16}  {1:>%d}" % (self.cols - 23)

        #self.win.addstr(2, 2, self.__tmpl.format(pg_name, pg_version), self.color_content)
        #self.set_status_undef()
        self.refresh()


    @abstractmethod
    def __call__(self, storage, curses_property):
        return False


class ActionLoginForm(ActionForm):
    """
    Форма авторизации пользователя.
    """
    def __init__(self, parent_win, rows, cols, x, y, color_content):
        super(ActionLoginForm, self).__init__(parent_win, rows, cols, x, y, color_content)


    def _make_ui(self):
        begin_x = 20
        begin_y = 7
        height = 5
        width = 40
    
        tb = curses.textpad.Textbox(self.win, insert_mode=True)
        #tb.box()
        text = tb.edit()
        #curses.addstr(8, 8, text.encode('utf_8'))


    def __call__(self, storage, curses_app):
        self._make_ui()
        while True:
            curses_app.refresh()
            self.refresh()
            curses_app.getch()
        
        return True