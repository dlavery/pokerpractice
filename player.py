import uuid

class Player:
# card player

    def __init__(self, name, chipstack=5000):
        self.reset()
        self.__name = name
        self.__id = uuid.uuid1()
        self.__chips = chipstack
        self.__lastbet = 0
        self.__active = True

    def reset(self):
        self.__hand = []
        self.__lastbet = 0
        self.__active = True

    def setid(self, id):
        self.__id = id

    def getid(self):
        return self.__id

    def deal(self, card):
        # receive a card
        self.__hand.append(card)

    def hand(self):
        return self.__hand

    def name(self):
        return self.__name

    def showhand(self):
        return [str(card.tup()) for card in self.__hand]

    def addchips(self, chips):
        self.__chips = self.__chips + chips

    def subtractchips(self, chips):
        self.__chips = self.__chips - chips

    def getchips(self):
        return self.__chips

    def makebet(self, chips):
        self.__lastbet = self.__lastbet + chips
        self.subtractchips(chips)

    def getlastbet(self):
        return self.__lastbet

    def fold(self):
        self.__active = False

    def isactive(self):
        return self.__active

    def clearbet(self):
        self.__lastbet = 0
