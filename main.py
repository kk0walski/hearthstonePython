import traceback

from game.State import GameState
from game.engine import GameEngine
from game.players.agents import random


def create_initial_game_state(clsA, nameA, clsB, nameB):
    player_A = clsA(nameA)
    player_B = clsB(nameB)
    curr_step = 0

    return GameState(player_A, player_B, curr_step)


def main():
    confs = [
        (random.RandomPlayer, 'RandomPlayer1', random.RandomPlayer, 'RandomPlayer2'),
    ]
    for clsA, nameA, clsB, nameB in confs:
        try:
            gs = create_initial_game_state(clsA, nameA, clsB, nameB)

            engine = GameEngine(gs)
            winning_player = engine.run()
            print(winning_player.__class__.__name__, 'won the game!')

        except KeyboardInterrupt:
            import sys
            sys.exit(0)
        except Exception as ex:
            print(traceback.format_exc())
            print('Exception occurred')
            continue


if __name__ == '__main__':
    # main_normal_game()
    main()
