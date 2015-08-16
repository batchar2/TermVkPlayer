# -*- coding: utf-8 -*-

import curses

from abc import ABCMeta, abstractmethod, abstractproperty

from win_base import BaseWin


class BaseListWin(BaseWin):
    """ Базовый клас для списка. Реализует основные функции работы со списокм """

    def __init__(self, parent_win, rows, cols, x, y, 
                    color_select, color_item, color_play):
        
        super(BaseListWin, self).__init__(parent_win, rows, cols, x, y)

        self.__list_pad = curses.newpad(6000, self.cols-2)

        """ тут должен быть экземпляр класса реализующий иттератор и метод get, set_marker """
        self._data = None
        self.__color_select = color_select
        self.__color_item = color_item
        self.__color_play = color_play

        self._count_data = 0
        # текущая "выбираемая" позиция
        self._current_position = 0
        # текущая выбранная композиция
        self._select_positon = -1
        # размер списка, видимый в настоящий момент на экране
        self._list_size = self.rows-4
        # начало и конец отображаемого списка
        self._begin_win, self._end_win = 0, self._list_size


    def clear(self):
        """ очистка списка """
        for i  in range(self._count_data):
            s = self._templ.format("  ", "  ", "  ", "  ", "  ", "  ")
            self.__rewrite_record_list_item(s, self.__color_item, i)
    

    def __rewrite_record_list_item(self, obj, color, position):
        """ перерисовываю элемент списка """
        self.__list_pad.addstr(position, 1, str(obj), color)


    def show(self):
        """ Вывожу все данные на список. Используется для первоналального отображения данных """
        position = 0
        if self._data is not None:
            for obj in self._data:
                if position == 0:
                    # подсвеиваю трек как выделенный в списке
                    self.__rewrite_record_list_item(obj, self.__color_select, position)
                else:
                    # подсвечиваю трек как обычный
                    self.__rewrite_record_list_item(obj, self.__color_item, position)
                position += 1

        self.refresh()


    def refresh(self):        
        """ Перерисовывает список. В зависимости от позиции курсора показывает определенную часть списка """
        super(BaseListWin, self).refresh()
        
        # курсор переместился вниз
        if self._current_position > self._end_win:
            if self._end_win >= self._count_data -1:
                return
            else:
                self._begin_win += (self._list_size/2)
                self._end_win += (self._list_size/2)
        # курсор переметислся вверх
        elif self._current_position < self._begin_win:
            if self._current_position <= 0:
                return
            else:
                self._begin_win -= (self._list_size/2)
                self._end_win -= (self._list_size/2)
   

        self.__list_pad.refresh(self._begin_win, 0, self.x+1, self.y+1, self.rows+7, self.y+self.cols)


    def hide_cursor(self):
        """ Скрывает выделения в списке """
        if self._data is None: return
        if self._current_position != -1:
            self.__rewrite_record_list_item(self._data.get(self._current_position), 
                                            self.__color_item, self._current_position)
        if self._select_positon != -1:
            self.__rewrite_record_list_item(self._data.get(self._select_positon), 
                                            self.__color_item, self._select_positon)
        self.refresh()
        

    def show_cursor(self):
        """ Отображает выделения в списке """
        if self._data is None: return
        if self._current_position != -1:
            self.__rewrite_record_list_item(self._data.get(self._current_position), 
                                            self.__color_select, self._current_position)
        if self._select_positon != -1:
            self.__rewrite_record_list_item(self._data.get(self._select_positon), 
                                            self.__color_play, self._select_positon)
        self.refresh()


    def move_up(self):
        """ Перемещение указателя вверх """  
        if self._current_position > 0:
            #self._data.set_marker(self.current_position, False)
            # отмечаю выделенный элемент
            if self._current_position == self._select_positon:
                self.__rewrite_record_list_item(self._data.get(self._current_position), 
                                                    self.__color_play, self._current_position)               
            else:
                self.__rewrite_record_list_item(self._data.get(self._current_position), 
                                                    self.__color_item, self._current_position)            
            
            self._current_position -= 1
            if self._current_position != self._select_positon:
                #self._data.set_marker(self.current_position, True)
                self.__rewrite_record_list_item(self._data.get(self._current_position), 
                                                    self.__color_select, self._current_position)
            self.refresh()


    def move_down(self):
        """ Перемещение указателя вниз """        
        if self._current_position < self._count_data - 1:
            #self._data.set_marker(self.current_position, False)
            # отмечаю проигрываемый трек
            if self._current_position == self._select_positon:
                self.__rewrite_record_list_item(self._data.get(self._current_position), 
                                                    self.__color_play, self._current_position)               
            else:
                self.__rewrite_record_list_item(self._data.get(self._current_position), 
                                                    self.__color_item, self._current_position)            
            
            self._current_position += 1
            if self._current_position != self._select_positon:
                #self._data.set_marker(self.current_position, False)
                self.__rewrite_record_list_item(self._data.get(self._current_position), 
                                                    self.__color_select, self._current_position)
            self.refresh()


    def get_select_data(self):
        """ Возвращает данные о выбранном объекте и подсвечивает его """        
        # "разотмечаю" предыдущую позицию
        if self._select_positon != -1:
            self._data.set_marker(self._select_positon, False)
            self.__rewrite_record_list_item(self._data.get(self._select_positon), 
                                            self.__color_item, self._select_positon)

        self._select_positon = self._current_position
        # отмечаю новую
        self._data.set_marker(self._select_positon, True)
        self.__rewrite_record_list_item(self._data.get(self._select_positon), 
                                            self.__color_play, self._select_positon)
        self.refresh()
    
        return self._data.get(self._select_positon)
        