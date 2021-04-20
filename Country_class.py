import requests


class Country:
    def __init__(self, id, att):
        self.id = id
        self.attemps = att
        self.set_name()
        self.set_path()
        self.set_pos()

    def set_name(self):
        pass

    def set_path(self):
        pass

    def set_pos(self):
        self.x = 0
        self.y = 0

    def right_country(self, text):
        map_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                      f"geocode={text}&format=json"
        response = requests.get(map_request)

        if not response:
            return 0  # Нет такого адресса
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        object = toponym["metaDataProperty"]["GeocoderMetaData"]
        if object['kind'] != "country":
            return 1  # Это не страна
        x = toponym["Point"]["pos"].split()[0]
        y = toponym["Point"]["pos"].split()[1]
        if x == self.x and y == self.y:
            return 2  # Верно отгадано
        if abs(x - self.x) >= abs(y - self.y):
            if x > self.x:
                return 31  # запад
            else:
                return 32  # восток
        else:
            if y > self.y:
                return 33  # север
            else:
                return 34  # юг
