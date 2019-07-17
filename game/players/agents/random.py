import random

from game.State import PlayerState
from game.players.Player import BasePlayer


class RandomPlayer(BasePlayer):

    def __init__(self, name):
        super(RandomPlayer, self).__init__(name)

    def play_turn(self, game_state):
        player, oponent = game_state.get_players()
        player_state = PlayerState(player, game_state)
        possible_actions = player_state.getPossibleActions()
        chosen_action = random.choice(possible_actions)

        print(str(self.name) + " " + str(chosen_action))

        new_player_state = player_state.takeAction(chosen_action)
        new_state = new_player_state.state

        return new_state
