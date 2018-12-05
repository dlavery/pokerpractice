class Card:
# playing card

    def __init__(self, value, suit):
        self.__suit = suit
        self.__value = value
        self.__points = 0

    def suit(self):
        return self.__suit

    def value(self):
        return self.__value

    def setpoints(self, points):
        self.__points = points

    def points(self):
        return self.__points

    def tup(self):
        return (self.__value, self.__suit)
