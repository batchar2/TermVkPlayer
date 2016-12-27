from .curswin.WinTermBase import WinTermBase

class WinLoginForm:
	def __init__(self, curses_instance, x=0, y=0, rows=0, cols=0):
        super(WinLoginForm, self).__init__(curses_instance, x, y, rows, cols)
