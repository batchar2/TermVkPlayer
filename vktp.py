#!/usr/bin/env python3

from tgui import ContextGUI





class ControlerContext:

    _terminal_gui = None
    def __init__(self):
                
        self._terminal_gui = ContextGUI()
        self._terminal_gui.set_login_interface()
        self.terminal_gui()


    def get_context(self):
        pass 


if __name__ == '__main__':
    app = ControlerContext()
