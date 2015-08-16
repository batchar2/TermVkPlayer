# -*- coding: utf-8 -*-
import sys
import getpass
import locale
import threading
import time

import curses

# импорт ui
from ui.win_navigation import NavigationWin
from ui.win_progressbar import ProgressBarWin
from ui.win_sysinfo import SystemInfoWin
from ui.win_trackinfo import TrackInfoWin
from ui.win_tracklist import TrackListWin
from ui.win_alboms import AlbomsWin
from ui.label_slk import LabelSlk
# импорт "плеера"
from player.gst_player import PlayerApp


from storage.storage import Storage 

locale.setlocale(locale.LC_ALL,"")

PG_NAME = "TermVkPlayer"
PG_VERSION = "v0.01"
TIME_SLEEP = 0.3
PG_SEEK_TIME = 30





""" Инициализация curses, создание окон, запуск плеера в новом потоке и главный цикл приложения """
class CursesApplication(object):
    KEY_ENTER = 10
    KEY_SPACE = 32
    KEY_d, KEY_D = 100, 68
    KEY_q, KEY_Q = 113, 81
    KEY_a, KEY_A = 97, 65
    KEY_UP = 259
    KEY_DOWN = 258 
    KEY_RIGHT = 261
    KEY_LEFT = 260
    KEY_F1 = 265

    def __init__(self, player, vk):
        global PG_NAME, PG_VERSION

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

        # получаю размеры экрана и оговариваю работу с клавиатурой
        self.stdscr.keypad(1)
        self.rows, self.cols = self.stdscr.getmaxyx()

        # Создаю главное окно. Конечно, можно было и без него обойтись, однако на будующее зазор оставлю
        self.win = curses.newwin(self.rows, self.cols, 0, 0)

        TRACK_PLAY_COLOR = curses.color_pair(1)
        TRAK_ITEM_COLOR = curses.color_pair(2)
        TRACK_SELECT_COLOR = curses.color_pair(3)

        COLOR_CONTENT = curses.color_pair(6)

        COLOR_PGBAR_PLAYNING = curses.color_pair(4)
        COLOR_PGBAR_FREE = curses.color_pair(5)

        TUX_COLOR_BLUE = curses.color_pair(7)
        TUX_COLOR_YELLOW = curses.color_pair(8)
        TUX_COLOR_WHILE = curses.color_pair(9)


        ALBOM_PLAY_COLOR = curses.color_pair(8)
        ALBOM_ITEM_COLOR = curses.color_pair(6)
        ALBOM_SELECT_COLOR = curses.color_pair(9)

        # цвет текса и цвет номера команды
        COLOR_SLC = curses.color_pair(16)
        COLOR_NUMBER = curses.color_pair(17)

        # выбрана левая панель с треками
        self.is_select_trak_list = True 
        # отображать список альбомов
        self.is_view_albom_list = True
        self.player = player
        self.vk = vk

        self.__help_f1 = LabelSlk(0, self.win, (self.rows, self.cols,),  u"Help", COLOR_SLC, COLOR_NUMBER)
        self.__edit_f2 = LabelSlk(1, self.win, (self.rows, self.cols,),  u"Edit", COLOR_SLC, COLOR_NUMBER)
        self.__copy_f3 = LabelSlk(2, self.win, (self.rows, self.cols,),  u"Copy", COLOR_SLC, COLOR_NUMBER)
        self.__move_f4 = LabelSlk(3, self.win, (self.rows, self.cols,),  u"Move", COLOR_SLC, COLOR_NUMBER)
        self.__newalbom_f5 = LabelSlk(4, self.win, (self.rows, self.cols,),  u"NewAlbum", COLOR_SLC, COLOR_NUMBER)
        self.__rm_f6 = LabelSlk(5, self.win, (self.rows, self.cols,),  u"Remove", COLOR_SLC, COLOR_NUMBER)
        self.__random_f7 = LabelSlk(6, self.win, (self.rows, self.cols,),  u"Random", COLOR_SLC, COLOR_NUMBER)
        self.__move_exit = LabelSlk(7, self.win, (self.rows, self.cols,),  u"Exit", COLOR_SLC, COLOR_NUMBER)

        # создаю окна
        self.system_info = SystemInfoWin(self.win, 6, self.cols/5, 0, 0, 
                                            PG_NAME, PG_VERSION, COLOR_CONTENT)
        self.track_info = TrackInfoWin(self.win, 6, self.cols/3, 0, self.cols/5, COLOR_CONTENT)
        #self.ekvalayzer = EkvalayzerWin(self.win, 6, self.cols - self.cols/3 - self.cols/5, 0, self.cols/3 + self.cols/5)
        self.track_duration = ProgressBarWin(self.win, 3, self.cols, 6, 0, COLOR_PGBAR_PLAYNING, COLOR_PGBAR_FREE)
        
        self.track_list = TrackListWin(self.win, self.rows-10, self.cols - 48, 9, 0,
                                        TRACK_SELECT_COLOR, TRAK_ITEM_COLOR, TRACK_PLAY_COLOR)

        # 48 символа макс. длина. инфа статичная
        self.navigation = NavigationWin(self.win, self.rows-10, 48, 9, self.cols - 48, TUX_COLOR_BLUE,
                                         TUX_COLOR_YELLOW, TUX_COLOR_WHILE)

        self.alboms_win = AlbomsWin(self.win, self.rows-10, 48, 9, self.cols - 48, self.cols,
                                        ALBOM_SELECT_COLOR, ALBOM_ITEM_COLOR, ALBOM_PLAY_COLOR)


        self.system_info.set_sound_volume(self.player.get_sound_volume())

        self.refresh()

    # цикл для curses и по совместительству основной цикл приложения 
    def loop(self):
        # добавляю и вывожу данные
        self.vk.load_traks()
        self.vk.load_alboms()

        self.track_list.set_data(self.vk.tracks)
        self.track_list.show()

        self.alboms_win.set_data(self.vk.alboms)
        self.alboms_win.show()
        
        # отмечаю альбом проигрываемый
        self.alboms_win.get_select_data()

        self.is_stop = False
        
        while self.is_stop is False:
            self.ch = self.stdscr.getch()
            # Up
            if  self.ch == self.KEY_UP:#259:
                if self.is_select_trak_list is True:
                    self.track_list.move_up()
                else:
                    self.alboms_win.move_up()
            # Down
            elif self.ch == self.KEY_DOWN:#258:
                if self.is_select_trak_list is True:
                    self.track_list.move_down()
                else:
                    self.alboms_win.move_down()
            # Left  ----
            elif self.ch == self.KEY_LEFT:#260:
                sound_vol = float(self.player.get_sound_volume())
                if sound_vol > 0.01:
                    sound_vol -= float(round(float(0.05), 2))
                    if sound_vol > 0:
                        self.player.set_sound_volume(round(sound_vol,2))
                        self.system_info.set_sound_volume(self.player.get_sound_volume())
            # Right ++++
            elif self.ch == self.KEY_RIGHT:#261:
                sound_vol = float(self.player.get_sound_volume())
                if sound_vol < 1:
                    sound_vol += float(round(float(0.05), 2))
                    if sound_vol < 100:
                        self.player.set_sound_volume(round(sound_vol,2))
                        self.system_info.set_sound_volume(self.player.get_sound_volume())
            # Enter
            elif self.ch == self.KEY_ENTER:#10:
                if self.is_select_trak_list is True:
                    track = self.track_list.get_select_data()
                    self.player.pause()
                    self.player.add_track(track.url)
                    self.player.play()
                    self.system_info.set_status_playning()
                    self.track_info.set_data(track)
                else:
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
            # Space
            elif self.ch == self.KEY_SPACE:#32:
                if self.player.playing == True:
                    self.system_info.set_status_paused()        
                    self.player.pause()
                else:
                    self.system_info.set_status_playning()
                    self.player.play()
            # Q/q
            elif self.ch == self.KEY_Q or self.ch == self.KEY_q:
                self.is_stop = True
            # Key D/d seeek -->
            elif self.ch == self.KEY_D or self.ch == self.KEY_d:
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
            # Key A,a seek <----
            elif self.ch == self.KEY_A or self.ch == self.KEY_a:
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
            # TAB
            elif self.ch == 9:
                if self.is_select_trak_list is True:
                    self.track_list.hide_cursor()
                    self.alboms_win.show_cursor()
                else:
                    self.track_list.show_cursor()
                    self.alboms_win.hide_cursor()

                self.is_select_trak_list = not self.is_select_trak_list
                #print '!!!!!!!!!!!!!!'
            elif self.ch == self.KEY_F1:
                if self.is_view_albom_list is True:
                    self.is_view_albom_list = False
                else:
                    self.is_view_albom_list = True
                self.refresh()
            else:
                pass
                #print self.ch
                #self.refresh()
    
    # выполняет обновление данных приложения
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

        if self.is_view_albom_list is False:
            self.navigation.refresh()
        else:
            self.alboms_win.refresh()


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
    def __init__(self):

        # получаю доступ к вк
        vk = Storage(login, password, 'VK').get()

        r, msg = vk.login()
        if r is False:
            print msg
            sys.exit(1)

        # устанавливаю плеер, запускается в отдельном потоке
        self.play = PlayerApp()
        # стартую ui
        self.ca = CursesApplication(self.play, vk)
        # стартую отдельный поток, для генерации событий, т.к. не работают с ncurses сигналы. ХЗ почему. Странно очень
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
