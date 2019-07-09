import traceback

from game.State import GameState
from game.actions import Action as action
from game.engine import GameEngine
from game.players.agents import random, mcts


def create_initial_game_state(clsA, nameA, clsB, nameB):
    player_A = clsA(nameA)
    player_B = clsB(nameB)
    curr_step = 0

    return GameState(player_A, player_B, curr_step)


def prepare_game(game_state):
    for _ in range(3):
        action.take_card(game_state.player_A)

    for _ in range(4):
        action.take_card(game_state.player_B)


def main():
    confs = [
        (mcts.MCTSPlayer, 'MCTSPlayer', random.RandomPlayer, 'RandomPlayer'),
        (random.RandomPlayer, 'RandomPlayer', mcts.MCTSPlayer, 'MCTSPlayer'),
    ]
    for clsA, nameA, clsB, nameB in confs:
        try:
            gs = create_initial_game_state(clsA, nameA, clsB, nameB)
            prepare_game(gs)

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
