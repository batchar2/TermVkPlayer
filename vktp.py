# -*- coding: utf-8 -*-
import sys
import getpass
import locale
import threading
import time


from storage.storage import Storage

from ui.cursesapp import CursesApplication

from ui.commands import CommandInterfaces, UnexpectedCommandError, CommandMakeUI, CommandLogin, CommandKeyEnter, CommandRefresh

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
       
        # Добавляю публичный метод для выполнения команд, экземпляр класса CommandInterfaces можно вызывать как функцию 
        self.run_command = self._command_interface


    """ Добавление команд, которые поддерживает система через ООП нотацию. """
    def _add_commands(self):
        self._command_interface.add_command("makeui", CommandMakeUI(self.curses_app, self.storage), [])
        self._command_interface.add_command("login", CommandLogin(self.curses_app, self.storage), [])
        self._command_interface.add_command("refresh", CommandRefresh(self.curses_app, self.storage), [])
        self._command_interface.add_command("key_enter", CommandKeyEnter(self.curses_app, self.storage), [10,])


    def run_loop(self):
        if self.run_command(cmd_name="login") is False:
            return False

        # перерисовываем окно
        #self.run_command(cmd_name="makeui")
        #self.run_command(cmd_name="refresh")

        while self._is_stop is False:
            try:
                ch = self.curses_app.getch()
                self.run_command(key_number=ch)
            except UnexpectedCommandError as e:
                pass


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
