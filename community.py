class Community:
# poker community cards

    __POINTS = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }

    __RANKING = {
        'straightflush': 9,
        'quads': 8,
        'fullhouse': 7,
        'flush': 6,
        'straight': 5,
        'trips': 4,
        'twopair': 3,
        'pair': 2,
        'highcard': 1
    }

    def __init__(self, playerlimit=8, blindinterval=600):
        self.__deck = Deck()
        self.__players = []
        self.__board = []
        self.__hands = []
        self.__inprogress = False
        self.__playerlimit = playerlimit - 1
        self.__bettingengine = Betting(self.__players, blindinterval)
        self.__blinds = (0, 0)
        self.__allowedactions = ()

    def addplayer(self, player):
        # limit to 8 players
        if self.__inprogress == True:
            raise GameException('Cannot add players, game in progress')
        if len(self.__players) > self.__playerlimit:
            raise GameException('Cannot add players, game is full')
        for p in self.__players:
            if p.name() == player.name():
                raise GameException('Cannot add player, already a player with that name')
            if p.getid() == player.getid():
                raise GameException('Cannot add player, you are already registered')
        self.__players.append(player)

    def players(self):
        return self.__players

    def newhand(self):
        for player in self.__players:
            player.reset()
        self.__deck.reset()
        self.__deck.shuffle()
        self.__board = []
        self.__hands = []
        self.__inprogress = True
        self.__blinds = self.__bettingengine.newhand()
        self.__allowedactions = ()

    def getblinds(self):
        return self.__blinds

    def hands(self):
        return self.__hands

    def setboard(self, board):
        self.__board = board[:]

    def deal(self):
        for i in range(0, 2):
            for player in self.__players:
                player.deal(self.__deck.card())
        self.__bettingengine.newround(Betting.PREFLOP)

    def flop(self):
        if self.playersinhand() < 2:
            raise GameOverException('Hand is won already')
        for i in range (0, 3):
            self.__board.append(self.__deck.card())
        self.__bettingengine.newround(Betting.FLOP)

    def showboard(self):
        return self.__board

    def burnandturn(self):
        self.__deck.card()                     # burn one
        self.__board.append(self.__deck.card())  # turn one

    def turn(self):
        if self.playersinhand() < 2:
            raise GameOverException('Hand is won already')
        self.__bettingengine.newround(Betting.TURN)
        self.burnandturn()

    def river(self):
        if self.playersinhand() < 2:
            raise GameOverException('Hand is won already')
        self.__bettingengine.newround(Betting.RIVER)
        self.burnandturn()

    def rotatedealer(self):
        player = self.__players.pop(0)
        self.__players.append(player)

    def nextbet(self):
        if self.playersinhand() <= 1:
            return None
        nextbet = self.__bettingengine.nextbet()
        if nextbet == None:
            self.__allowedactions = ()
            return None
        self.__allowedactions = nextbet[1]
        return nextbet

    def playeract(self, player, action, amount=0):
        if action not in self.__allowedactions:
            raise GameException('Action not allowed')
        self.__bettingengine.act(player, action, amount)

    def getcurrentbet(self):
        return self.__bettingengine.currentbet()

    def playersinhand(self):
        no_of_players = 0
        for player in self.__players:
            if player.isactive():
                no_of_players = no_of_players + 1
        return no_of_players

    def getpot(self):
        return self.__bettingengine.getpot()

    def winner(self):
        hands = []
        for player in self.__players:
            if player.isactive() == False:
                continue
            hands.append(self.makehand(player))
        self.__hands = hands[:]
        winners = []
        for hand in hands:
            if winners and hand[1] > winners[0][1]: # pick the biggest ranking
                winners = []
                winners.append(hand)
            elif winners and hand[1] < winners[0][1]:
                pass
            else:
                winners.append(hand)
        if len(winners) > 1:    # equal rank, look for high card
            dedup = []
            i = 0
            highvalue = 0
            while i < 5:
                for hand in winners:
                    cards = hand[2]
                    if cards[i].points() > highvalue:
                        dedup = []
                        dedup.append(hand)
                        highvalue = cards[i].points()
                    elif cards[i].points() == highvalue:
                        dedup.append(hand)
                winners = dedup[:]
                if len(winners) == 1:
                    break
                dedup = []
                highvalue = 0
                i = i + 1

        the_pot = self.__bettingengine.getpot()
        while the_pot > 0:
            for winner in winners:
                for player in self.__players:
                    if player.name() == winner[0]:
                        player.addchips(1)
                        the_pot = the_pot - 1
                        if the_pot < 1:
                            break
                if the_pot < 1:
                    break

        return winners

    def makehand(self, player):
        hand = self.__board + player.hand()
        sortedhand = []
        for card in hand:
            card.setpoints(self.__POINTS[card.value()])
            sortedhand.append(card)
        sortedhand = sorted(sortedhand, key=lambda card: (14 - card.points()))
        flushhand = self.isflush(sortedhand)
        if flushhand:
            straighthand = self.isstraight(flushhand)
            if straighthand:
                return (player.name(), self.__RANKING['straightflush'], straighthand)
            else:
                return (player.name(), self.__RANKING['flush'], flushhand[0:5])
        quadshand = self.isquads(sortedhand)
        if quadshand:
            return (player.name(), self.__RANKING['quads'], quadshand)
        fullhousehand = self.isfullhouse(sortedhand)
        if fullhousehand:
            return (player.name(), self.__RANKING['fullhouse'], fullhousehand)
        straighthand = self.isstraight(sortedhand)
        if straighthand:
            return (player.name(), self.__RANKING['straight'], straighthand)
        tripshand = self.istrips(sortedhand)
        if tripshand:
            return (player.name(), self.__RANKING['trips'], tripshand)
        twopairhand = self.istwopair(sortedhand)
        if twopairhand:
            return (player.name(), self.__RANKING['twopair'], twopairhand)
        pairhand = self.ispair(sortedhand)
        if pairhand:
            return (player.name(), self.__RANKING['pair'], pairhand)
        return (player.name(), self.__RANKING['highcard'], sortedhand[0:5])

    def isquads(self, hand):
        count = {}
        quadhand = False
        for card in hand:
            if card.points() not in count:
                count[card.points()] = []
            count[card.points()].append(card)
        for k, v in count.items():
            if len(v) > 3:
                quadhand = v
                break
        if quadhand:
            for k in sorted(count, reverse=True):
                if len(count[k]) < 4:
                    quadhand.append(count[k][0])
                    break
        return quadhand

    def isfullhouse(self, hand):
        count = {}
        fhhand = False
        for card in hand:
            if card.points() not in count:
                count[card.points()] = []
            count[card.points()].append(card)
        sortedcount = sorted(count, reverse=True)
        for k in sortedcount:
            if len(count[k]) == 3:
                fhhand = count[k]
                break
        if fhhand:
            for k in sortedcount:
                if len(count[k]) == 2:
                    fhhand = fhhand + count[k]
                    break
        if fhhand and len(fhhand) == 5:
            return fhhand
        else:
            return False

    def isflush(self, hand):
        clubs = []
        diamonds = []
        hearts = []
        spades = []
        for card in hand:
            if card.suit() == 'C':
                clubs.append(card)
            elif card.suit() == 'D':
                diamonds.append(card)
            elif card.suit() == 'H':
                hearts.append(card)
            else:
                spades.append(card)
        # got a flush?
        if len(clubs) > 4:
            return clubs
        elif len(diamonds) > 4:
            return diamonds
        elif len(hearts) > 4:
            return hearts
        elif len(spades) > 4:
            return spades
        return False

    def isstraight(self, hand):
        topcard = hand[0]
        newhand = hand[:]
        if topcard.value() == 'A':
            # ace can be low too
            bottomcard = Card(topcard.value(), topcard.suit())
            bottomcard.setpoints(1)
            newhand.append(bottomcard)
        straight = []
        lastvalue = 0
        for card in newhand:
            if straight == [] or card.points() == (lastvalue - 1):
                straight.append(card)
            elif card.points() == lastvalue:
                continue
            else:
                straight = []
                straight.append(card)
            if len(straight) > 4:
                return straight
            lastvalue = card.points()
        return False

    def istrips(self, hand):
        count = {}
        tripshand = False
        for card in hand:
            if card.points() not in count:
                count[card.points()] = []
            count[card.points()].append(card)
        for k in sorted(count, reverse=True):
            if len(count[k]) == 3:
                tripshand = count[k]
                break
        if tripshand:
            for card in hand:
                if card not in tripshand:
                    tripshand.append(card);
                if len(tripshand) > 4:
                    break
        return tripshand

    def istwopair(self, hand):
        count = {}
        tphand = []
        for card in hand:
            if card.points() not in count:
                count[card.points()] = []
            count[card.points()].append(card)
        for k in sorted(count, reverse=True):
            if len(count[k]) == 2:
                tphand = tphand + count[k]
            if len(tphand) == 4:
                break
        if len(tphand) == 4:
            for card in hand:
                if card not in tphand:
                    tphand.append(card);
                    break
        else:
            tphand = []
        return tphand

    def ispair(self, hand):
        count = {}
        pairhand = []
        for card in hand:
            if card.points() not in count:
                count[card.points()] = []
            count[card.points()].append(card)
        for k in sorted(count, reverse=True):
            if len(count[k]) == 2:
                pairhand = count[k]
                break
        if pairhand:
            for card in hand:
                if card not in pairhand:
                    pairhand.append(card);
                if len(pairhand) > 4:
                    break
        return pairhand
