# -*- coding: utf-8 -*-
import sys
import getpass
import locale
import threading
import time


from storage.storage import Storage

from ui.cursesapp import CursesApplication


from ui.commands import CommandInterfaces, CommandLogin, CommandKeyEnter, CommandRefresh

PLAYER_NAME = "VkTp"
PLAYER_VERSION = "0.6.1"

class Application(object):
    """ Главный класс приложения. Отвечает за построение системы и регистрацию событий системы """

    _is_stop = False
    _command_interface = CommandInterfaces()
    
    def __init__(self):
        self._storage = Storage('vk')
        self._curses_app = CursesApplication(PLAYER_NAME, PLAYER_VERSION, self.storage)

        self._add_commands()
        # перерисовываем окно
        self.run_command(cmd_name="refresh")

    """ Добавление команд, которые поддерживает система через ООП нотацию. """
    def _add_commands(self):
        self._command_interface.add_command("login", CommandLogin(self.curses_app, self.storage), None)
        self._command_interface.add_command("refresh", CommandRefresh(self.curses_app, self.storage), None)
        self._command_interface.add_command("key_enter", CommandKeyEnter(self.curses_app, self.storage), [10,])

    def run_loop(self):
        while self._is_stop is False:
            ch = self.curses_app.getch()

    """ Исполнение команды """
    def run_command(self, cmd_name=None, key_number=None):
        print "run_command", cmd_name, key_number
        if cmd_name is not None:
            self._command_interface(cmd_name=cmd_name)
        elif key_number is not None:
            self._command_interface(key_number=key_number)

    @property
    def storage(self):
        return self._storage

    @property
    def curses_app(self):
        return self._curses_app


if __name__ == '__main__':
    app = Application()
    app.run_loop()

    #curses.endwin()
