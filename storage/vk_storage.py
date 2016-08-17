# -*- coding: utf-8 -*-
import sys
import vk_api

from base_storage import BaseStorage

class VkStorage(BaseStorage):
    """ Класс является прослойкой между vk_api и приложением. """

    genres =   {
        '1': 'Rock',
        '2': 'Pop',
        '3': 'Rap & Hip-Hop',
        '4': 'Easy Listening',
        '5': 'Dance & House',
        '6': 'Instrumental',
        '7': 'Metal',
        '21': 'Alternative',
        '8': 'Dubstep',
        '9': 'Jazz & Blues',
        '10': 'Drum & Bass',
        '11': 'Trance',
        '12': 'Chanson',
        '13': 'Ethnic',
        '14': 'Acoustic & Vocal',
        '15': 'Reggae',
        '16': 'Classical',
        '17': 'Indie Pop',
        '19': 'Speech',
        '22': 'Electropop & Disco',
        '18': 'Other',
    }

    def __init__(self, login=None, password=None, count=9999):
        super(VkStorage, self).__init__(login, password, count)
        self.__alboms = None
        self.__tracks = None
        self.__login = login
        self.__password = password
        self.__count = count


    def login(self, login=None, password=None):
        """ Авторизвация """
        if login is not None and password is not None:
            self.__login = login
            self.__password = password

        self.__vk = vk_api.VkApi(login=self.__login, 
                                    password=self.__password)
        try:
            self.__vk.authorization()
        except vk_api.AuthorizationError as error_msg:
            self.__vk = None
            return False, 'The password/login you entered is incorrect'
        except vk.ConnectionError as error_msg:
            self.__vk = None
            return False, 'Connection aborted'
        
        return True, "Ok"

    def load_traks(self, albom_id=None):
        """ Производит загрузку списка треков """
        if self.__vk is not None:
            if albom_id is None:
                self.__tracks = self.__vk.method('audio.get', {'count': self.__count})
            else:
                self.__tracks = self.__vk.method('audio.get', {'count': self.__count, 'album_id': albom_id})
            return True
        else:
            return False


    def load_alboms(self):
        """ Производит загрузку списка альбомов пользователя """
        if self.__vk is not None:
            self.__alboms = self.__vk.method('audio.getAlbums', {'count':100})
            return True
        else:
            return False

    @property
    def tracks(self):
        """
            Передает данные для дальнейшего использования, предварительно проведа небольшие манипуляции:
            1) убираем двойные пробелы в название, артисте
            2) подставляю символьному цифровому представлению жаннра наименование
         """
        traks = []
        if self.__tracks is not None:
            if len(self.__tracks['items'] ) == 0: 
                return None

            for item in self.__tracks[u'items']:
                if u'genre_id' not in item:
                    item[u'genre_id'] = '18'

                obj = {
                    'title': item[u'title'].replace('  ', ' '),
                    'artist': item[u'artist'].replace('  ', ' '),
                    'genre_title': self.__get_genre_name(item[u'genre_id']),
                    'genre_id': item[u'genre_id'],
                    'duration': item['duration'],
                    'url': item[u'url'],
                }
                traks.append(obj)
            return traks
        else:
            return None

    @property
    def alboms(self):
        """ Передает список альбомов пользователю. Так же генерируется псеводальбом с id=-1. Сюда входят ВСЕ песни :) """
        alboms = []
        item = {
            'id': -1,
            'title': '[all]',
        }
        alboms.append(item)

        if len(self.__alboms['items'] ) != 0: 
            for item in self.__alboms[u'items']:
                item = {
                    'id': item[u'id'],
                    'title': item[u'title'],
                }
                alboms.append(item)

        return alboms

    def __get_genre_name(self, key):
        """ Сопоставляет номер с названием жанра. номера предопределены ВК  """
        if str(key) in self.genres:
            return self.genres[str(key)]
        else:
            return 'Other'