# -*- coding: utf-8 -*-

from win_base import BaseWin

class LabelSlk(object):
	""" Подобие функциональности slk_set """
	
	"""
		@index - номер
		@text - текст
		@stdscr - параметры экрана
		@color - цвет
	"""
	def __init__(self, index, win, param, title, color_title, color_number):
		self.__index = index
		self.__title = title
		self.__win = win
		self.__rows, self.__cols = param
		self.color_title = color_title
		self.color_number = color_number
		# 10 лейблов, и 10 отступов
		self.__size_label = (self.__cols / 8)

		self.__tmpl = "{:<%d}" % (self.__size_label-3)

		self.show()
		#self.__tmpl = "{1:<10}"

	def show(self):
		title = self.__tmpl.format(self.__title)
		self.__win.addstr(self.__rows-1, (self.__index * self.__size_label)+1, 
							"%d" % (self.__index+1), self.color_number)

		self.__win.addstr(self.__rows-1, (self.__index * self.__size_label)+2, 
							title, self.color_title)

	def refresh(self):
		self.__win.refresh()