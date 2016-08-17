# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty

class BaseStorage(object):
    """ Базовый абстрактный класс хранилища данных """
    __metaclass__ = ABCMeta

    def __init__(self, login, password, count):
        self.__login = login
        self.__password = password
        self.__count = count

    @abstractmethod
    def login(self, login, password):
        pass

    @abstractmethod
    def load_traks(self, albom=None):
        pass

    @abstractmethod
    def load_alboms(self):
        if self.__vk is None:
            self.__alboms = self.vk.method('audio.getAlbums', {'count':100})
            return True
        else:
            return False

    @abstractproperty
    def traks(self):
        pass

    @abstractproperty
    def alboms(self):
        pass