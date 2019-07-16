import random

from game.State import PlayerState
from game.players.Player import BasePlayer


class RandomPlayer(BasePlayer):

    def __init__(self, name):
        super(RandomPlayer, self).__init__(name)

    def play_turn(self, game_state):
        player, oponent = game_state.get_players()
        playerState = PlayerState(player, game_state)
        possible_actions = playerState.getPossibleActions()
        chosen_action = random.choice(possible_actions)

        print(chosen_action)

        newPlayerState = playerState.takeAction(chosen_action)
        newState = newPlayerState.state

        return newState
