# -*- coding: utf-8 -*-
import time

from unidecode import unidecode

from win_base import BaseWin
from win_base_list import BaseListWin

class TrackItem:
    """ Хранит информацию о единственном треке """

    def __init__(self, data, template, position, title_size, artist_size):

        self.__title = self.__translit(data['title'])
        self.__artist = self.__translit(data['artist'])
        self.__genre = data['genre_title']
        self.__genre_id = data['genre_id']
        self.__time = self.__get_time(data['duration'])

        self.__url = data['url']

        self.__title_size = title_size - 3
        self.__artist_size = artist_size - 1
        self.__position = position
        self.__template = template

        self.__marker, self.__ptr = False, '  '

    def __str__(self):
        """ Генерирую такую вот строку: ->    id     Title   Author   Genre    Time  """
        return self.__template.format(self.__ptr, str(self.__position+1), self.__title[0:self.__title_size],
                            self.__artist[0:self.__artist_size], self.__genre, self.__time)

    def __get_time(self, total_time):
        """ секунды в нормальное, человеческое представление """
        total = time.strftime("%H:%M:%S", time.gmtime(total_time))
        return "%s" %(total)


    def __translit(self, locallangstring):
        return unidecode(locallangstring)

    @property 
    def url(self):
        return self.__url

    @property
    def title(self):
        return self.__title

    @property
    def artist(self):
        return self.__artist

    @property
    def marker(self):
        return self.__ptr
        
    @marker.setter
    def marker(self, value):
        """ устанавливаю маркер, индикатор, трека """
        if value is True:
            self.__ptr = '->'
        else:
            self.__ptr = '  '


class TrackItemList:
    """ Хранит список треков. Класс реализует иттератор """

    def __init__(self):
        self.__data = []
        # номер трека, с нуля начинается
        self.__count_items = 0 
        

    def set_data(self, data_list, template, title_size, artist_size):
        """ Добавление данных в класс. """
        self.__count_items = 0 
        self.__current_position = 0
        if data_list is not None:
            if len(data_list) != 0:
                # сохраняю элементы
                for item in data_list:
                    obj = TrackItem(item, template, self.__count_items, 
                                        title_size, artist_size)
                    self.__data.append(obj)
                    self.__count_items += 1


    def __iter__(self):
        """ Сам себе итератор """
        return self


    def next(self):
        """ Реализую итератор  """
        if self.__count_items == 0 or self.__current_position >= self.__count_items:
            raise StopIteration
        else:
            self.__current_position += 1
            return self.__data[self.__current_position-1]


    def set_marker(self, index, is_select):
        """ Установка "марккера", т.е. вот такой стрелочки "->", указывает на проигрываемый трек  """
        self.__data[index].marker = is_select;


    def get(self, index):
        return self.__data[index]




class TrackListWin(BaseListWin):

    """ реализует спиок на основе вызова ncurses newpad() """
    def __init__(self, parent_win, rows, cols, x, y, 
                    color_select, color_item, color_play):

        """
        Список музыкальных произведений. Реализован скролинг и выбор.
        @parent_win - родительское окно
        @rows - колличество строк
        @cols - столбцов
        @x смещение по x
        @y смещение по y
        @color_select - цвет выбраного трека
        @color_item - цвет никак не выделеного трека
        @color_play - цвет проигрываемого трека
        """
        super(TrackListWin, self).__init__(parent_win, rows, cols, x, y, 
                                            color_select, color_item, color_play)
        self.win_set_title("Track list")

        tmp_cols = self.cols - 42
        self._artist_size = tmp_cols/3
        self._track_size = tmp_cols - (tmp_cols/3)

        """           ->     id    Title  Author Genre  Time   """
        self._templ= "{0:2} {1:3} {2:%d} {3:%d} {4:18} {5:8}  " % (self._track_size,
            self._artist_size)


    def set_data(self, data_list):
        """ установка данных """

        if self._count_data != 0:
            self.clear()

        self._data = None
        self._begin_win = 0
        """  Добавление новых данных в список """
        self._current_position, self._select_positon = 0, -1

        if data_list is None:
            return

        self._count_data = len(data_list)

        if len(data_list) != 0:
            self._data = TrackItemList()
            self._data.set_data(data_list, self._templ, self._track_size, self._artist_size)