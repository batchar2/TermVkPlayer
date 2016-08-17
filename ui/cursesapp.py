# -*- coding: utf-8 -*-

import curses


from wins.sysinfo import SysInfoWin

class CursesProperty(object):
    """ Свойства и переменные curses для удобства сведены в один класс """
    def __init__(self):
        self._stdscr = curses.initscr()
        self._stdscr.clear()

        curses.cbreak()
        curses.noecho()
        self._stdscr.keypad(0)

        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

         # получаю размеры экрана и оговариваю работу с клавиатурой
        self._stdscr.keypad(1)
        
        # Создаю главное окно. Конечно, можно было и без него обойтись, однако на будующее зазор оставлю
        self._gen_win = curses.newwin(self.rows, self.cols, 0, 0)
    
        self._initclr()

    
    #""" Инициализация цветов """
    def _initclr(self):
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



    """ Возврат указателя на главное окно, на главном окне выводятся все остальные подокна """
    @property
    def screen(self):
        return self._stdscr

    @property
    def general_win(self):
        return self._gen_win

    @property
    def rows(self):
        rows, cols = self._stdscr.getmaxyx()
        return rows

    @property
    def cols(self):
        rows, cols = self._stdscr.getmaxyx()
        return cols




class CursesApplication(object):
    
    """ Фасад GUI-интерфейса """
    PLAYER_NAME = ""
    PLAYER_VERSION = ""
    storage = None

    def __init__(self, player_name, player_version, storage):
        self.PLAYER_NAME = player_name
        self.PLAYER_VERSION = player_version

        self.storage = storage

        self.curses_property = CursesProperty()

        self._sysinfo = SysInfoWin(self.curses_property.general_win, 6, self.curses_property.cols/5, 0, 0, 
                                    self.PLAYER_NAME, self.PLAYER_VERSION, self.curses_property.COLOR_CONTENT)

    @property
    def sysinfo(self):
        return self._sysinfo


    def refresh(self):
        print "CursesApplication.refresh"
        

        self.curses_property.screen.refresh()
        #self.curses_property.general_win.refresh()

        self._sysinfo.refresh()

    """ Получить символ (команду) через ввод ncurses """
    def getch(self):
        return self.curses_property.screen.getch()