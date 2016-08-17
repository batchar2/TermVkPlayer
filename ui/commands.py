# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class UnexpectedCommandError(Exception):
    """ Исключение, которое должно выпадать при попытки выполнить неизвестную команду """
    def __init__(self, message, error=None):
        self._message = message
        self._error = error

    def __str__(self):
        return self._message

    def __repr_(self):
        return self._message


class Command(object):
    __metaclass__= ABCMeta
    """ Абстрактный класс для паттерна "Команда". """
    
    def __init__(self, curses_app, storage):
        self._curses_app = curses_app
        self._storage = storage

    @property
    def storage(self):
        return self._storage

    @property
    def curses_app(self):
        return self._curses_app


    @abstractmethod
    def __call__(self):
        pass



class CommandLogin(Command):
    """ Команда вывода окна для "логинизации" """
    def __init__(self, curses_app, storage):
        super(CommandLogin, self).__init__(curses_app, storage)

    def __call__(self):
        return self.curses_app.action_login()


class CommandRefresh(Command):
    """ Команда перерисовки всего содержимого экрана """
    def __init__(self, curses_app, storage):
        super(CommandRefresh, self).__init__(curses_app, storage)

    def __call__(self):
        return self.curses_app.refresh()


class CommandMakeUI(Command):
    """ Производит построение интерфейса """
    def __init__(self, curses_app, storage):
        super(CommandMakeUI, self).__init__(curses_app, storage)

    def __call__(self):
        return self.curses_app.makeui()


class CommandKeyEnter(Command):
    """ Команда Enter """
    def __init__(self, curses_app, storage):
        super(CommandKeyEnter, self).__init__(curses_app, storage)

    def __call__(self):
        print "call"
        return True


class CommandInterfaces(object):
    """ Интерфейс для команд. """
    
    def __init__(self):
        self._commands = []

    """ 
    Добавление команды в коммандный интерфейс
    cmd_name - имя команды
    cmd - объект команды
    key - номер клавиши
    """
    def add_command(self, cmd_name, cmd, keys):
        self._commands.append({"name": cmd_name, "obj": cmd, "keys": keys})

    """ 
    Вызов интерфейса с параметром имя команды.
    True - успешно отработано
    False - косяк
    В случае ошибки исключение UnexpectedCommandError
    """
    def __call__(self, cmd_name=None, key_number=None):
        #print cmd_name, key_number, self._commands
        command = None
        if cmd_name is not None:
            cmd = filter(lambda e: e['name'] == cmd_name, self._commands)
        elif key_number is not None:
            cmd = filter(lambda e: key_number in e["keys"], self._commands)
        else:
            raise UnexpectedCommandError("Undefine command")

        if len(cmd) > 0:
            command = cmd[0]["obj"]

        print command
        if command is None:
            raise UnexpectedCommandError("Undefine command")
        else:
            return command()

