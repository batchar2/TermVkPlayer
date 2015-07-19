# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
import gobject
import sys
import locale
import signal
import random
import thread
import datetime
import threading
import time
import getpass


import curses
import vk_api


import pygst

pygst.require("0.10")

import gst

from unidecode import unidecode

locale.setlocale(locale.LC_ALL,"")

PG_NAME = "TermVkPlayer"
PG_VERSION = "v0.01"


# перемещение на время
PG_SEEK_TIME = 30
# время срабатывания таймера
TIME_SLEEP = 0.3


"""
    Базовый клас для окон
"""
__metaclass__ = type

class BaseWin:
    def __init__(self, parent_win, rows, cols, x, y):
        self.parent_win = parent_win
        self.rows, self.cols, self.x, self.y = rows, cols, x, y 
        self.win = self.parent_win.subwin(rows, cols, x, y)

        #curses.wattron()
        self.win.box()

    def refresh(self):
        if self.win is not None:
            self.win.refresh()

    def win_set_title(self, title):
        self.win.addstr(0, 2, "|%s|" % title, curses.color_pair(6)) 



"""
Окно с системной информацией.
Тут приводится значения громкости, высталвенной для приложения, статус и проч.
"""
class SystemInfoWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y):
        super(SystemInfoWin, self).__init__(parent_win, rows, cols, x, y)
        self.win_set_title(u"System info")
        

        self.__tmpl = "{0:16}  {1:>%d}" % (self.cols - 23)

        self.win.addstr(2, 2, self.__tmpl.format(PG_NAME, PG_VERSION), curses.color_pair(6))
        self.set_status_undef()

    def set_status_undef(self):
        self.win.addstr(3, 2, self.__tmpl.format('Status', '-------'), curses.color_pair(6))
        self.refresh()

    def set_status_playning(self):
        self.win.addstr(3, 2, self.__tmpl.format('Status', 'Playning'), curses.color_pair(6))
        self.refresh()

    def set_status_paused(self):
        self.win.addstr(3, 2, self.__tmpl.format('Status', 'Paused'), curses.color_pair(6))
        self.refresh()

    def set_sound_volume(self, volume):
        self.volume = "%d%%" % int(float(round(volume, 2))*100)
        self.win.addstr(4, 2, self.__tmpl.format('Volume', self.volume), curses.color_pair(6))        
        self.refresh()


"""
Окно с информацией о треке.
Название, альбом (если есть) и проч.
"""
class TrakInfoWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y):
        super(TrakInfoWin, self).__init__(parent_win, rows, cols, x, y)

        self.win_set_title(u"Info track")
        self.__tmpl = "{0:7} {1:>%d}" % (self.cols-11)

    def set_data(self, trak_data):
        self.win.addstr(2, 2, self.__tmpl.format('Title:', trak_data[u'title'].encode('utf-8')), curses.color_pair(6))
        self.win.addstr(3, 2, self.__tmpl.format('Artist:', trak_data[u'artist'].encode('utf-8')), curses.color_pair(6))
        self.win.addstr(4, 2, self.__tmpl.format('Albom:', "  "), curses.color_pair(6))
        self.refresh()

    def set_data_undef(self):
        
        self.win.addstr(2, 2, self.__tmpl.format(' ', ' '), curses.color_pair(6))
        self.win.addstr(2, 3, self.__tmpl.format(' ', ' '), curses.color_pair(6))
        self.win.addstr(2, 2, self.__tmpl.format(' ', ' '), curses.color_pair(6))
        #super(TrakInfoWin, self).refresh()
        self.refresh()


"""
Эквалайзер. ну, тут все понятно
"""
class EkvalayzerWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y):
        super(EkvalayzerWin, self).__init__(parent_win, rows, cols, x, y)

        self.win_set_title("Ekvalayzer")
    
        self.__size_bar = self.cols - 3
        self.__str_format = '{:%d}' % (self.__size_bar)
        self.init_ekv()

        self.refresh()
        #self.draw()


    def draw(self):
        self.__ekv_bar = self.__str_format.format(' ')
        
        i = 2
        j = 1
        for k in range(4):
            i = 2
            self.win.addstr(j, i, self.__ekv_bar)
            for c in self.__ekv_bar:
                # нарастает
                if self.ekv_rows[k]['is_plus'] is True:
                    # наращиваем до текущего значения
                    if i < self.ekv_rows[k]['value']:
                        self.win.addstr(j, i, c, curses.color_pair(10+j))
                    elif i == self.__size_bar -1:
                        self.ekv_rows[k]['is_plus'] = False
                    elif i == self.ekv_rows[k]['value']:
                        # увеличиваем порог
                        self.ekv_rows[k]['value'] += 1
                        break
                else:
                    # наращиваем до текущего значения
                    if i < self.ekv_rows[k]['value'] - 2:
                        self.win.addstr(j, i, c, curses.color_pair(10+j))
                    elif i == 2:
                        self.ekv_rows[k]['is_plus'] = True
                    elif i == self.ekv_rows[k]['value'] - 1:
                        # увеличиваем порог
                        self.ekv_rows[k]['value'] -= 1
                        break
                i += 1
            j += 1

        self.refresh()
        

    # инициализация псевдовизуализатора
    def init_ekv(self):
        self.ekv_rows = []
        for i in xrange(0, 4):
            r  = {
                'value': int(random.random() * 100) % (self.__size_bar-5), 
                "is_plus": True
            }
            if r['value'] == 0:
                r['value'] = 5

            # is_plus = True -- возраставет, иначе - убывает
            if r['value'] % 2 == 0: r['is_plus'] = False    
            self.ekv_rows.append(r)

        
        
"""
Отдельное окно с информацией и времени и шкалой прогресса воспроизведения
"""
class TrakDurationWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y):
        super(TrakDurationWin, self).__init__(parent_win, rows, cols, x, y)
        self.__size_bar = self.cols - 3

    def __get_time(self, current_time, total_time):
        current = time.strftime("%H:%M:%S", time.gmtime(current_time))
        total = time.strftime("%H:%M:%S", time.gmtime(total_time))
        return "%s/%s" %(current, total)


    def set_time(self, current_time, total_time):
        if total_time != 0:
            # вывожу время
            self.__str_format = '{:^%d}' % (self.__size_bar)
            self.__progres_bar = self.__str_format.format(self.__get_time(current_time, total_time))
            
            index = -1
            if current_time != 0 and total_time != 0:
                delta = float(self.__size_bar) / float(total_time)  
                index = int(current_time * delta) 

            # вывожу прогресс-бар    
            i = 0
            for c in self.__progres_bar:
                if index >= i:
                    self.win.addstr(1, i+1, c, curses.color_pair(4))
                else: 
                    self.win.addstr(1, i+1, c, curses.color_pair(5))
                i += 1
            self.refresh()

"""
Содержится картинка и информация для управления приложением. Картинка, ну - это прикольно :)
"""
class NavigationWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y):
        super(NavigationWin, self).__init__(parent_win, rows, cols, x, y)

        self.win_set_title("Help")

        self.__tmpl = '{0:16}  {1:>%d}' % (self.cols/2)
        self.win.addstr(1, 2, self.__tmpl.format('Start/Stop', '<Enter>'))
        self.win.addstr(2, 2, self.__tmpl.format('Pause', '<Space>'))
        self.win.addstr(3, 2, self.__tmpl.format('Move Up/Down', '<Up/Down>'))
        self.win.addstr(4, 2, self.__tmpl.format('Sound', '<Left/Right>'))
        self.win.addstr(5, 2, self.__tmpl.format('Seek', '<A/D>'))
        self.win.addstr(7, 2, self.__tmpl.format('Save', '<S>'))        

        """
        self.win.addstr(9, 2, "                 .88888888:. ", curses.color_pair(7))      
        self.win.addstr(10, 2, "                88888888888888.", curses.color_pair(7))      
        self.win.addstr(11, 2, "              .8888888888888888.   ", curses.color_pair(7))
        self.win.addstr(12, 2, "              888888888888888888 ", curses.color_pair(7))
        self.win.addstr(13, 2, "              88'  `88'   `88888 ", curses.color_pair(7))
        self.win.addstr(14, 2, "              88  * 88  *  88888 ", curses.color_pair(7) )
        self.win.addstr(15, 2, "              88_  _::_  _:88888 ", curses.color_pair(7))
        self.win.addstr(16, 2, "              88:::,::,:::::8888 ")
        self.win.addstr(17, 2, "              88`:::::::::'`8888 ")
        self.win.addstr(18, 2, "              88  `::::'    8:88.")
        self.win.addstr(19, 2, "            8888            `8:888. ", curses.color_pair(7))      
        self.win.addstr(20, 2, "          .8888'             `888888. " , curses.color_pair(7))
        self.win.addstr(21, 2, "         .8888:..  .::.  ...:'8888888:.", curses.color_pair(7))
        self.win.addstr(22, 2, "       .8888.'     :'     `'::`88:88888", curses.color_pair(7))
        self.win.addstr(23, 2, "      .8888        '         `.888:8888.", curses.color_pair(7))
        self.win.addstr(24, 2, "      888:8         .           888:88888 ", curses.color_pair(7))
        self.win.addstr(25, 2, "    .888:88        .:           888:88888: ", curses.color_pair(7))
        self.win.addstr(26, 2, "    8888888.       ::           88:888888 ", curses.color_pair(7))
        self.win.addstr(27, 2, "     .::.888.      ::           .88888888")
        self.win.addstr(28, 2, "    .::::::.888.    ::         :::`8888'.:.")
        self.win.addstr(29, 2, "   ::::::::::.888   '         .::::::::::::")
        self.win.addstr(30, 2, "   ::::::::::::.8    '      .:8::::::::::::.")
        self.win.addstr(31, 2, "  .::::::::::::::.        .:888:::::::::::::")
        self.win.addstr(32, 2, "  :::::::::::::::88:.__..:88888:::::::::::")
        self.win.addstr(33, 2, "     .:::::::::::88888888888.88:::::::::' ")
        self.win.addstr(34, 2, "         `':::_:' -- '' -'-' `':_::::'`")
        """

        self.win.addstr(9, 2, "                 .88888888:. ", curses.color_pair(7))      
        self.win.addstr(10, 2, "                88888888888888.", curses.color_pair(7))      
        self.win.addstr(11, 2, "              .8888888888888888.   ", curses.color_pair(7))
        self.win.addstr(12, 2, "              888888888888888888 ", curses.color_pair(7))
        self.win.addstr(13, 2, "              88'  `88'   `88888 ", curses.color_pair(7))
        
        self.win.addstr(14, 2, "              88  ", curses.color_pair(7))
        self.win.addstr(14, 20, "*", curses.color_pair(9))
        self.win.addstr(14, 22, "88  ", curses.color_pair(7))
        self.win.addstr(14, 26, "*", curses.color_pair(9))
        self.win.addstr(14, 27, "  88888 ", curses.color_pair(7) )

        self.win.addstr(15, 2, "              88_  _", curses.color_pair(7))
        self.win.addstr(15, 22, "::", curses.color_pair(8))
        self.win.addstr(15, 24, "_  _:88888 ", curses.color_pair(7))

        self.win.addstr(16, 2, "              88", curses.color_pair(7)) 
        self.win.addstr(16, 18, ":::,::,:::::", curses.color_pair(8)), 
        self.win.addstr(16, 30, "8888", curses.color_pair(7))

        self.win.addstr(17, 2, "              88", curses.color_pair(7))
        self.win.addstr(17, 18, "`:::::::::'`", curses.color_pair(8))
        self.win.addstr(17, 30, "8888 ", curses.color_pair(7))
        
        self.win.addstr(18, 2, "              88", curses.color_pair(7))
        self.win.addstr(18, 18, "  `::::'    ", curses.color_pair(8))
        self.win.addstr(18, 30, "8:88.", curses.color_pair(7))

        self.win.addstr(19, 2, "            8888            `8:888. ", curses.color_pair(7))      
        self.win.addstr(20, 2, "          .8888'             `888888. " , curses.color_pair(7))
        self.win.addstr(21, 2, "         .8888:..  .::.  ...:'8888888:.", curses.color_pair(7))
        self.win.addstr(22, 2, "       .8888.'     :'     `'::`88:88888", curses.color_pair(7))
        self.win.addstr(23, 2, "      .8888        '         `.888:8888.", curses.color_pair(7))
        self.win.addstr(24, 2, "      888:8         .           888:88888 ", curses.color_pair(7))
        self.win.addstr(25, 2, "    .888:88        .:           888:88888: ", curses.color_pair(7))
        self.win.addstr(26, 2, "    8888888.       ::           88:888888 ", curses.color_pair(7))

        self.win.addstr(27, 2, "     .::.", curses.color_pair(8))
        self.win.addstr(27, 11, "888.      ::           ", curses.color_pair(7))
        self.win.addstr(27, 34, ".", curses.color_pair(8))
        self.win.addstr(27, 35, "88888888", curses.color_pair(7))

        self.win.addstr(28, 2, "    .::::::.", curses.color_pair(8))
        self.win.addstr(28, 14, "888.    ::         ", curses.color_pair(7))
        self.win.addstr(28, 33, "::::", curses.color_pair(8))
        self.win.addstr(28, 37, "8888'", curses.color_pair(7))
        self.win.addstr(28, 41, ".:.", curses.color_pair(8))

        self.win.addstr(29, 2, "   ::::::::::.", curses.color_pair(8))
        self.win.addstr(29, 16, "888   '         ", curses.color_pair(7))
        self.win.addstr(29, 32, ".::::::::::::", curses.color_pair(8))

        self.win.addstr(30, 2, "   ::::::::::::.", curses.color_pair(8))
        self.win.addstr(30, 18, "8    '      .:8", curses.color_pair(7))
        self.win.addstr(30, 32, "::::::::::::.", curses.color_pair(8))

        self.win.addstr(31, 2, " .::::::::::::::.", curses.color_pair(8))
        self.win.addstr(31, 20, "        .:888", curses.color_pair(7))
        self.win.addstr(31, 32, ":::::::::::::", curses.color_pair(8))
        
        self.win.addstr(32, 2, "  :::::::::::::::", curses.color_pair(8))
        self.win.addstr(32, 18, "88:.__..:88888", curses.color_pair(7))
        self.win.addstr(32, 32, ":::::::::::", curses.color_pair(8))
        
        self.win.addstr(33, 2, "    .:::::::::::", curses.color_pair(8))
        self.win.addstr(33, 18, "88888888888.88", curses.color_pair(7))
        self.win.addstr(33, 33, ":::::::::' ", curses.color_pair(8))
        
        self.win.addstr(34, 2, "         `':::_:'", curses.color_pair(8))
        self.win.addstr(34, 19, "-- '' -'-' ", curses.color_pair(7))
        self.win.addstr(34, 32, "`':_::::'`", curses.color_pair(8))

        self.refresh()
"""
Список музыкальных произведений. Реализован скролинг и выбор.
"""
class TrakListWin(BaseWin):
    
    def __init__(self, parent_win, rows, cols, x, y):
        super(TrakListWin, self).__init__(parent_win, rows, cols, x, y)

        self.win_set_title("Trak list")

        self.parent = parent_win
        self.cols = cols - 3
        # Собственно сам список
        self.trak_list_pad = curses.newpad(1000, self.cols)
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

        # список жанров
        self.genres =   {
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

        tmp_cols = self.cols - 33
        self.__autor_title_size = tmp_cols/3 - 2
        self.__trak_title_size = tmp_cols - (tmp_cols/3) - 2

        #                      ->    id     Title   Author   Genre    Time        
        self.__format_str = "{0:2} {1:3} {2:%d} {3:%d} {4:18} {5:8}" % (self.__trak_title_size,
            self.__autor_title_size)

    def __get_genre_name(self, key):
        if str(key) in self.genres:
            return self.genres[str(key)]
        else:
            return 'Other'

    # добавление новых данных в список
    def add_data(self, data):
        if data is None:    return
        if len(data['items']) == 0: return

        for item in data['items']:
            # сохраняю элементы в списке
            if u'artist' in item:
                if item[u'artist'][0] == ' ':
                    item[u'artist'] = item[u'artist'][1:]
                item[u'artist'] = self.__translit(item[u'artist']).replace('  ', ' ')[0:self.__autor_title_size-1]
            else:
                item[u'artist'] = ' '

            if u'title' in item:
                if item[u'title'][0] == ' ':
                    item[u'title'] = item[u'title'][1:]
                item[u'title'] = self.__translit(item[u'title']).replace('  ', ' ')[0:self.__trak_title_size-3]
            else:
                item[u'title'] = ' '

            if u'genre_id' not in item:
                item[u'genre_id'] = '18'            
            self.data.append(item)

            # рисую стрелочку перед треком, как указатель текущей позиции "крашу" строку
            self.__ptr, self.__color = '  ', curses.color_pair(2)
            if self.count_data == 0:
                self.__ptr, self.__color = ' ', curses.color_pair(3)

            self.__rewrite_record_list_item(self.count_data,
                item, self.__color, self.__ptr)
            
            self.count_data += 1

        self.refresh()
        self.trak_list_pad.refresh(self.begin_win, 0, self.x+1, 1, self.rows+7, self.cols)

    
    """ Перерисовывает список. В зависимости от позиции курсора показывает определенную часть списка """
    def refresh(self):

        super(TrakListWin, self).refresh()
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
        
        self.trak_list_pad.refresh(self.begin_win, 0, self.x+1, 1, self.rows+7, self.cols)
            

    """ секунды в нормальное, человеческое представление """
    def __get_time(self, total_time):
        total = time.strftime("%H:%M:%S", time.gmtime(total_time))
        return "%s" %(total)

    """ перерисовываю элемент списка """
    def __rewrite_record_list_item(self, position, data_item, color, ptr):                
        #     ->      id     Title   Author   Genre    Time 
        self.trak_list_pad.addstr(position, 1, self.__format_str.format(
                ptr, 
                str(position+1), 
                data_item[u'title'],
                data_item[u'artist'],  
                self.__get_genre_name(data_item[u'genre_id']),
                self.__get_time(data_item['duration'])
            ), 
            color
        )
        

    def __translit(self, locallangstring):
        return unidecode(locallangstring)
        
    """ Перемещение указателя вверх """
    def move_up(self):
        if self.current_position > 0:
            ## отмечаю проигрываемый трек
            if self.current_position == self.select_positon:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], curses.color_pair(1), '->')
            else:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], curses.color_pair(2), '  ')

            self.current_position -= 1
            if self.current_position != self.select_positon:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], curses.color_pair(3), '  ')
                
            self.refresh()

    """ Перемещение указателя вниз """
    def move_down(self):
        if self.current_position < self.count_data - 1:
            # отмечаю проигрываемый трек
            if self.current_position == self.select_positon:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], curses.color_pair(1), '->')
            else:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], curses.color_pair(2), '  ')
                    
            self.current_position += 1
            if self.current_position != self.select_positon:
                self.__rewrite_record_list_item(self.current_position, 
                    self.data[self.current_position], curses.color_pair(3), '  ')

            self.refresh()

    """ Возвращает данные о выбранном треке """
    def select_track_get_data(self):
        # "разотмечаю" предыдущую позицию
        if self.select_positon != -1:
            self.__rewrite_record_list_item(self.select_positon, 
                    self.data[self.select_positon], curses.color_pair(2), '  ')


        self.select_positon = self.current_position
        # отмечаю новую
        self.__rewrite_record_list_item(self.select_positon, 
                self.data[self.select_positon], curses.color_pair(1), '->')

        self.refresh()
    
        return self.data[self.select_positon]


    """ переключает на след.трек,вызывается автоматически по завершению воспроизведения """
    def next_trak(self):
        if self.select_positon == self.count_data -1:
            self.select_positon = 0

        # затираю старое
        if self.select_positon != -1:
            self.__rewrite_record_list_item(self.select_positon, 
                    self.data[self.select_positon], curses.color_pair(2), '  ')


        # переписываю страку выбора, малоли-то
        self.__rewrite_record_list_item(self.current_position, 
                self.data[self.current_position], curses.color_pair(3), '  ')

        self.select_positon += 1
        # отмечаю новую
        self.__rewrite_record_list_item(self.select_positon, 
                self.data[self.select_positon], curses.color_pair(1), '->')
        self.refresh()


        return self.data[self.select_positon]



""" Реализация плеера """
class PlayerApp:
    def __init__(self):

        gobject.threads_init()
        def start():
            loop = gobject.MainLoop()
            loop.run()
        thread.start_new_thread(start, ())

        #sys.stderr.close()        

        self.__file = None
        self.player = gst.element_factory_make("playbin", "player")
        self.is_eos = False
        self.is_error = False

        self.bus = self.player.get_bus()
        self.bus.enable_sync_message_emission()


        self.bus.add_signal_watch()
        self.bus.connect("message", self._handle_message)

        self.playing  = False
        self.cached_time = False

        self.pause()

    # добавляю файл на воспроизведение
    def add_trak(self, url):

        self.__file = url
        self.player.set_state(gst.STATE_NULL)
        self.player.set_property('uri', self.__file)
        
    def pause(self):
        self.playing  = False
        self.player.set_state(gst.STATE_PAUSED)
        self.is_eos = False

    def play(self):
        if self.__file is not None:
            self.playing  = True
            self.player.set_state(gst.STATE_PLAYING)
            self.is_eos = False
            self.is_error = False

    def set_sound_volume(self, volume):
        self.player.set_property('volume', volume)

    def get_sound_volume(self):
        return self.player.get_property('volume')

    def _get_state(self):
        """Returns the current state flag of the playbin."""
        return self.player.get_state()[1]


    # возврат времени выполнения, в виде кортежа. первое число текущая позиция, второе число - общее время
    def time(self):
        if self.__file is not None:
            fmt = gst.Format(gst.FORMAT_TIME)
            try:
                pos = self.player.query_position(fmt, None)[0]/(10**9)
                length = self.player.query_duration(fmt, None)[0]/(10**9)
                self.cached_time = (pos, length)
                return (pos, length)

            except gst.QueryError:
                if self.playing and self.cached_time:
                    return self.cached_time
                else:
                    return (0, 0)

    # обработка сообщений 
    def _handle_message(self, bus, msg):
        if msg.type == gst.MESSAGE_EOS:
            self.is_eos = True
            self.player.set_state(gst.STATE_NULL)

        elif msg.type == gst.MESSAGE_ERROR:
            self.is_error = False
            self.player.set_state(gst.STATE_NULL)
            (err, debug) = msg.parse_error()
            
            sys.stderr.write("Error: %s  | %s" % (err, debug))

    # пеермещщение по записи
    def seek(self, position):
        cur_pos, cur_len = self.time()
        if position > cur_len:
            self.stop()
            return

        fmt = gst.Format(gst.FORMAT_TIME)
        ns = position * 10**9 # convert to nanoseconds
        self.player.seek_simple(fmt, gst.SEEK_FLAG_FLUSH, ns)



""" Инициализация curses, создание окон, запуск плеера в новом потоке и главный цикл приложения """
class CursesApplication:
    def __init__(self, player, vk):

        self.player = player
        self.vk = vk


        self.stdscr = curses.initscr()
        self.stdscr.clear()

        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(0)

        #screen.keypad(0);
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

        # инициализация цветовых схем
        if curses.can_change_color(): 
            init_color(-1, 0, 0, 0)
        
        # выделенный трек
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)
        # невыделенный трек
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        # отмеченный на воспроизмедение трек
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_GREEN)
        # для прогрессбара
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_YELLOW, -1)
        # заголовки окон
        curses.init_pair(6, curses.COLOR_CYAN, -1)
        # Голова и тело пигвина, черные
        curses.init_pair(7, curses.COLOR_BLUE, -1)
        curses.init_pair(8, curses.COLOR_YELLOW, -1)
        curses.init_pair(9, curses.COLOR_WHITE, -1)
        # эквалайзер
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(11, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(12, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(13, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        curses.init_pair(14, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(15, curses.COLOR_RED, curses.COLOR_RED)
        
        # получаю размеры экрана и оговариваю работу с клавиатурой
        self.stdscr.keypad(1)
        self.rows, self.cols = self.stdscr.getmaxyx()

        # Создаю главное окно. Конечно, можно было и без него обойтись, однако на будующее зазор оставлю
        self.win = curses.newwin(self.rows, self.cols, 0, 0)

        # создаю окна
        self.system_info = SystemInfoWin(self.win, 6, self.cols/5, 0, 0)
        self.trak_info = TrakInfoWin(self.win, 6, self.cols/3, 0, self.cols/5)
        self.ekvalayzer = EkvalayzerWin(self.win, 6, self.cols - self.cols/3 - self.cols/5, 0, self.cols/3 + self.cols/5)
        self.trak_duration = TrakDurationWin(self.win, 3, self.cols, 6, 0)
        self.trak_list = TrakListWin(self.win, self.rows-9, self.cols - 48, 9, 0)

        # 48 символа макс. длина. инфа статичная
        self.navigation = NavigationWin(self.win, self.rows-9, 48, 9, self.cols - 48)

        self.system_info.set_sound_volume(self.player.get_sound_volume())

        self.refresh()

    # цикл для curses и по совместительству основной цикл приложения 
    def loop(self):
        # добавляю и вывожу данные
        
        self.response = self.vk.method('audio.get', {'count':1000})
        self.trak_list.add_data(self.response)
            
        self.is_stop = False
        while self.is_stop is False:
            self.ch = self.stdscr.getch()
            # Up
            if  self.ch == 259:
                self.trak_list.move_up()
            # Down
            elif self.ch == 258:
                self.trak_list.move_down()
            # Left  ----
            elif self.ch == 260:
                sound_vol = float(self.player.get_sound_volume())
                if sound_vol > 0.01:
                    sound_vol -= float(round(float(0.05), 2))
                    if sound_vol > 0:
                        self.player.set_sound_volume(round(sound_vol,2))
                        self.system_info.set_sound_volume(self.player.get_sound_volume())
            # Right ++++
            elif self.ch == 261:
                sound_vol = float(self.player.get_sound_volume())
                if sound_vol < 1:
                    sound_vol += float(round(float(0.05), 2))
                    if sound_vol < 100:
                        self.player.set_sound_volume(round(sound_vol,2))
                        self.system_info.set_sound_volume(self.player.get_sound_volume())
            # Enter
            elif self.ch == 10:
                trak_data = self.trak_list.select_track_get_data()
                self.player.pause()
                self.player.add_trak(trak_data['url'])
                self.player.play()
                self.system_info.set_status_playning()
                self.trak_info.set_data(trak_data)
            # Space
            elif self.ch == 32:
                if self.player.playing == True:
                    self.system_info.set_status_paused()        
                    self.player.pause()
                else:
                    self.system_info.set_status_playning()
                    self.player.play()
            # Q/q
            elif self.ch == 113 or self.ch == 81:
                self.is_stop = True
            # Key D/d seeek -->
            elif self.ch == 100 or self.ch == 68:
                tm = self.player.time()
                if tm is not None:
                    cur, total = tm
                    if total != 0:
                        if cur + PG_SEEK_TIME < total:
                            self.player.seek(cur + PG_SEEK_TIME)
                        else:
                            self.player.seek(total-1)
            # Key A,a seek <----
            elif self.ch == 97 or self.ch == 65:
                tm = self.player.time()
                if tm is not None:
                    cur, total = tm
                    if total != 0:
                        if cur - PG_SEEK_TIME > 0:
                            self.player.seek(cur - PG_SEEK_TIME)
                        else:
                            self.player.seek(0)
            else:
                self.refresh()
            #else:
            #    print self.ch
    # выполняет обновление данных приложения
    def update_data(self):
        # эквалайзер
        # прогресс-бар и время
        tm = self.player.time()
        if tm is not None:
            current_time, total_time = tm
            self.trak_duration.set_time(current_time, total_time)
        
        # след.трек, т.к. закончился текущий
        if self.player.is_eos:
            trak_data = self.trak_list.next_trak()
            self.player.pause()
            self.player.add_trak(trak_data['url'])
            self.player.play()
            
            self.system_info.set_status_playning()
            self.trak_info.set_data(trak_data)
        #
        #произошла ошибка, перерисовать все
        #if self.player.is_error:
        #    self.refresh()


    # обновление экрана и всех окон
    def refresh(self):
        #return
        self.stdscr.refresh()
        self.win.refresh()
        self.system_info.refresh()
        self.trak_info.refresh()
        self.trak_duration.refresh()
        self.trak_list.refresh()
        self.navigation.refresh()



""" выполняет обновления прогресс-бара """
class ClockThread(threading.Thread):
    def __init__(self, curses_app):
        threading.Thread.__init__(self)
        self.daemon = True
        self.curses_app = curses_app

    def run(self):
        while True:
            try:
                time.sleep(TIME_SLEEP)
                self.curses_app.update_data()
            except:
                pass


""" Производит инициализация curses и gstreamer """
class Application:
    def __init__(self):
        
        #sys.stderr.close()

        self.vk = None
        
        self.vk = vk_api.VkApi(login=login, password=password)

        try:
            self.vk.authorization()
        except vk_api.AuthorizationError as error_msg:
            print "The password/login you entered is incorrect"
            return

        self.play = PlayerApp()
        self.ca = CursesApplication(self.play, self.vk)

        clock = ClockThread(self.ca)
        clock.start()


    def run(self):
        self.ca.loop()


if __name__ == '__main__':
    sys.stdout.write('Login: ')
    login = raw_input()
    
    password = getpass.getpass()

    app = Application()
    app.run()

    curses.endwin()