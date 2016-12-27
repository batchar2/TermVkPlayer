from .WinTermBase import WinTermBase

class WinPlayerInfo(WinTermBase):

    def __init__(self, curses_instance, x=0, y=0, rows=0, cols=0):
        super(WinPlayerInfo, self).__init__(curses_instance, x, y, rows, cols)