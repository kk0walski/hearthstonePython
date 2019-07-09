import random

from game.State import PlayerState
from game.players.Player import BasePlayer


class RandomPlayer(BasePlayer):

    def __init__(self, name):
        super(RandomPlayer, self).__init__(name)

    def play_turn(self, game_state):
        while True:
            player, oponent = game_state.get_players()
            playerState = PlayerState(player, game_state)
            possible_actions = playerState.getPossibleActions()

            pa = (*possible_actions['minion_plays'],
                  *possible_actions['minion_puts'],
                  *possible_actions['no_actions'])

            chosen_action = random.choice(pa)
            newState = playerState.takeAction(chosen_action)

            return newState
