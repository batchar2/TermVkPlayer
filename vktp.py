# -*- coding: utf-8 -*-
import sys
import getpass
import locale
import threading
import time

import curses
import vk_api



# импорт ui
from ui.win_navigation import NavigationWin
from ui.win_progressbar import ProgressBarWin
from ui.win_sysinfo import SystemInfoWin
from ui.win_trackinfo import TrackInfoWin
from ui.win_tracklist import TrackListWin
from ui.win_alboms import AlbomsWin
# импорт "плеера"
from player.gst_player import PlayerApp

locale.setlocale(locale.LC_ALL,"")

PG_NAME = "TermVkPlayer"
PG_VERSION = "v0.01"
TIME_SLEEP = 0.3
PG_SEEK_TIME = 30

login, password = 'skokov1992@mail.ru', 'putinvvico'


""" Инициализация curses, создание окон, запуск плеера в новом потоке и главный цикл приложения """
class CursesApplication:
    KEY_ENTER = 10
    KEY_SPACE = 32
    KEY_d, KEY_D = 100, 68
    KEY_q, KEY_Q = 113, 81
    KEY_a, KEY_A = 97, 65
    KEY_UP = 259
    KEY_DOWN = 258 
    KEY_RIGHT = 261
    KEY_LEFT = 260

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


        #curses.slk_set(1, "Test1", 1)
        #curses.slk_set(2, "Test2", 1)
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

        # создаю окна
        self.system_info = SystemInfoWin(self.win, 6, self.cols/5, 0, 0, PG_NAME, PG_VERSION, COLOR_CONTENT)
        self.track_info = TrackInfoWin(self.win, 6, self.cols/3, 0, self.cols/5, COLOR_CONTENT)
        #self.ekvalayzer = EkvalayzerWin(self.win, 6, self.cols - self.cols/3 - self.cols/5, 0, self.cols/3 + self.cols/5)
        self.track_duration = ProgressBarWin(self.win, 3, self.cols, 6, 0, COLOR_PGBAR_PLAYNING, COLOR_PGBAR_FREE)
        self.track_list = TrackListWin(self.win, self.rows-9, self.cols - 48, 9, 0,
                                        TRACK_SELECT_COLOR, TRAK_ITEM_COLOR, TRACK_PLAY_COLOR)

        # 48 символа макс. длина. инфа статичная
        #self.navigation = NavigationWin(self.win, self.rows-9, 48, 9, self.cols - 48, TUX_COLOR_BLUE,
        #                                 TUX_COLOR_YELLOW, TUX_COLOR_WHILE)

        self.alboms_win = AlbomsWin(self.win, self.rows-9, 48, 9, self.cols - 48,
                                        TRACK_SELECT_COLOR, TRAK_ITEM_COLOR, TRACK_PLAY_COLOR)


        self.system_info.set_sound_volume(self.player.get_sound_volume())

        self.refresh()

    # цикл для curses и по совместительству основной цикл приложения 
    def loop(self):
        # добавляю и вывожу данные
        #self.all_traks = self.vk.method('audio.get', {'count':2000})
        #self.track_list.set_data(self.all_traks)
        #self.track_list.show_data()

        self.all_alboms = self.vk.method('audio.getAlbums', {'count':100})
        self.alboms_win.set_data(self.all_alboms)
        self.alboms_win.show_data()
        

        self.is_stop = False
        
        while self.is_stop is False:
            self.ch = self.stdscr.getch()
            # Up
            if  self.ch == self.KEY_UP:#259:
                self.track_list.move_up()
            # Down
            elif self.ch == self.KEY_DOWN:#258:
                self.track_list.move_down()
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
                track = self.track_list.select_track_get_data()
                self.player.pause()
                self.player.add_track(track.get_url())
                self.player.play()
                self.system_info.set_status_playning()
                self.track_info.set_data(track)
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
                        if cur + PG_SEEK_TIME < total:
                            self.player.seek(cur + PG_SEEK_TIME)
                        else:
                            self.player.seek(total-1)
            # Key A,a seek <----
            elif self.ch == self.KEY_A or self.ch == self.KEY_a:
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
            self.player.add_track(track.get_url())
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
#        self.navigation.refresh()



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

        self.vk = vk_api.VkApi(login=login, password=password)

        try:
            self.vk.authorization()
        except vk_api.AuthorizationError as error_msg:
            print "The password/login you entered is incorrect"
            return

        # устанавливаю плеер, запускается в отдельном потоке
        self.play = PlayerApp()
        # стартую ui
        self.ca = CursesApplication(self.play, self.vk)
        # стартую отдельный поток, для генерации событий, т.к. не работают с ncurses сигналы. ХЗ почему. Странно очень
        clock = ClockThread(self.ca)
        clock.start()

    def run(self):
        self.ca.loop()


if __name__ == '__main__':
#    sys.stdout.write('Login: ')
#    login = raw_input()    
#    password = getpass.getpass()

    app = Application()
    app.run()

    curses.endwin()
