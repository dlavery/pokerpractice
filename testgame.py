import unittest
from game import Game, GameException
from player import Player
from card import Card

class TestGame(unittest.TestCase):

    def setUp(self):
        pass

    def test_maximumplayers(self):
        game = Game()
        gamefull = False
        game.addplayer(Player('1'))
        game.addplayer(Player('2'))
        game.addplayer(Player('3'))
        game.addplayer(Player('4'))
        game.addplayer(Player('5'))
        game.addplayer(Player('6'))
        game.addplayer(Player('7'))
        game.addplayer(Player('8'))
        try:
            game.addplayer(Player('9'))
        except GameException:
            gamefull = True
        self.assertEqual(gamefull, True)

    def test_gameinprogress(self):
        game = Game()
        gamestarted = False
        game.addplayer(Player('1'))
        game.addplayer(Player('2'))
        game.addplayer(Player('3'))
        game.addplayer(Player('4'))
        game.newhand()
        game.deal()
        try:
            game.addplayer(Player('5'))
        except GameException:
            gamestarted = True
        self.assertEqual(gamestarted, True)

    def test_duplicateplayer(self):
        game = Game()
        duplicateplayer = False
        game.addplayer(Player('1'))
        try:
            game.addplayer(Player('1'))
        except GameException:
            duplicateplayer = True
        self.assertEqual(duplicateplayer, True)

    def test_ranking_highcard(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('9', 'C'))
        alice.deal(Card('Q', 'C'))
        game.setboard([Card('K', 'S'), Card('7', 'H'), Card('A', 'H'), Card('8', 'S'), Card('2', 'S')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 1)

    def test_ranking_pair(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('8', 'C'))
        alice.deal(Card('Q', 'C'))
        game.setboard([Card('K', 'S'), Card('7', 'H'), Card('A', 'H'), Card('8', 'S'), Card('2', 'S')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 2)

    def test_ranking_twopairs(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('8', 'C'))
        alice.deal(Card('Q', 'C'))
        game.setboard([Card('K', 'S'), Card('Q', 'H'), Card('A', 'H'), Card('8', 'S'), Card('2', 'S')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 3)

    def test_ranking_trips(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('8', 'C'))
        alice.deal(Card('Q', 'C'))
        game.setboard([Card('K', 'S'), Card('Q', 'H'), Card('A', 'H'), Card('Q', 'S'), Card('2', 'S')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 4)

    def test_ranking_straight(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('10', 'C'))
        alice.deal(Card('Q', 'C'))
        game.setboard([Card('K', 'S'), Card('J', 'H'), Card('9', 'H'), Card('Q', 'S'), Card('2', 'S')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 5)

    def test_ranking_straightwithacehigh(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('10', 'C'))
        alice.deal(Card('Q', 'C'))
        game.setboard([Card('K', 'S'), Card('J', 'H'), Card('A', 'H'), Card('Q', 'S'), Card('2', 'S')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 5)

    def test_ranking_straightwithacelow(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('3', 'C'))
        alice.deal(Card('5', 'C'))
        game.setboard([Card('K', 'S'), Card('J', 'H'), Card('A', 'H'), Card('4', 'S'), Card('2', 'S')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 5)

    def test_ranking_straightwithapair(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('3', 'C'))
        alice.deal(Card('5', 'C'))
        game.setboard([Card('6', 'S'), Card('4', 'C'), Card('Q', 'H'), Card('4', 'S'), Card('2', 'S')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 5)

    def test_ranking_flush(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('3', 'C'))
        alice.deal(Card('5', 'C'))
        game.setboard([Card('7', 'S'), Card('4', 'C'), Card('Q', 'C'), Card('4', 'S'), Card('2', 'C')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 6)

    def test_ranking_fullhouse(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('3', 'C'))
        alice.deal(Card('4', 'D'))
        game.setboard([Card('7', 'S'), Card('4', 'C'), Card('Q', 'C'), Card('4', 'S'), Card('3', 'H')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 7)

    def test_ranking_quads(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('3', 'C'))
        alice.deal(Card('3', 'D'))
        game.setboard([Card('7', 'S'), Card('K', 'C'), Card('3', 'S'), Card('4', 'S'), Card('3', 'H')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 8)

    def test_ranking_straightflush(self):
        game = Game()
        alice = Player('Alice')
        game.addplayer(alice)
        alice.deal(Card('8', 'D'))
        alice.deal(Card('10', 'D'))
        game.setboard([Card('7', 'D'), Card('K', 'C'), Card('9', 'D'), Card('6', 'D'), Card('3', 'H')])
        ranking = game.makehand(alice)
        self.assertEqual(ranking[1], 9)

    def test_winner_1playerwithhigherpair(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        game.addplayer(alice)
        game.addplayer(bob)
        alice.deal(Card('8', 'C'))
        alice.deal(Card('Q', 'C'))
        bob.deal(Card('8', 'D'))
        bob.deal(Card('K', 'D'))
        game.setboard([Card('K', 'S'), Card('7', 'H'), Card('A', 'H'), Card('8', 'S'), Card('2', 'S')])
        winners = game.winner()
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0][0], 'Bob')

    def test_winner_2playerswithsamepair(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        game.addplayer(alice)
        game.addplayer(bob)
        alice.deal(Card('8', 'C'))
        alice.deal(Card('Q', 'C'))
        bob.deal(Card('8', 'D'))
        bob.deal(Card('K', 'D'))
        game.setboard([Card('4', 'S'), Card('7', 'H'), Card('A', 'H'), Card('8', 'S'), Card('2', 'S')])
        winners = game.winner()
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0][0], 'Bob')

    def test_winner_2playerswithsamehand(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        game.addplayer(alice)
        game.addplayer(bob)
        alice.deal(Card('8', 'C'))
        alice.deal(Card('Q', 'C'))
        bob.deal(Card('8', 'D'))
        bob.deal(Card('Q', 'D'))
        game.setboard([Card('4', 'S'), Card('7', 'H'), Card('A', 'H'), Card('8', 'S'), Card('2', 'S')])
        winners = game.winner()
        self.assertEqual(len(winners), 2)
        self.assertEqual(winners[0][0], 'Alice')
        self.assertEqual(winners[1][0], 'Bob')

    def test_winner_2players1winner(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        game.addplayer(alice)
        game.addplayer(bob)
        alice.deal(Card('8', 'C'))
        alice.deal(Card('Q', 'C'))
        bob.deal(Card('7', 'D'))
        bob.deal(Card('10', 'D'))
        game.setboard([Card('8', 'S'), Card('8', 'H'), Card('A', 'H'), Card('Q', 'S'), Card('10', 'S')])
        winners = game.winner()
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0][0], 'Alice')

    def test_preflop_betting_all_call(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        john = Player('John')
        jill = Player('Jill')
        game.addplayer(alice)
        game.addplayer(bob)
        game.addplayer(john)
        game.addplayer(jill)
        game.newhand()
        game.deal()
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'John')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Jill')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Alice')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Bob')
        self.assertEqual(actor[1], ('check', 'raise'))
        game.playeract(actor[0], 'check', 0)
        actor = game.nextbet()
        self.assertEqual(actor, None)
        self.assertEqual(alice.getchips(), 4800)
        self.assertEqual(bob.getchips(), 4800)
        self.assertEqual(john.getchips(), 4800)
        self.assertEqual(jill.getchips(), 4800)

    def test_preflop_betting_player_raise(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        john = Player('John')
        jill = Player('Jill')
        game.addplayer(alice)
        game.addplayer(bob)
        game.addplayer(john)
        game.addplayer(jill)
        game.newhand()
        game.deal()
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'John')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Jill')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'raise', 400)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Alice')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Bob')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'John')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor, None)
        self.assertEqual(alice.getchips(), 4600)
        self.assertEqual(bob.getchips(), 4600)
        self.assertEqual(john.getchips(), 4600)
        self.assertEqual(jill.getchips(), 4600)

    def test_preflop_betting_smallblind_raise(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        john = Player('John')
        jill = Player('Jill')
        game.addplayer(alice)
        game.addplayer(bob)
        game.addplayer(john)
        game.addplayer(jill)
        game.newhand()
        game.deal()
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'John')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Jill')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Alice')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'raise', 500)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Bob')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'John')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Jill')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor, None)
        self.assertEqual(alice.getchips(), 4500)
        self.assertEqual(bob.getchips(), 4500)
        self.assertEqual(john.getchips(), 4500)
        self.assertEqual(jill.getchips(), 4500)

    def test_preflop_betting_bigblind_raise(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        john = Player('John')
        jill = Player('Jill')
        game.addplayer(alice)
        game.addplayer(bob)
        game.addplayer(john)
        game.addplayer(jill)
        game.newhand()
        game.deal()
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'John')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Jill')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Alice')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Bob')
        self.assertEqual(actor[1], ('check', 'raise'))
        game.playeract(actor[0], 'raise', 1000)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'John')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Jill')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Alice')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor, None)
        self.assertEqual(alice.getchips(), 4000)
        self.assertEqual(bob.getchips(), 4000)
        self.assertEqual(john.getchips(), 4000)
        self.assertEqual(jill.getchips(), 4000)

    def test_preflop_betting_fold_1(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        john = Player('John')
        jill = Player('Jill')
        game.addplayer(alice)
        game.addplayer(bob)
        game.addplayer(john)
        game.addplayer(jill)
        game.newhand()
        game.deal()
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'John')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'fold', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Jill')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Alice')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Bob')
        self.assertEqual(actor[1], ('check', 'raise'))
        game.playeract(actor[0], 'check', 0)
        actor = game.nextbet()
        self.assertEqual(actor, None)
        self.assertEqual(alice.getchips(), 4800)
        self.assertEqual(bob.getchips(), 4800)
        self.assertEqual(john.getchips(), 5000)
        self.assertEqual(jill.getchips(), 4800)

    def test_preflop_betting_fold_2(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        john = Player('John')
        jill = Player('Jill')
        game.addplayer(alice)
        game.addplayer(bob)
        game.addplayer(john)
        game.addplayer(jill)
        game.newhand()
        game.deal()
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'John')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Jill')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Alice')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'fold', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Bob')
        self.assertEqual(actor[1], ('check', 'raise'))
        game.playeract(actor[0], 'check', 0)
        actor = game.nextbet()
        self.assertEqual(actor, None)
        self.assertEqual(alice.getchips(), 4900)
        self.assertEqual(bob.getchips(), 4800)
        self.assertEqual(john.getchips(), 4800)
        self.assertEqual(jill.getchips(), 4800)

    def test_postflop_betting_all_call(self):
        game = Game()
        alice = Player('Alice')
        bob = Player('Bob')
        john = Player('John')
        jill = Player('Jill')
        game.addplayer(alice)
        game.addplayer(bob)
        game.addplayer(john)
        game.addplayer(jill)
        game.newhand()
        game.deal()
        actor = game.nextbet()
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        game.playeract(actor[0], 'check', 0)
        game.flop()
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Alice')
        self.assertEqual(actor[1], ('check', 'bet'))
        game.playeract(actor[0], 'check', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Bob')
        self.assertEqual(actor[1], ('check', 'bet'))
        try:
            game.playeract(actor[0], 'bet', 100)
            assertEqual(1, 0)
        except GameException as e:
            pass
        game.playeract(actor[0], 'bet', 400)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'John')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        try:
            game.playeract(actor[0], 'check', 0)
            assertEqual(1, 0)
        except GameException as e:
            pass
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Jill')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor[0].name(), 'Alice')
        self.assertEqual(actor[1], ('call', 'raise', 'fold'))
        game.playeract(actor[0], 'call', 0)
        actor = game.nextbet()
        self.assertEqual(actor, None)
        self.assertEqual(alice.getchips(), 4400)
        self.assertEqual(bob.getchips(), 4400)
        self.assertEqual(john.getchips(), 4400)
        self.assertEqual(jill.getchips(), 4400)

if __name__ == '__main__':
    unittest.main()