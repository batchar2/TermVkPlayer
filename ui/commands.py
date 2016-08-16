# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Command(object):
	 __metaclass__= ABCMeta
	""" Абстрактный класс для паттерна "Команда". """
	
	def __init__(self, obj, storage):
		self._obj = obj
		self._storage = storage

	@property
	def storage(self):
		return self._storage

	@property
	def obj(self):
		return self._obj


	@abstractmethod
	def __call__(self):
		pass



class CommandLogin(Command):
	""" Команда вывода окна для "логинизации" """

	def __init__(self, obj, storage):
		super(CommandLogin, self).__init__(obj, storage)

	def __call__(self):
		print "call"


class CommandKeyEnter(Command):
	""" Команда Enter """
	def __init__(self, obj, storage):
		super(CommandLogin, self).__init__(obj, storage)

	def __call__(self):
		print "call"


class CommandInterfaces(object):
	""" Интерфейс для команд. """
	
	def __init__(self):
		self._commands = []

	""" Добавление команды в коммандный интерфейс
		cmd_name - имя команды
		cmd - объект команды
	"""
	def add_command(self, cmd_name, cmd):
		self._commands.append({cmd_name: cmd})

	""" Вызов интерфейса с параметром имя команды.
		True - успешно отработано
		False - косяк
		None - жеский косяк, исправить на исключение
	"""
	def __call__(self, cmd_name):
		if cmd_name in self._commands:
			return self._commands[cmd_name]()
		else:
			return None

