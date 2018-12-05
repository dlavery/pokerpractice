import sys
from game import Game
from player import Player

def do_betting():
  while True:
      actor = game.nextbet()
      if actor == None:
          break
      print(actor[0].name() + ' to bet: ' + str(actor[1]) + '; current bet: ' + str(game.getcurrentbet()))
      act_split = ('',)
      while act_split[0] not in actor[1]:
          act = input('Action?')
          act_split = act.split(' ')
          if (act_split[0] == 'bet' or act_split[0] == 'raise') and len(act_split) < 2:
              act_split = ('',)
              continue
          if len(act_split) > 1:
              betval = int(act_split[1])
          else:
              betval = 0
          game.playeract(actor[0], act_split[0], betval)

def main():
    global game
    game = Game()
    game.addplayer(Player('Alice'))
    game.addplayer(Player('Bob'))
    game.addplayer(Player('Carla'))
    game.addplayer(Player('Dave'))
    gamenumber = 0
    while True:
      answ = input('Deal? (Y/n)')
      if answ == 'n' or answ == 'N':
          sys.exit(0)
      gamenumber = gamenumber + 1
      if gamenumber > 1:
          game.rotatedealer()
      game.newhand()
      game.deal()
      print('- Hand ' + str(gamenumber))
      for player in game.players():
          print(player.name() + ': ' + str(player.showhand()))
      do_betting()
      if game.playersinhand() > 1:
          answ = input('Flop? (Y/n)')
          if answ == 'n' or answ == 'N':
              sys.exit(0)
          game.flop()
          print(' '.join([str(x.tup()) for x in game.showboard()]))
          do_betting()
          if game.playersinhand() > 1:
              answ = input('Turn? (Y/n)')
              if answ == 'n' or answ == 'N':
                  sys.exit(0)
              game.turn()
              print(' '.join([str(x.tup()) for x in game.showboard()]))
              do_betting()
              if game.playersinhand() > 1:
                  answ = input('River? (Y/n)')
                  if answ == 'n' or answ == 'N':
                      sys.exit(0)
                  game.river()
                  print(' '.join([str(x.tup()) for x in game.showboard()]))
                  do_betting()
                  if game.playersinhand() > 1:
                      answ = input('Showdown? (Y/n)')
                      if answ == 'n' or answ == 'N':
                          sys.exit(0)
      winners = game.winner()
      for h in game.hands():
          print(str(h[0]) + ' ' + str(h[1]) + ' ' + str([x.tup() for x in h[2]]))
      if len(winners) == 1:
          print(winners[0][0] + ' wins!')
      else:
          wintext = ''
          for winner in winners:
              wintext = wintext + winner[0] + ' '
          print(wintext + 'chop!')
      print('-')

main()
