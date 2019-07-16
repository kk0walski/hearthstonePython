"""Game engine"""
from copy import deepcopy

from game import config
from game.gui import StateGui


class GameEngine(object):
    """Object implementing main loop / logic of game

    Attributes:
        * game_state (GameState): the current game state
    """

    def __init__(self, game_state):
        self.game_state = game_state

    def run(self):
        while not self.game_state.isTerminal():

            game_state_cpy = deepcopy(self.game_state)

            player, _ = game_state_cpy.get_players()

            if game_state_cpy.isTerminal():
                self.game_state = game_state_cpy
                break

            # Print current game_state
            if config.VERBOSE:
                print(StateGui.prepare_state(game_state_cpy))

            new_state = player.play_turn(game_state_cpy)

            self.game_state = new_state

        winning_player = self.game_state.get_winning_player()

        if config.VERBOSE:
            print('Player {} won the game!'.format(winning_player.name))

        return winning_player
