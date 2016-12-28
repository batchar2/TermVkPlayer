from .ControlerBase import ControlerBase

from .curseswin import WinPlayerInfo

class ControlerLogin(ControlerBase):
    
    def __init__(self, curses_instance):
    	super(ControlerLogin, self).__init__(curses_instance)

    def view_gui(self):
    	test_win = WinPlayerInfo(self.curses_instance, 0, 0, 30, 30)
    	