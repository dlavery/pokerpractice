from datetime import datetime
from gameexception import GameException

class Betting:
    # Betting module for poker

    __BLINDS = [100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 3000, 4000, 5000]

    def __init__(self, players, blindinterval):
        self.__players = players
        self.__blinds = (self.__BLINDS[0], self.__BLINDS[0] * 2)
        self.__blindlimit = len(self.__BLINDS) - 1
        self.__blindcount = 0
        self.__blindinterval = blindinterval
        self.__starttime = datetime.utcnow().timestamp()
        self.__pot = 0

    def newhand(self):
        self.__pot = 0
        ts = datetime.utcnow().timestamp()
        blindsup = (ts - self.__starttime) >= self.__blindinterval
        if blindsup:
            if self.__blindcount < self.__blindlimit:
                self.__blindcount = self.__blindcount + 1
            self.__blinds = (self.__BLINDS[self.__blindcount], self.__BLINDS[self.__blindcount] * 2)
            self.__starttime = ts
        self.__players[0].makebet(self.__blinds[0])
        self.__players[1].makebet(self.__blinds[1])
        self.__pot = self.__pot + self.__blinds[0] + self.__blinds[1]
        self.__currentbet = self.__blinds[1]
        if len(self.__players) < 3:
            self.__betindex = 0
        else:
            self.__betindex = 2
        self.__betcount = 0
        return self.__blinds

    def newround(self):
        self.__betindex = 0
        self.__betcount = 0
        self.__currentbet = 0
        for player in self.__players:
            player.clearbet()

    def nextbet(self):
        if self.__betcount >= len(self.__players):
            return None
        nextplayer = self.__players[self.__betindex]
        while nextplayer.isactive() == False:
            if nextplayer.getlastbet() == self.__currentbet:
                return None
            self.__betindex = self.__betindex + 1
            if self.__betindex >= len(self.__players):
                return None
            nextplayer = self.__players[self.__betindex]
        if self.__currentbet > nextplayer.getlastbet():
            if nextplayer.getchips() <= self.__currentbet:
                options = ('fold', 'all-in')
            else:
                options = ('call', 'raise', 'fold', 'all-in')
        elif self.__currentbet > 0:
            # big blind
            options = ('check', 'raise', 'all-in')
        else:
            options = ('check', 'bet', 'all-in')
        self.__betindex = self.__betindex + 1
        if self.__betindex >= len(self.__players):
            self.__betindex = 0
        return (nextplayer, options)

    def currentbet(self):
        return self.__currentbet

    def act(self, player, action, amount):
        self.__betcount = self.__betcount + 1
        if action == 'check':
            pass
        elif action == 'bet':
            if amount > player.getchips():
                raise GameException("Can't bet more than your stack")
            if amount < self.__blinds[1]:
                raise GameException("Bet minimum is big blind")
            player.makebet(amount)
            self.__currentbet = amount
            self.__pot = self.__pot + amount
            self.__betcount = 1
        elif action == 'call':
            amount = self.__currentbet - player.getlastbet()
            player.makebet(amount)
            self.__pot = self.__pot + amount
        elif action == 'raise':
            raiseamount = amount - player.getlastbet()
            if raiseamount > player.getchips():
                raise GameException("Can't bet more than your stack")
            if raiseamount < self.__blinds[1]:
                raise GameException("Raise minimum is big blind")
            player.makebet(raiseamount)
            self.__currentbet = amount
            self.__pot = self.__pot + raiseamount
            self.__betcount = 1
        elif action == 'fold':
            player.fold()
        else:
            pass

    def getpot(self):
        return self.__pot
