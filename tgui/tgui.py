from .CursesInstance import CursesInstance

from .controlers import ControlerLogin
from .controlers import ControlerPlayer

#from .forms.BuilderForm import BuilderLogin, BuilderPlayer 



""" Текстовый интерфейс приложения. Реализован на ncurses
 
Реализуется паттерн State.
Переключает вид и контролер 
Получаются подпрограммы, события обрабатываются соответствующим классом
При изменении глобального состояния программы: форма логина, окно плеера - подменяем соответствующий обработчик. 
"""
class ContextGUI:

    _curses_instance = None
    _controler = None

    def __init__(self):
        self._curses_instance = CursesInstance()

        

        #self._builder_login = BuilderLogin(self._curses_instance)
        #self._builder_player = BuilderPlayer(self._curses_instance)


    def set_login_interface(self):
        self._controler = ControlerLogin(self._curses_instance)
        
    def set_player_interface(self):
        self._controler = ControlerPlayer(self._curses_instance)

    def __call__(self):
        self._controler.view_gui()


        while True:
            symbol = self._curses_instance.stdscr.getch()
            self._controler(symbol)
            #print(ch)


