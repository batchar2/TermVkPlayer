# -*- coding: utf-8 -*-

import curses

from unidecode import unidecode
from win_base import BaseWin



class AlbomItem:
    """ Хранит информацию о единственном треке """
    
    def __init__(self, data, size):
        
        self.__title = self.__translit(data[u'title'])
        self.__id = data[u'id']

        self.__template = '{1:>%d}' % (size-10)
    
    def __str__(self):
        #print self.__title
        """ Генерирую такую вот строку: ->    id     Title   Author   Genre    Time  """
        return self.__title
        #return self.__template.format(self.__title)


    def __translit(self, locallangstring):
        return unidecode(locallangstring.encode('utf-8'))


    def get_id(self):
        if self.__id == -1:
            return None
        else:
            return self.__id

    def get_title(self):
        return self.__title



class AlbomItemList:
    """ Хранит список треков. Класс реализует иттератор """
    def __init__(self):
        
        self.__albom_list = []
        # номер трека, с нуля начинается
        self.count_items = 0 
        

    def set_data(self, data, size):
        """ Добавление данных в класс. """
        
        self.__count_items = 0 
        self.__current_position = 0
        if data is not None:
            if len(data) != 0:
                item = {
                    u'id': -1,
                    u'title': u'[all]',
                }
                obj = AlbomItem(item, size)
                self.__albom_list.append(obj)
                self.__count_items += 1

                # сохраняю элементы
                for item in data[u'items']:
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



"""
Содержится картинка и информация для управления приложением. Картинка, ну - это прикольно :)
"""
class AlbomsWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y, max_cols, color_select, color_item, color_play):
        super(AlbomsWin, self).__init__(parent_win, rows, cols, x, y)
        #self.cols = cols - 3
        self.win_set_title("Alboms")

        #self.albom_list_pad = curses.newpad(self.cols, 10)
        self.albom_list_pad = curses.newpad(30, self.cols)

        #self.albom_list_pad.mvwin(1,1)
        
        self.max_cols = max_cols
        self.color_select = color_select
        self.color_item = color_item
        self.color_play = color_play

        self.count_data, self.data = 0, []
        # текущая "выбираемая" позиция
        self.current_position = 0
        # текущая выбранная композиция
        self.select_positon = -1
        # размер списка
        self.list_size = self.rows-4
        # начало и конец отображаемого списка
        self.begin_win, self.end_win = 0, self.list_size

        self.refresh()

    def set_data(self, data):
        self.alboms = AlbomItemList()
        self.current_position = 0
        self.select_positon = -1

        #print data

        if data is None:    return
        
        if len(data['items']) == 0:
            self.count_data = 0
        else:
            self.alboms.set_data(data, self.rows)
            self.count_data = len(data['items']) + 1

    """ перерисовываю элемент списка """
    def __rewrite_record_list_item(self, obj, color, position):
        #print self.x, self.rows, self.cols, self.y
        #self.albom_list_pad.addstr(position, self.rows, str(obj), color)
        #self.albom_list_pad.addstr(position, 0, self(obj))
        self.albom_list_pad.addstr(position, 1, str(obj), color)
        

    def show_data(self):
        """ Вывожу все данные  """
        position = 0
        for obj in self.alboms:
            if position == 0:
                self.__rewrite_record_list_item(obj, self.color_select, position)
            else:
                self.__rewrite_record_list_item(obj, self.color_item, position)
            position += 1

        self.refresh()

    
    """ Перерисовывает список. В зависимости от позиции курсора показывает определенную часть списка """
    def refresh(self):

        super(AlbomsWin, self).refresh()
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
        
        #self.albom_list_pad.box()
        #self.albom_list_pad.refresh(self.begin_win, 0, self.x+1, 1, self.rows+7, self.cols)
        #self.albom_list_pad.refresh(self.begin_win, 1, self.x+1, 1, self.rows, self.cols+10)
        #self.albom_list_pad.refresh(0, 0, 5, 5, 20, 75)

        self.albom_list_pad.refresh(0, 0, self.x+1, self.y+1, self.cols-1, self.max_cols-3)
        #self.albom_list_pad.refresh(0, 0, 15, self.y, 50, 150)
    
    """ Перемещение указателя вверх """
    def move_up(self):
        
        if self.current_position > 0:
            #self.tracks.set_marker(self.current_position, False)
            # отмечаю проигрываемый трек
            if self.current_position == self.select_positon:
                self.__rewrite_record_list_item(self.alboms.get(self.current_position), 
                                                    self.color_play, self.current_position)               
            else:
                self.__rewrite_record_list_item(self.alboms.get(self.current_position), 
                                                    self.color_item, self.current_position)            
            
            self.current_position -= 1
            if self.current_position != self.select_positon:
                #self.tracks.set_marker(self.current_position, True)
                self.__rewrite_record_list_item(self.alboms.get(self.current_position), 
                                                    self.color_select, self.current_position)
            self.refresh()


    """ Перемещение указателя вниз """
    def move_down(self):
        
        if self.current_position < self.count_data - 1:
            #self.tracks.set_marker(self.current_position, False)
            # отмечаю проигрываемый трек
            if self.current_position == self.select_positon:
                self.__rewrite_record_list_item(self.alboms.get(self.current_position), 
                                                    self.color_play, self.current_position)               
            else:
                self.__rewrite_record_list_item(self.alboms.get(self.current_position), 
                                                    self.color_item, self.current_position)            
            
            self.current_position += 1
            if self.current_position != self.select_positon:
                #self.tracks.set_marker(self.current_position, False)
                self.__rewrite_record_list_item(self.alboms.get(self.current_position), 
                                                    self.color_select, self.current_position)
            self.refresh()

    def select_albom_get_data(self):
        # "разотмечаю" предыдущую позицию
        if self.select_positon != -1:
        #    self.alboms.set_marker(self.select_positon, False)
            self.__rewrite_record_list_item(self.alboms.get(self.select_positon), 
                                            self.color_item, self.select_positon)

        self.select_positon = self.current_position
        # отмечаю новую
        #self.alboms.set_marker(self.select_positon, True)
        self.__rewrite_record_list_item(self.alboms.get(self.select_positon), 
                                            self.color_play, self.select_positon)


        self.refresh()
    
        return self.alboms.get(self.select_positon)

    def hide_cursor(self):
        if self.current_position != -1:
            self.__rewrite_record_list_item(self.alboms.get(self.current_position), 
                                            self.color_item, self.current_position)
        if self.select_positon != -1:
            self.__rewrite_record_list_item(self.alboms.get(self.select_positon), 
                                            self.color_item, self.select_positon)
        self.refresh()
        

    def show_cursor(self):
        if self.current_position != -1:
            self.__rewrite_record_list_item(self.alboms.get(self.current_position), 
                                            self.color_select, self.current_position)
        if self.select_positon != -1:
            self.__rewrite_record_list_item(self.alboms.get(self.select_positon), 
                                            self.color_play, self.select_positon)
        self.refresh()