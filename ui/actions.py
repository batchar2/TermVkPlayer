# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


from wins.base import BaseWin

import curses
import curses.textpad



class TextBox(object):
    def __init__(self, win, y, x, txt, title):
        self._win = win.derwin(1, 20, y, x+7)
        self._win.bkgd(' ', curses.color_pair(2))
        self._win.clear()
        self._txtbox = curses.textpad.Textbox(self._win)
        self._txtbox.stripspaces = True
        
        win.refresh()
        win.addstr(y, x, title)

        if txt is not None:
            self._insert(txt)
    
        self._win.refresh()

    def edit(self):
        return self._txtbox.edit()
  
    def value(self):
        return self._txtbox.gather()
  
    def _insert(self, txt):
        for ch in txt:
            self._txtbox.do_command(ch)
  

class PasswordBox(TextBox):
    def __init__(self, win, y, x, txt, title):
        self._password = ''
        super(PasswordBox, self).__init__(win, y, x, txt, title)
  
    def edit(self, cb=None):
        return self._txtbox.edit(self._validateInput)
  
    def value(self):
        return self._password
  
    def _validateInput(self, ch):
        if ch in (curses.KEY_BACKSPACE, curses.ascii.BS):
            self._password = self._password[0:-1]
            return ch
        elif curses.ascii.isprint(ch):
            self._password += chr(ch)
            return '*'
        else:
            return ch
  
    def _insert(self, str):
        for ch in str:
            self._password += ch
            self._txtbox.do_command('*')






class ActionForm(BaseWin):
    __metaclass__ = ABCMeta
    """
    Базовый класс представления сложной логики взаимодействия с пользователем. 
    """

    def __init__(self, parent_win, rows, cols, x, y, color_content):
        super(ActionForm, self).__init__(parent_win, rows, cols, x, y)
        
        self.color_content = color_content
        self.win_set_title(u"Login")
        
        self.refresh()

    def _make_field(self, title, width, height, x, y):
        self.parent_win.addstr(x, y, "|%s|" % title)
        field = self.parent_win.subwin(1, 30, self.x + 10, self.y + 2)
        field.box()
        field.refresh()

        #field = self.parent_win.subwin(height, width, x, y)
        #field.box()
        #field.refresh()
        return field


    @abstractmethod
    def __call__(self, storage, curses_property):
        return False


class ActionLoginForm(ActionForm):
    """
    Форма авторизации пользователя.
    """
    def __init__(self, parent_win, rows, cols, x, y, color_content):
        super(ActionLoginForm, self).__init__(parent_win, rows, cols, x, y, color_content)


    def make_field(self, title, width, height, x, y):
        
        field = self.parent_win.subwin(height, width, x, y)
        field.box()
        field.refresh()

    def _make_ui(self):

        self.refresh()
        tb = TextBox(self.win, 2, 2, "", "Login")

        tb2 = PasswordBox(self.win, 4, 2, "", "Password")
        #tb = TextBox(self.parent_win, 5, 5, "1234")
        tb.edit()
        tb2.edit()
        #self._login_field =  self._make_field(u"Login", 30, 1, self.x+3, self.y+2) ##self.parent_win.subwin(1, 30, self.x+10, self.y+2)
        #self._password_field =  self._make_field(u"Password", 30, 1, self.x+3, self.y+10)

        #self._login_field.box()
        #self._login_field.refresh()
        #self._login_field = self.win.subwin(4, 2, 5, 5)
        #self._login_field.box()
        
    
        #login = curses.textpad.Textbox(self._login_field)
        #passwd = curses.textpad.Textbox(self._password_field)
        #curses.textpad.rectangle(self.win, 1, 21, self.y+2, self.x+2)
        #tb.box()
        #text = login.edit()
        #text = passwd.edit()
        #curses.addstr(8, 8, text.encode('utf_8'))


    def __call__(self, storage, curses_app):
        self._make_ui()
        while True:
            #curses_app.refresh()
            #self.refresh()
            curses_app.getch()
        
        return True
