class ID(object):
    def __init__(self, type, number, country):
        self._type = type
        self._number = number
        self._country = country

    def to_primitive(self):
        return {
            'type': self._type,
            'number': self._number,
            'country': self._country
        }

    @staticmethod
    def from_primitive(primitive):
        if primitive['type'] == "id":
            return SouthAfricanID(number=primitive['number'])
        else:
            return Passport(number=primitive['number'], country=primitive['country'])


class SouthAfricanID(ID):
    def __init__(self, number):
        super(SouthAfricanID, self).__init__(type='id', number=number, country="ZA")


class Passport(ID):
    def __init__(self, number, country):
        super(Passport, self).__init__(type='passport', number=number, country=country)


class Cellphone(object):
    def __init__(self, number, country="ZA"):
        self._number = number
        self._country = country

    def to_primitive(self):
        return {
            'number': self._number,
            'country': self._country
        }

    @staticmethod
    def from_primitive(primitive):
        return Cellphone(number=primitive['number'], country=primitive['country'])