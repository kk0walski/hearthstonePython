import random

from game.players.Player import BasePlayer


class RandomPlayer(BasePlayer):

    def __init__(self, name):
        super(RandomPlayer, self).__init__(name)

    def play_turn(self, game_state):
        while True:
            possible_actions = game_state.getPossibleActions()

            pa = (*possible_actions['minion_plays'],
                  *possible_actions['minion_puts'],
                  *possible_actions['no_actions'])

            chosen_action = random.choice(pa)
            newState = game_state.takeAction(chosen_action)

            return newState
