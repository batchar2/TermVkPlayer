# -*- coding: utf-8 -*-

import curses
import time

from win_base import BaseWin
from unidecode import unidecode

class TrackItem:
    """ Хранит информацию о единственном треке """
    # список жанров ВК
    genres =   {
        '1': 'Rock',
        '2': 'Pop',
        '3': 'Rap & Hip-Hop',
        '4': 'Easy Listening',
        '5': 'Dance & House',
        '6': 'Instrumental',
        '7': 'Metal',
        '21': 'Alternative',
        '8': 'Dubstep',
        '9': 'Jazz & Blues',
        '10': 'Drum & Bass',
        '11': 'Trance',
        '12': 'Chanson',
        '13': 'Ethnic',
        '14': 'Acoustic & Vocal',
        '15': 'Reggae',
        '16': 'Classical',
        '17': 'Indie Pop',
        '19': 'Speech',
        '22': 'Electropop & Disco',
        '18': 'Other',
    }
    


    def __init__(self, data, template, position, ptr, title_size, artist_size):
        if u'genre_id' not in data:
            data[u'genre_id'] = '18'
        
        #if u'artist' in data:
        #    if data[u'artist'][0] == ' ':
        #        data[u'artist'] = data[u'artist'][1:]
        #    else:
        #        data[u'artist'] = ' '

        #if u'title' in data:
        #    if data[u'title'][0] == ' ':
        #        data[u'title'] = data[u'title'][1:]
        #else:
        #    data[u'title'] = ' '

        self.__ptr = ptr
        self.__title = self.__translit(data[u'title'])
        self.__artist = self.__translit(data[u'artist']).replace('  ', ' ')
        self.__genre = self.__get_genre_name(data[u'genre_id'])
        self.__time = self.__get_time(data['duration'])

        self.__title_size = title_size - 3
        self.__artist_size = artist_size - 1
        self.__position = position
        self.__template = template


    def set_ptr(self, ptr):
        """ устанавливаю маркер, индикатор, трека """
        self.ptr = ptr


    def __str__(self):
        """ Генерирую такую вот строку: ->    id     Title   Author   Genre    Time  """
        return self.__template.format(self.__ptr, str(self.__position+1), self.__title[0:self.__title_size],
                            self.__artist[0:self.__artist_size], self.__genre, self.__time)


    def __get_genre_name(self, key):
        """ сопоставляет номер с названием жанра. номера предопределены ВК  """
        if str(key) in self.genres:
            return self.genres[str(key)]
        else:
            return 'Other'


    """ секунды в нормальное, человеческое представление """
    def __get_time(self, total_time):
        total = time.strftime("%H:%M:%S", time.gmtime(total_time))
        return "%s" %(total)


    def __translit(self, locallangstring):
        return unidecode(locallangstring)



class TrackItemList:
    """ Хранит список треков. Класс реализует иттератор """
    def __init__(self):
        
        self.__track_list = []
        # номер трека, с нуля начинается
        self.count_items = 0 
        

    def set_data(self, data_list, template, title_size, artist_size):
        """ Добавление данных в класс. """
        self.__count_items = 0 
        self.__current_position = 0
        if data_list is not None:
            if len(data_list) != 0:
                # сохраняю элементы
                for item in data_list[u'items']:
                    obj = TrackItem(item, template, self.__count_items, 
                                        '   ', title_size, artist_size)
                    self.__track_list.append(obj)
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
            return self.__track_list[self.__current_position-1]
            
                

class TrackListWin(BaseWin): 
    """
    Список музыкальных произведений. Реализован скролинг и выбор.
    @parent_win - родительское окно
    @rows - колличество строк
    @cols - столбцов
    @x смещение по x
    @y смещение по y
    @color_select - выбранный трек
    @color_item - никак не выделеный трек
    @color_play - проигрываемый трек
    """    
    def __init__(self, parent_win, rows, cols, x, y, 
                    color_select, color_item, color_play):
        super(TrackListWin, self).__init__(parent_win, rows, cols, x, y)

        self.win_set_title("track list")

        self.color_select = color_select
        self.color_item = color_item
        self.color_play = color_play

        self.parent = parent_win
        self.cols = cols - 3
        # Собственно сам список
        self.track_list_pad = curses.newpad(1000, self.cols)
        #self.border_win.addstr(0, 2, u"Track list", curses.color_pair(150))
        # сюда кладу информацию обо всех треках
        self.count_data, self.data = 0, []
        # текущая "выбираемая" позиция
        self.current_position = 0
        # текущая выбранная композиция
        self.select_positon = -1
        # размер списка
        self.list_size = self.rows-4
        # начало и конец отображаемого списка
        self.begin_win, self.end_win = 0, self.list_size


        tmp_cols = self.cols - 33
        self.__artist_size = tmp_cols/3 - 3
        self.__track_size = tmp_cols - (tmp_cols/3) - 3

        #                      ->    id     Title   Author   Genre    Time        
        self.__templ= "{0:2} {1:3} {2:%d} {3:%d} {4:18} {5:8}" % (self.__track_size,
            self.__artist_size)

        # хранит список треков
        self.tracks = TrackItemList()


    
    def set_data(self, data_list):
        """  Добавление новых данных в список """
        if data_list is None:    return
        if len(data_list['items']) == 0: return

        self.tracks.set_data(data_list, self.__templ, self.__track_size, self.__artist_size)



    """ перерисовываю элемент списка """
    def __rewrite_record_list_item(self, obj, color, position):
        self.track_list_pad.addstr(position, 1, str(obj), color)
        """
        #     ->      id     Title   Author   Genre    Time 
        self.track_list_pad.addstr(position, 1, self.__format_str.format(
                ptr, 
                str(position+1), 
                data_item[u'title'],
                data_item[u'artist'],  
                self.__get_genre_name(data_item[u'genre_id']),
                self.__get_time(data_item['duration'])
            ), 
            color
        )
        """
        self.track_list_pad.addstr

    def show_data(self):
        """ Вывожу все данные  """
        position = 0
        for obj in self.tracks:
            if position == 0:
                self.__rewrite_record_list_item(obj, self.color_select, position)
            else:
                self.__rewrite_record_list_item(obj, self.color_item, position)
            position += 1

        self.refresh()
        """
        # "крашу" строку

        self.__ptr = '  '
        self.__color = track_COLOR
        if self.count_data == 0:
            self.__ptr, self.__color = ' ', SELECT_track_COLOR

        self.__rewrite_record_list_item(self.count_data,
            item, self.__color, self.__ptr)
        
        self.count_data += 1

        self.refresh()
        self.track_list_pad.refresh(self.begin_win, 0, self.x+1, 1, self.rows+7, self.cols)
        """
    
    """ Перерисовывает список. В зависимости от позиции курсора показывает определенную часть списка """
    def refresh(self):

        super(TrackListWin, self).refresh()
        if self.current_position > self.end_win:
            if self.end_win >= self.count_data -1:
                return
            else:
                self.begin_win += (self.list_size/2)
                self.end_win += (self.list_size/2)
        elif self.current_position < self.begin_win:
            if self.current_position <= 0:
                return
            else:
                self.begin_win -= (self.list_size/2)
                self.end_win -= (self.list_size/2)
        
        self.track_list_pad.refresh(self.begin_win, 0, self.x+1, 1, self.rows+7, self.cols)
                    
        
    """ Перемещение указателя вверх """
    def move_up(self):
        if self.current_position > 0:
            ## отмечаю проигрываемый трек
            if self.current_position == self.select_positon:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], SELECT_track_PLAY_COLOR, '->')
            else:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], track_COLOR, '  ')

            self.current_position -= 1
            if self.current_position != self.select_positon:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], SELECT_track_COLOR, '  ')
                
            self.refresh()

    """ Перемещение указателя вниз """
    def move_down(self):
        if self.current_position < self.count_data - 1:
            # отмечаю проигрываемый трек
            if self.current_position == self.select_positon:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], SELECT_track_PLAY_COLOR, '->')
            else:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], track_COLOR, '  ')
                    
            self.current_position += 1
            if self.current_position != self.select_positon:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], SELECT_track_COLOR, '  ')

            self.refresh()

    """ Возвращает данные о выбранном треке """
    def select_track_get_data(self):
        # "разотмечаю" предыдущую позицию
        if self.select_positon != -1:
            self.__rewrite_record_list_item(self.select_positon, 
                    self.data[self.select_positon], track_COLOR, '  ')


        self.select_positon = self.current_position
        # отмечаю новую
        self.__rewrite_record_list_item(self.select_positon, 
                self.data[self.select_positon], SELECT_track_PLAY_COLOR, '->')

        self.refresh()
    
        return self.data[self.select_positon]


    """ переключает на след.трек,вызывается автоматически по завершению воспроизведения """
    def next_track(self):
        if self.select_positon == self.count_data -1:
            self.select_positon = 0

        # затираю старое
        if self.select_positon != -1:
            self.__rewrite_record_list_item(self.select_positon, 
                    self.data[self.select_positon], track_COLOR, '  ')

        # переписываю страку выбора, малоли-то
        self.__rewrite_record_list_item(self.current_position, 
                self.data[self.current_position], SELECT_track_COLOR, '  ')

        self.select_positon += 1
        # отмечаю новую
        self.__rewrite_record_list_item(self.select_positon, 
                self.data[self.select_positon], SELECT_track_PLAY_COLOR, '->')
        self.refresh()


        return self.data[self.select_positon]

