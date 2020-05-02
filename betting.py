from datetime import datetime
from gameexception import GameException

class Betting:
    # Betting module for poker

    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3

    def __init__(self, players, blindtimer):
        self.__players = players
        self.__pot = 0
        self.__blindtimer = blindtimer
        self.__blinds = blindtimer.getblinds()

    def newhand(self):
        self.__blinds = self.__blindtimer.getblinds()
        self.__actcount = 0
        self.__round = ''
        self.__betindex = 0
        self.__playercount = 0
        self.__pot = 0
        return self.__blinds

    def newround(self, round):
        self.__round = round
        self.__playercount = 0
        for player in self.__players:
            player.clearbet()
            if player.isactive():
                self.__playercount = self.__playercount + 1
        if self.__round == self.PREFLOP:
            self.__players[0].smallblind(self.__blinds[0])
            self.__players[1].bigblind(self.__blinds[1])
            self.__pot = self.__pot + self.__blinds[0] + self.__blinds[1]
            self.__currentbet = self.__blinds[1]
            if self.__playercount > 2:
                self.__betindex = 2
            else:
                self.__betindex = 1
        else:
            self.__currentbet = 0
            self.__betindex = 0
        self.__actcount = 0

    def nextbet(self):
        nextplayer = self.__players[self.__betindex]
        while nextplayer.isactive() == False:
            self.__betindex = self.__betindex + 1
            if self.__betindex >= len(self.__players):
                self.__betindex = 0
            nextplayer = self.__players[self.__betindex]
        if self.__round == self.PREFLOP and nextplayer.isbigblind():
            # big blind
            if nextplayer.getlastbet() < self.__currentbet:
                # someone else has (re)raised
                options = ('call', 'raise', 'fold', 'all-in')
            elif nextplayer.getlastbet() > self.__blinds[1]:
                # big blind raised and it has now come back around
                return None
            else:
                # big blind's first act
                options = ('check', 'raise', 'all-in')
        elif self.__actcount >= self.__playercount:
            # been all the way around
            return None
        elif self.__currentbet > nextplayer.getlastbet():
            # player has to act
            if nextplayer.getchips() <= self.__currentbet:
                options = ('fold', 'all-in')
            else:
                options = ('call', 'raise', 'fold', 'all-in')
        else:
            options = ('check', 'bet', 'all-in')
        self.__betindex = self.__betindex + 1
        if self.__betindex >= len(self.__players):
            self.__betindex = 0
        return (nextplayer, options)

    def currentbet(self):
        return self.__currentbet

    def act(self, player, action, amount):
        self.__actcount = self.__actcount + 1
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
            self.__actcount = 1
            self.recount_players()
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
            self.__actcount = 1
            self.recount_players()
        elif action == 'all-in':
            allinamount = player.getchips()
            if allinamount <= 0:
                raise GameException("Already all in")
            totalbet = allinamount + player.getlastbet()
            if totalbet > self.__currentbet:
                self.__currentbet = totalbet
            player.makebet(allinamount)
            self.__pot = self.__pot + allinamount
            self.__actcount = 1
            self.recount_players()
        elif action == 'fold':
            player.fold()
        else:
            pass

    def recount_players(self):
        self.__playercount = 0
        for player in self.__players:
            if player.isactive():
                self.__playercount = self.__playercount + 1

    def getpot(self):
        return self.__pot
