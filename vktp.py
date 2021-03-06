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
    
    keys_cmd = [
        {"key_number" : 9, "cmd_name": "key_tab", "title": "KEY_TAB"},
        {"key_number" : 10, "cmd_name": "enter", "title": "KEY_ENTER"},
        {"key_number" : 32, "cmd_name": "space", "title": "KEY_SPACE"},
        {"key_number" : 100, "cmd_name": "key_d", "title": "KEY_d"},
        {"key_number" : 68, "cmd_name": "key_d", "title": "KEY_D"},
        {"key_number" : 113, "cmd_name": "key_q", "title": "KEY_q"},
        {"key_number" : 68, "cmd_name": "key_q", "title": "KEY_Q"},
        {"key_number" : 97, "cmd_name": "key_a", "title": "KEY_a"},
        {"key_number" : 65, "cmd_name": "key_a", "title": "KEY_A"},
        {"key_number" : 259, "cmd_name": "up", "title": "KEY_UP"},
        {"key_number" : 258, "cmd_name": "down", "title": "KEY_DOWN"},

        {"key_number" : 261, "cmd_name": "right", "title": "KEY_RIGHT"},
        {"key_number" : 260, "cmd_name": "left", "title": "KEY_LEFT"},
        {"key_number" : 265, "cmd_name": "f1", "title": "KEY_F1"},
    ]

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

    def get_command(self):
        ch = self.stdscr.getch()
        for cmd in self.keys_cmd:
            if ch == cmd["key_number"]:
                return cmd["cmd_name"]

        return None

    """
    Переместить вверх
    """
    def up(self):
        if self.is_select_trak_list is True:
            self.track_list.move_up()
        elif self.is_view_albom_list is True:
            self.alboms_win.move_up()

    """
    Переместить вниз
    """
    def down(self):
        if self.is_select_trak_list is True:
            self.track_list.move_down()
        elif self.is_view_albom_list is True:
            self.alboms_win.move_down()

    """
    Уменьшаю громкость
    """
    def left(self):
        sound_vol = float(self.player.get_sound_volume())
        if sound_vol > 0.01:
            sound_vol -= float(round(float(0.05), 2))
            if sound_vol > 0:
                self.player.set_sound_volume(round(sound_vol,2))
                self.system_info.set_sound_volume(self.player.get_sound_volume())
    """
    Увеличиваю громкость
    """
    def right(self):
        sound_vol = float(self.player.get_sound_volume())
        if sound_vol < 1:
            sound_vol += float(round(float(0.05), 2))
            if sound_vol < 100:
                self.player.set_sound_volume(round(sound_vol,2))
                self.system_info.set_sound_volume(self.player.get_sound_volume())


    """
    Выбор трека для воспроизведения
    """
    def enter(self):
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

    """
    Поставить/снаять с паузы
    """
    def space(self):
        if self.player.playing == True:
                self.system_info.set_status_paused()        
                self.player.pause()
        else:
            self.system_info.set_status_playning()
            self.player.play()

    def key_q(self):
        self.is_stop = True

    """
    Промотать вперед
    """
    def key_d(self):
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

    """
    Промотать назад
    """
    def key_a(self):
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

    def key_tab(self):
        # при выборе "пингвина" TAB не будет работать
        #if self.is_view_albom_list is False:
        if self.is_select_trak_list is True:
            self.track_list.hide_cursor()
            self.alboms_win.show_cursor()
        else:
            self.track_list.show_cursor()
            self.alboms_win.hide_cursor()

        self.is_select_trak_list = not self.is_select_trak_list


    def key_f1(self):
        if self.is_view_albom_list is True:
            self.is_view_albom_list = False
            self.is_select_trak_list = False        
        else:
            self.is_view_albom_list = True

        self.is_select_trak_list = True
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
            if True:
            #try:
                command = self.get_command()
                if command is not None:
                    f = getattr(self, command)
                    f()
            #except Exception as e:
            #    print e
    
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

        if self.is_view_albom_list is True:
            #pass
            self.alboms_win.refresh()
        else:
            self.navigation.refresh()
            


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
