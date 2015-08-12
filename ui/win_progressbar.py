# -*- coding: utf-8 -*-

from win_base import BaseWin
import time
"""
Отдельное окно с информацией и времени и шкалой прогресса воспроизведения
"""
class ProgressBarWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y, color_playning, color_free):
        super(ProgressBarWin, self).__init__(parent_win, rows, cols, x, y)
        self.__size_bar = self.cols - 3
        self.color_playning = color_playning
        self.color_free = color_free

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
                    self.win.addstr(1, i+1, c, self.color_playning)
                else: 
                    self.win.addstr(1, i+1, c, self.color_free)
                i += 1
            self.refresh()
