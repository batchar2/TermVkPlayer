# -*- coding: utf-8 -*-

import curses

from unidecode import unidecode

from win_base import BaseWin
from win_base_list import BaseListWin

class AlbomItem:
    """ Хранит информацию о единственном треке """
    
    def __init__(self, data, size):
        

        self.__title = self.__translit(data['title'])
        self.__id = data['id']
        self.__template = '{1:>%d}' % (size-10)
    
        #print self.__title

    def __str__(self):
        return self.__title
        #return self.__template.format(self.__title)


    def __translit(self, s):
        return unidecode(s)

    @property
    def id(self):
        if self.__id == -1:
            return None
        else:
            return self.__id
    @property
    def title(self):
        return self.__title



class AlbomItemList:
    """ Хранит список треков. Класс реализует иттератор """
    def __init__(self):
        
        self.__albom_list = []
        # номер трека, с нуля начинается
        self.__count_items = 0 
        

    def set_data(self, data_list, size):
        """ Добавление данных в класс. """
        
        self.__count_items = 0 
        self.__current_position = 0
        if data_list is not None:
            # сохраняю элементы
            for item in data_list:
                #print item
                obj = AlbomItem(item, size)
                self.__albom_list.append(obj)
                self.__count_items += 1

                
    def __iter__(self):
        """ сам себе итератор """
        return self


    def next(self):
        """ реализую итератор.  """
        if self.__count_items == 0 or self.__current_position >= self.__count_items:
            raise StopIteration
        else:
            self.__current_position += 1
            return self.__albom_list[self.__current_position-1]

    def get(self, index):
        return self.__albom_list[index]

    def set_marker(self, index, is_select):
        #тут нужно поминять цвет
        pass
        #self.__data[index].marker = is_select;


class AlbomsWin(BaseListWin):
    """ Список альбомов пользователя """
    def __init__(self, parent_win, rows, cols, x, y, max_cols, 
                    color_select, color_item, color_play):
        
        super(AlbomsWin, self).__init__(parent_win, rows, cols, x, y, 
                                            color_select, color_item, color_play)
        self.win_set_title("Alboms")
        self.__templ = "{0:%d}" % (cols-3)
        self.refresh()


    def set_data(self, data_list):
        """ установка данных """

        if self._count_data != 0:
            self.clear()

        self._data = None
        self._begin_win = 0
        """  Добавление новых данных в список """
        self._current_position, self._count_data, self._select_positon = 0, 0, -1

        if data_list is None:
            return

        self._count_data = len(data_list)
        
        if len(data_list) != 0:
            self._data = AlbomItemList()
            self._data.set_data(data_list, self.cols)
            