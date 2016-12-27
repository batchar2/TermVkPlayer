
""" Реализуется паттерн State. Получаются подпрограммы, события обрабатываются соответствующим классом подпрограммы """
class ApplicationContext:
    
    _state = None
    def __init__(self):
        pass

    def login_form(self):
    	pass

    def player_form(self):
    	pass

    @property
    def app(self):
    	return