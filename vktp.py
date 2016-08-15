# -*- coding: utf-8 -*-
import sys
import getpass
import locale
import threading
import time

import curses

from abc import ABCMeta, abstractmethod

# импорт ui
from ui.win_navigation import NavigationWin
from ui.win_progressbar import ProgressBarWin
from ui.win_sysinfo import SystemInfoWin
from ui.win_trackinfo import TrackInfoWin
from ui.win_tracklist import TrackListWin
from ui.win_alboms import AlbomsWin
from ui.label_slk import LabelSlk

from ui.win_login import LoginWin

# импорт "плеера"
from player.gst_player import PlayerApp


from storage.storage import Storage 

# переделать
from command.command import CursesApplicationInterface

locale.setlocale(locale.LC_ALL,"")

PG_NAME = "TermVkPlayer"
PG_VERSION = "v0.01"
TIME_SLEEP = 0.3
PG_SEEK_TIME = 30

""" Инициализация и хранение стилей приложения """
class CursesProperty(object):
    
    """ Инициализация ncurses, инициализация терминала """
    def initscr(self):
        self.stdscr = curses.initscr()
        self.stdscr.clear()

        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(0)

        #screen.keypad(0);
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

         # получаю размеры экрана и оговариваю работу с клавиатурой
        self.stdscr.keypad(1)
        self.rows, self.cols = self.stdscr.getmaxyx()

        # Создаю главное окно. Конечно, можно было и без него обойтись, однако на будующее зазор оставлю
        self._win_general = curses.newwin(self.rows, self.cols, 0, 0)
    
    """ Возврат указателя на главное окно, на главном окне выводятся все остальные подокна """
    @property
    def screen(self):
        return self._win_general

    #def refresh():
    #   self.stdscr.refresh()
    #    return self.stdscr

    #def getch():
    #    return self.stdscr.getch()

    """ Инициализация цветов """
    def initclr(self):
        # инициализация цветовых схем
        if curses.can_change_color(): 
            init_color(-1, 0, 0, 0)
        # отмеченный на воспроизмедение трек
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)
        # невыделенный трек
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        # выделенный трек
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
        # slc
        curses.init_pair(16, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(17, curses.COLOR_WHITE, -1)

        self.TRACK_PLAY_COLOR = curses.color_pair(1)
        self.TRAK_ITEM_COLOR = curses.color_pair(2)
        self.TRACK_SELECT_COLOR = curses.color_pair(3)

        self.COLOR_CONTENT = curses.color_pair(6)

        self.COLOR_PGBAR_PLAYNING = curses.color_pair(4)
        self.COLOR_PGBAR_FREE = curses.color_pair(5)

        self.TUX_COLOR_BLUE = curses.color_pair(7)
        self.TUX_COLOR_YELLOW = curses.color_pair(8)
        self.TUX_COLOR_WHILE = curses.color_pair(9)

        self.ALBOM_PLAY_COLOR = curses.color_pair(8)
        self.ALBOM_ITEM_COLOR = curses.color_pair(6)
        self.ALBOM_SELECT_COLOR = curses.color_pair(9)

        # цвет текса и цвет номера команды
        self.COLOR_SLC = curses.color_pair(16)
        self.COLOR_NUMBER = curses.color_pair(17)


""" Инициализация curses, создание окон, запуск плеера в новом потоке и главный цикл приложения """
class CursesApplication(object):
    
    """ Список кнопок и их обработчиков """
    """
    keys_cmd = [
        {"key_number" : 9, "cmd_name": "_key_tab", "title": "KEY_TAB"},
        {"key_number" : 10, "cmd_name": "_enter", "title": "KEY_ENTER"},
        {"key_number" : 32, "cmd_name": "_space", "title": "KEY_SPACE"},
        {"key_number" : 100, "cmd_name": "_key_d", "title": "KEY_d"},
        {"key_number" : 68, "cmd_name": "_key_d", "title": "KEY_D"},
        {"key_number" : 113, "cmd_name": "_key_q", "title": "KEY_q"},
        {"key_number" : 68, "cmd_name": "_key_q", "title": "KEY_Q"},
        {"key_number" : 97, "cmd_name": "_key_a", "title": "KEY_a"},
        {"key_number" : 65, "cmd_name": "_key_a", "title": "KEY_A"},
        {"key_number" : 259, "cmd_name": "_up", "title": "KEY_UP"},
        {"key_number" : 258, "cmd_name": "_down", "title": "KEY_DOWN"},

        {"key_number" : 261, "cmd_name": "_right", "title": "KEY_RIGHT"},
        {"key_number" : 260, "cmd_name": "_left", "title": "KEY_LEFT"},
        {"key_number" : 265, "cmd_name": "_f1", "title": "KEY_F1"},
    ]
    """

    def __init__(self):
    #def __init__(self , player, vk):
        global PG_NAME, PG_VERSION

        #self.player = player
        #self.vk = vk

        # штшциализирую ncurses
        self.curses_property = CursesProperty()
        self.curses_property.initscr()
        self.curses_property.initclr()

        # если отображается ui плеера
        self.is_view_ui_player = False

        self.win = self.curses_property.screen
        self.rows = self.curses_property.rows
        self.cols = self.curses_property.cols

        #self.__view_ui_player()


    def view_login_form(self):
        """ Переделать на команду """
        #login = LoginWin(self.win, 10, 20, self.rows/2, self.cols/2)
        self.login = LoginWin(self.win, self.rows/2 - 10, self.rows/2 - 20, self.rows/2, self.cols/2, self.curses_property.COLOR_NUMBER)

    def __view_ui_player(self):
        # выбрана левая панель с треками
        self.is_select_trak_list = True 
        # отображать список альбомов
        self.is_view_albom_list = True
        
        

        self.__help_f1 = LabelSlk(0, self.win, (self.rows, self.cols,),  u"Help", 
                                    self.curses_property.COLOR_SLC, self.curses_property.COLOR_NUMBER)
        self.__edit_f2 = LabelSlk(1, self.win, (self.rows, self.cols,),  u"Edit", 
                                    self.curses_property.COLOR_SLC, self.curses_property.COLOR_NUMBER)

        self.__copy_f3 = LabelSlk(2, self.win, (self.rows, self.cols,),  u"Copy", 
                                    self.curses_property.COLOR_SLC, self.curses_property.COLOR_NUMBER)

        self.__move_f4 = LabelSlk(3, self.win, (self.rows, self.cols,),  u"Move", 
                                    self.curses_property.COLOR_SLC, self.curses_property.COLOR_NUMBER)
        self.__newalbom_f5 = LabelSlk(4, self.win, (self.rows, self.cols,),  u"NewAlbum", 
                                    self.curses_property.COLOR_SLC, self.curses_property.COLOR_NUMBER)
        self.__rm_f6 = LabelSlk(5, self.win, (self.rows, self.cols,),  u"Remove", 
                                    self.curses_property.COLOR_SLC, self.curses_property.COLOR_NUMBER)
        self.__random_f7 = LabelSlk(6, self.win, (self.rows, self.cols,),  u"Random", 
                                        self.curses_property.COLOR_SLC, self.curses_property.COLOR_NUMBER)
        self.__move_exit = LabelSlk(7, self.win, (self.rows, self.cols,),  u"Exit", 
                                        self.curses_property.COLOR_SLC, self.curses_property.COLOR_NUMBER)

        # создаю окна
        self.system_info = SystemInfoWin(self.win, 6, self.cols/5, 0, 0, 
                                            PG_NAME, PG_VERSION, self.curses_property.COLOR_CONTENT)
        self.track_info = TrackInfoWin(self.win, 6, self.cols/3, 0, self.cols/5, self.curses_property.COLOR_CONTENT)
        #self.ekvalayzer = EkvalayzerWin(self.win, 6, self.cols - self.cols/3 - self.cols/5, 0, self.cols/3 + self.cols/5)
        self.track_duration = ProgressBarWin(self.win, 3, self.cols, 6, 0, 
                                                self.curses_property.COLOR_PGBAR_PLAYNING, self.curses_property.COLOR_PGBAR_FREE)
        
        self.track_list = TrackListWin(self.win, self.rows-10, self.cols - 48, 9, 0,
                                            self.curses_property.TRACK_SELECT_COLOR, self.curses_property.TRAK_ITEM_COLOR, self.curses_property.TRACK_PLAY_COLOR)

        # 48 символа макс. длина. инфа статичная
        self.navigation = NavigationWin(self.win, self.rows-10, 48, 9, self.cols - 48, self.curses_property.TUX_COLOR_BLUE,
                                            self.curses_property.TUX_COLOR_YELLOW, self.curses_property.TUX_COLOR_WHILE)

        self.alboms_win = AlbomsWin(self.win, self.rows-10, 48, 9, self.cols - 48, self.cols,
                                        self.curses_property.ALBOM_SELECT_COLOR, self.curses_property.ALBOM_ITEM_COLOR, self.curses_property.ALBOM_PLAY_COLOR)


        self.system_info.set_sound_volume(self.player.get_sound_volume())

        self.refresh()

    """ Пасринг команд от пользователя. Сопоставление с объявленными командами """
    """
    def get_command(self):
        ch = self.curses_property.stdscr.getch()
        for cmd in self.keys_cmd:
            if ch == cmd["key_number"]:
                return cmd["cmd_name"]
        return None
    """

    """ Переместить вверх """
    """
    def _up(self):
        if self.is_select_trak_list is True:
            self.track_list.move_up()
        elif self.is_view_albom_list is True:
            self.alboms_win.move_up()
    """
    """ Переместить вниз """
    """
    def _down(self):
        if self.is_select_trak_list is True:
            self.track_list.move_down()
        elif self.is_view_albom_list is True:
            self.alboms_win.move_down()
    """
    """ Уменьшаю громкость 
    def _left(self):
        sound_vol = float(self.player.get_sound_volume())
        if sound_vol > 0.01:
            sound_vol -= float(round(float(0.05), 2))
            if sound_vol > 0:
                self.player.set_sound_volume(round(sound_vol,2))
                self.system_info.set_sound_volume(self.player.get_sound_volume())

    Увеличиваю громкость 
    def _right(self):
        sound_vol = float(self.player.get_sound_volume())
        if sound_vol < 1:
            sound_vol += float(round(float(0.05), 2))
            if sound_vol < 100:
                self.player.set_sound_volume(round(sound_vol,2))
                self.system_info.set_sound_volume(self.player.get_sound_volume())


    Выбор трека для воспроизведения 
    def _enter(self):
        if self.is_select_trak_list is True:
            track = self.track_list.get_select_data()
            self.player.pause()
            self.player.add_track(track.url)
            self.player.play()
            self.system_info.set_status_playning()
            self.track_info.set_data(track)
        elif self.is_view_albom_list is True:
            albom = self.alboms_win.get_select_data()
            self.vk.load_traks()
            # отображаю все песни
            if albom.id is not None:
                self.vk.load_traks(albom.id)
            else:
                self.vk.load_traks()

            self.track_list.set_data(self.vk.tracks)
            self.track_list.show()
            self.track_list.hide_cursor()


    Поставить/снять с паузы 
    def _space(self):
        if self.player.playing == True:
                self.system_info.set_status_paused()        
                self.player.pause()
        else:
            self.system_info.set_status_playning()
            self.player.play()


    def _key_q(self):
        self.is_stop = True


    Промотать вперед
    def _key_d(self):
        tm = self.player.time()
        if tm is not None:
            cur, total = tm
            if total != 0:
                self.player.pause()
                if cur + PG_SEEK_TIME < total:
                    self.player.seek(cur + PG_SEEK_TIME)
                else:
                    self.player.seek(total-1)
                self.player.play()


    Промотать назад
    def _key_a(self):
        tm = self.player.time()
        if tm is not None:
            cur, total = tm
            if total != 0:
                self.player.pause()
                if cur - PG_SEEK_TIME > 0:
                    self.player.seek(cur - PG_SEEK_TIME)
                else:
                    self.player.seek(0)
                self.player.play()


    TAB - переключить.  
    def _key_tab(self):
        # при выборе "пингвина" TAB не будет работать
        #if self.is_view_albom_list is False:
        if self.is_select_trak_list is True:
            self.track_list.hide_cursor()
            self.alboms_win.show_cursor()
        else:
            self.track_list.show_cursor()
            self.alboms_win.hide_cursor()

        self.is_select_trak_list = not self.is_select_trak_list


    def _key_f1(self):
        if self.is_view_albom_list is True:
            self.is_view_albom_list = False
            self.is_select_trak_list = False        
        else:
            self.is_view_albom_list = True

        self.is_select_trak_list = True
        self.refresh()

    """

    """ Загрузка данных """
    def __load_data(self):
         # добавляю и вывожу данные
        self.vk.load_traks()
        self.vk.load_alboms()

        self.track_list.set_data(self.vk.tracks)
        self.track_list.show()

        self.alboms_win.set_data(self.vk.alboms)
        self.alboms_win.show()
        
        # отмечаю альбом проигрываемый
        self.alboms_win.get_select_data()

    
    """ Выполняет обновление данных приложения """
    def update_data(self):
        # прогресс-бар и время
        tm = self.player.time()
        if tm is not None:
            current_time, total_time = tm
            self.track_duration.set_time(current_time, total_time)
        # след.трек, т.к. закончился текущий
        if self.player.is_eos:
            track = self.track_list.next_track()
            self.player.add_track(track.url)
            self.player.play()
            self.system_info.set_status_playning()
            self.track_info.set_data(track)
        

    """ Обновление экрана и всех окон """
    def refresh(self):
        #return
        self.curses_property.stdscr.refresh()
        self.win.refresh()
        
        self.system_info.refresh()
        self.track_info.refresh()
        self.track_duration.refresh()
        self.track_list.refresh()

        self.__help_f1.refresh()
        self.__edit_f2.refresh()
        self.__copy_f3.refresh()
        self.__move_f4.refresh()

        self.__newalbom_f5.refresh()
        self.__rm_f6.refresh()
        self.__random_f7.refresh()
        self.__move_exit.refresh()

        if self.is_view_albom_list is True:
            #pass
            self.alboms_win.refresh()
        else:
            self.navigation.refresh()

    """ Цикл для curses и по совместительству основной цикл приложения  """
    """
    def loop(self):
        self.__load_data()        
        #self.__is_view_ui_player = False
        #self.view_ui_player()
        
        login = LoginWin(self.win, 10, 20, self.rows/2, self.cols/2)
       
        self.is_stop = False
        
        while self.is_stop is False:
            #if True:
            try:
                command = self.get_command()
                if command is not None:
                    #pass
                    #print command
                    # выполняю команду
                    getattr(self, command)()
                    #print f
            except AttributeError as e:
                print e
    """        


class ClockThread(threading.Thread):
    """ 
    Выполняет обновления прогресс-бара. Костыль возник из-за бага, 
    когда приложение с ncurses не может обрабатывать сигналы 
    """
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

    """ Список кнопок и их обработчиков """
    keys_cmd = [
        {"key_number" : 9, "cmd_name": "key_tab", "title": "KEY_TAB"},
        {"key_number" : 10, "cmd_name": "key_enter", "title": "KEY_ENTER"},
        {"key_number" : 32, "cmd_name": "key_space", "title": "KEY_SPACE"},
        {"key_number" : 100, "cmd_name": "key_d", "title": "KEY_d"},
        {"key_number" : 68, "cmd_name": "key_d", "title": "KEY_D"},
        {"key_number" : 113, "cmd_name": "key_q", "title": "KEY_q"},
        {"key_number" : 68, "cmd_name": "key_q", "title": "KEY_Q"},
        {"key_number" : 97, "cmd_name": "key_a", "title": "KEY_a"},
        {"key_number" : 65, "cmd_name": "key_a", "title": "KEY_A"},
        {"key_number" : 259, "cmd_name": "key_up", "title": "KEY_UP"},
        {"key_number" : 258, "cmd_name": "key_down", "title": "KEY_DOWN"},

        {"key_number" : 261, "cmd_name": "key_right", "title": "KEY_RIGHT"},
        {"key_number" : 260, "cmd_name": "key_left", "title": "KEY_LEFT"},
        {"key_number" : 265, "cmd_name": "key_f1", "title": "KEY_F1"},
    ]

    def __init__(self):
        # 1. Создать пользовательский интерфейс
        # 2. Получить объект vk
        # 3. Авторизоваться
        # 4. Загрузить плейлисты и треки
        # 5. Работать в штатном режиме
        self.is_stop = False
        self._is_login = False
        # стартую ui
        self.curses_app = CursesApplication()
        # обработка комманд для приложения, через паттерн комманда
        self.command_interface = CursesApplicationInterface(self.curses_app)

        return
        # получаю доступ к вк
        vk = Storage(login, password, 'VK').get()

        r, msg = vk.login()
        if r is False:
            print msg
            sys.exit(1)

        # устанавливаю плеер, запускается в отдельном потоке
        self.play = PlayerApp()
        # стартую ui
        # обработка комманд для приложения, через паттерн комманда
        #self.command_interface = CursesApplicationInterface(self.curses_app)

        # стартую отдельный поток, для генерации событий, т.к. не работают с ncurses сигналы. ХЗ почему. Странно очень
        clock = ClockThread(self.ca)
        clock.start()
    
    def _get_command(self):
        ch = self.curses_app.curses_property.stdscr.getch()
        for cmd in self.keys_cmd:
            if ch == cmd["key_number"]:
                return cmd["cmd_name"]
        return None

    def loop(self):
        while self.is_stop is False:
            #if True:
            try:
                # вывожу окно для ввода логина и пароля
                if self._is_login is False:
                    self.curses_app.view_login_form()
                else:
                    command_name = self._get_command()
                    if command_name is not None:
                        # выполняю команду
                        print command_name
                        getattr(self.command_interface, command_name)()
                        #print f
            except AttributeError as e:
                print e
    
        #self.ca.loop()



if __name__ == '__main__':
    
    #вывожу окно логина
    #login = LoginWin(curses_property.screen, 10, 20, curses_property.rows/2, curses_property.cols/2, curses_property.ALBOM_PLAY_COLOR)
    
    #sys.stdout.write('Login: ')
    #login = raw_input()    
    #password = getpass.getpass()
    login = "skokov1992@mail.ru"
    password = "putinvvico24"

    app = Application()
    app.loop()

    curses.endwin()
