# -*- coding: utf-8 -*-

from win_base import BaseWin

"""
Содержится картинка и информация для управления приложением. Картинка, ну - это прикольно :)
"""
class NavigationWin(BaseWin):
    def __init__(self, parent_win, rows, cols, x, y, color_blue, color_yellow, color_white):
        super(NavigationWin, self).__init__(parent_win, rows, cols, x, y)

        self.color_blue = color_blue
        self.color_yellow = color_yellow
        self.color_white = color_white

        self.win_set_title("Help")

        self.__tmpl = '{0:16}  {1:>%d}' % (self.cols/2)
        self.win.addstr(1, 2, self.__tmpl.format('Start/Stop', '<Enter>'))
        self.win.addstr(2, 2, self.__tmpl.format('Pause', '<Space>'))
        self.win.addstr(3, 2, self.__tmpl.format('Move Up/Down', '<Up/Down>'))
        self.win.addstr(4, 2, self.__tmpl.format('Sound', '<Left/Right>'))
        self.win.addstr(5, 2, self.__tmpl.format('Seek', '<A/D>'))
        self.win.addstr(7, 2, self.__tmpl.format('Save', '<S>'))        

        """
        self.win.addstr(9, 2, "                 .88888888:. ", self.color_blue)      
        self.win.addstr(10, 2, "                88888888888888.", self.color_blue)      
        self.win.addstr(11, 2, "              .8888888888888888.   ", self.color_blue)
        self.win.addstr(12, 2, "              888888888888888888 ", self.color_blue)
        self.win.addstr(13, 2, "              88'  `88'   `88888 ", self.color_blue)
        self.win.addstr(14, 2, "              88  * 88  *  88888 ", self.color_blue )
        self.win.addstr(15, 2, "              88_  _::_  _:88888 ", self.color_blue)
        self.win.addstr(16, 2, "              88:::,::,:::::8888 ")
        self.win.addstr(17, 2, "              88`:::::::::'`8888 ")
        self.win.addstr(18, 2, "              88  `::::'    8:88.")
        self.win.addstr(19, 2, "            8888            `8:888. ", self.color_blue)      
        self.win.addstr(20, 2, "          .8888'             `888888. " , self.color_blue)
        self.win.addstr(21, 2, "         .8888:..  .::.  ...:'8888888:.", self.color_blue)
        self.win.addstr(22, 2, "       .8888.'     :'     `'::`88:88888", self.color_blue)
        self.win.addstr(23, 2, "      .8888        '         `.888:8888.", self.color_blue)
        self.win.addstr(24, 2, "      888:8         .           888:88888 ", self.color_blue)
        self.win.addstr(25, 2, "    .888:88        .:           888:88888: ", self.color_blue)
        self.win.addstr(26, 2, "    8888888.       ::           88:888888 ", self.color_blue)
        self.win.addstr(27, 2, "     .::.888.      ::           .88888888")
        self.win.addstr(28, 2, "    .::::::.888.    ::         :::`8888'.:.")
        self.win.addstr(29, 2, "   ::::::::::.888   '         .::::::::::::")
        self.win.addstr(30, 2, "   ::::::::::::.8    '      .:8::::::::::::.")
        self.win.addstr(31, 2, "  .::::::::::::::.        .:888:::::::::::::")
        self.win.addstr(32, 2, "  :::::::::::::::88:.__..:88888:::::::::::")
        self.win.addstr(33, 2, "     .:::::::::::88888888888.88:::::::::' ")
        self.win.addstr(34, 2, "         `':::_:' -- '' -'-' `':_::::'`")
        """

        
        self.win.addstr(9, 2, "                 .88888888:. ", self.color_blue)      
        self.win.addstr(10, 2, "                88888888888888.", self.color_blue)      
        self.win.addstr(11, 2, "              .8888888888888888.   ", self.color_blue)
        self.win.addstr(12, 2, "              888888888888888888 ", self.color_blue)
        self.win.addstr(13, 2, "              88'  `88'   `88888 ", self.color_blue)
        
        self.win.addstr(14, 2, "              88  ", self.color_blue)
        self.win.addstr(14, 20, "*", self.color_white)
        self.win.addstr(14, 22, "88  ", self.color_blue)
        self.win.addstr(14, 26, "*", self.color_white)
        self.win.addstr(14, 27, "  88888 ", self.color_blue )

        self.win.addstr(15, 2, "              88_  _", self.color_blue)
        self.win.addstr(15, 22, "::", self.color_yellow)
        self.win.addstr(15, 24, "_  _:88888 ", self.color_blue)

        self.win.addstr(16, 2, "              88", self.color_blue) 
        self.win.addstr(16, 18, ":::,::,:::::", self.color_yellow), 
        self.win.addstr(16, 30, "8888", self.color_blue)

        self.win.addstr(17, 2, "              88", self.color_blue)
        self.win.addstr(17, 18, "`:::::::::'`", self.color_yellow)
        self.win.addstr(17, 30, "8888 ", self.color_blue)
        
        self.win.addstr(18, 2, "              88", self.color_blue)
        self.win.addstr(18, 18, "  `::::'    ", self.color_yellow)
        self.win.addstr(18, 30, "8:88.", self.color_blue)

        self.win.addstr(19, 2, "            8888            `8:888. ", self.color_blue)      
        self.win.addstr(20, 2, "          .8888'             `888888. " , self.color_blue)
        self.win.addstr(21, 2, "         .8888:..  .::.  ...:'8888888:.", self.color_blue)
        self.win.addstr(22, 2, "       .8888.'     :'     `'::`88:88888", self.color_blue)
        self.win.addstr(23, 2, "      .8888        '         `.888:8888.", self.color_blue)
        self.win.addstr(24, 2, "      888:8         .           888:88888 ", self.color_blue)
        self.win.addstr(25, 2, "    .888:88        .:           888:88888: ", self.color_blue)
        self.win.addstr(26, 2, "    8888888.       ::           88:888888 ", self.color_blue)

        self.win.addstr(27, 2, "     .::.", self.color_yellow)
        self.win.addstr(27, 11, "888.      ::           ", self.color_blue)
        self.win.addstr(27, 34, ".", self.color_yellow)
        self.win.addstr(27, 35, "88888888", self.color_blue)

        self.win.addstr(28, 2, "    .::::::.", self.color_yellow)
        self.win.addstr(28, 14, "888.    ::         ", self.color_blue)
        self.win.addstr(28, 33, "::::", self.color_yellow)
        self.win.addstr(28, 37, "8888'", self.color_blue)
        self.win.addstr(28, 41, ".:.", self.color_yellow)

        self.win.addstr(29, 2, "   ::::::::::.", self.color_yellow)
        self.win.addstr(29, 16, "888   '         ", self.color_blue)
        self.win.addstr(29, 32, ".::::::::::::", self.color_yellow)

        self.win.addstr(30, 2, "   ::::::::::::.", self.color_yellow)
        self.win.addstr(30, 18, "8    '      .:8", self.color_blue)
        self.win.addstr(30, 32, "::::::::::::.", self.color_yellow)

        self.win.addstr(31, 2, " .::::::::::::::.", self.color_yellow)
        self.win.addstr(31, 20, "        .:888", self.color_blue)
        self.win.addstr(31, 32, ":::::::::::::", self.color_yellow)
        
        self.win.addstr(32, 2, "  :::::::::::::::", self.color_yellow)
        self.win.addstr(32, 18, "88:.__..:88888", self.color_blue)
        self.win.addstr(32, 32, ":::::::::::", self.color_yellow)
        
        self.win.addstr(33, 2, "    .:::::::::::", self.color_yellow)
        self.win.addstr(33, 18, "88888888888.88", self.color_blue)
        self.win.addstr(33, 33, ":::::::::' ", self.color_yellow)
        
        self.win.addstr(34, 2, "         `':::_:'", self.color_yellow)
        self.win.addstr(34, 19, "-- '' -'-' ", self.color_blue)
        self.win.addstr(34, 32, "`':_::::'`", self.color_yellow)
        
        self.refresh()
