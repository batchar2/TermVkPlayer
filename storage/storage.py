# -*- coding: utf-8 -*-
import sys
from vk_storage import VkStorage

class Storage(object):
    """ 
    Класс фабрика. По строке @type_string с наименованием апи, определяет необходимый класс. 
    Нужен для добавления в будующем поддержки других API, помимо VK
    """
    def __init__(self, type_string):
        self._storage = None
        if type_string == 'VK':
            self._storage = VkStorage()
    
    """ Собственно, передача требуемого класса в приложение """
    def get(self):
        return self._storage
