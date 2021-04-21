import random

import requests
import sqlite3


# Класс для игры в очертания
class CountryOutline:
    def __init__(self, att):
        # У любой страны из бд есть очертания, следовательно такой id
        self.id = random.randrange(1, 44)
        self.attemps = att
        self.set_name()
        self.set_path()
        self.set_pos()

    # С помощью бд получаем название страны
    def set_name(self):
        con = sqlite3.connect("countries.db")
        cur = con.cursor()
        self.name = cur.execute("""SELECT country FROM paths
                    WHERE id = ?""", (self.id,)).fetchone()[0]
        con.close()

    # Получаем путь к очертанию страны
    def set_path(self):
        con = sqlite3.connect("countries.db")
        cur = con.cursor()
        self.path = cur.execute(f"""SELECT outline_path FROM paths
                            WHERE id = ?""", (self.id,)).fetchone()[0]
        con.close()

    # Получаем координаты страны
    def set_pos(self):
        map_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                      f"geocode={self.name}&format=json"
        response = requests.get(map_request)
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        self.x = float(toponym["Point"]["pos"].split()[0])
        self.y = float(toponym["Point"]["pos"].split()[1])

    # Проверяем сообщение пользователя и возвращаем exit_code проверки
    def right_country(self, text):
        map_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                      f"geocode={text}&format=json"
        response = requests.get(map_request)

        try:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            object = toponym["metaDataProperty"]["GeocoderMetaData"]
            if object['kind'] != "country":
                return 1  # Это не страна
            x = float(toponym["Point"]["pos"].split()[0])
            y = float(toponym["Point"]["pos"].split()[1])
            if x == self.x and y == self.y:
                return 2  # Верно отгадано
            if abs(x - self.x) >= abs(y - self.y):
                if x > self.x:
                    return 31  # запад
                else:
                    return 32  # восток
            else:
                if y < self.y:
                    return 33  # север
                else:
                    return 34  # юг
        except Exception:
            return 0


# Класс для игры в сувенир
class CountrySouvenir:
    def __init__(self):
        # Не для всех стран в бд есть сувениры,
        # с помощью метода выбираем только из имеющихся
        self.set_id()
        self.set_name()
        self.set_path()
        self.set_pos()

    def set_id(self):
        con = sqlite3.connect("countries.db")
        cur = con.cursor()
        x = cur.execute("""SELECT id FROM paths 
        WHERE souvenirs_path IS NOT NULL""").fetchall()
        con.close()
        self.id = random.choice(x)[0]

    def set_name(self):
        con = sqlite3.connect("countries.db")
        cur = con.cursor()
        self.name = cur.execute("""SELECT country FROM paths
                        WHERE id = ?""", (self.id,)).fetchone()[0]
        con.close()

    def set_path(self):
        con = sqlite3.connect("countries.db")
        cur = con.cursor()
        self.path = cur.execute("""SELECT souvenirs_path FROM paths
                        WHERE id = ?""", (self.id,)).fetchone()[0]
        con.close()

    def set_pos(self):
        map_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                      f"geocode={self.name}&format=json"
        response = requests.get(map_request)
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        self.x = float(toponym["Point"]["pos"].split()[0])
        self.y = float(toponym["Point"]["pos"].split()[1])

    # Т.к. попытка всего одна, нам не важно, как находится указанная страна относительно загаданной
    def right_country(self, text):
        map_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                      f"geocode={text}&format=json"
        response = requests.get(map_request)

        try:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            object = toponym["metaDataProperty"]["GeocoderMetaData"]
            if object['kind'] != "country":
                return 1  # Это не страна
            x = float(toponym["Point"]["pos"].split()[0])
            y = float(toponym["Point"]["pos"].split()[1])
            if x == self.x and y == self.y:
                return 2  # Верно отгадано
            return 3
        except Exception:
            return 0


# Класс для игры в фото
class CountryPhoto:
    def __init__(self, att):
        self.set_id()
        self.attemps = att
        self.set_name()
        self.set_path()
        self.set_pos()

    def set_id(self):
        con = sqlite3.connect("countries.db")
        cur = con.cursor()
        x = cur.execute("""SELECT id FROM paths 
        WHERE photo_path IS NOT NULL""").fetchall()
        con.close()
        self.id = random.choice(x)[0]

    def set_name(self):
        con = sqlite3.connect("countries.db")
        cur = con.cursor()
        self.name = cur.execute("""SELECT country FROM paths
                    WHERE id = ?""", (self.id,)).fetchone()[0]
        con.close()

    def set_path(self):
        con = sqlite3.connect("countries.db")
        cur = con.cursor()
        self.path = cur.execute(f"""SELECT photo_path FROM paths
                            WHERE id = ?""", (self.id,)).fetchone()[0]
        con.close()

    def set_pos(self):
        map_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                      f"geocode={self.name}&format=json"
        response = requests.get(map_request)
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        self.x = float(toponym["Point"]["pos"].split()[0])
        self.y = float(toponym["Point"]["pos"].split()[1])

    def right_country(self, text):
        map_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                      f"geocode={text}&format=json"
        response = requests.get(map_request)

        try:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            object = toponym["metaDataProperty"]["GeocoderMetaData"]
            if object['kind'] != "country":
                return 1  # Это не страна
            x = float(toponym["Point"]["pos"].split()[0])
            y = float(toponym["Point"]["pos"].split()[1])
            if x == self.x and y == self.y:
                return 2  # Верно отгадано
            if abs(x - self.x) >= abs(y - self.y):
                if x > self.x:
                    return 31  # запад
                else:
                    return 32  # восток
            else:
                if y < self.y:
                    return 33  # север
                else:
                    return 34  # юг
        except Exception:
            return 0
