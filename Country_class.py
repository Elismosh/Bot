import requests
import sqlite3


class Country:
    def __init__(self, id, att):
        self.id = id
        self.attemps = att
        self.set_name()
        self.set_path()
        self.set_pos()

    def set_name(self):
        con = sqlite3.connect("countries.db")
        cur = con.cursor()
        self.name = cur.execute(f"""SELECT country FROM paths
                    WHERE id = {self.id}""").fetchone()
        con.close()

    def set_path(self):
        con = sqlite3.connect("countries.db")
        cur = con.cursor()
        self.path = cur.execute(f"""SELECT path FROM paths
                            WHERE id = {self.id}""").fetchone()
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

        # if not response:
        #     return 0  # Нет такого адресса
        try:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            object = toponym["metaDataProperty"]["GeocoderMetaData"]
        except Exception:
            return 0
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
