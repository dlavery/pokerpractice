
class PlayerHand:
# player's hand

    def __init__(self):
        self.__hand = []

    def deal(self, card):
        # receive a card
        self.__hand.append(card)

    def gethand(self):
        return self.__hand

    def burnhand(self):
        self.__hand = []
