import random

from mcts import mcts

from game.Hero import Hero
from game.State import PlayerState


class BasePlayer(Hero):

    def play_turn(self, game_state):
        pass


class RandomPlayer(BasePlayer):

    def play_turn(self, game_state):
        while True:
            possible_actions = game_state.getPossibleActions()

            pa = (*possible_actions['minion_plays'],
                  *possible_actions['minion_puts'],
                  *possible_actions['no_actions'])

            chosen_action = random.choice(pa)
            newState = game_state.takeAction(chosen_action)

            return newState


class MCTSPlayer(BasePlayer):

    def play_turn(self, game_state):
        mctsAI = mcts(timeLimit=1000)
        player, oponent = game_state.get_players()
        playerState = PlayerState(player, game_state)
        bestAction = mctsAI.search(initialState=playerState)
        newState = game_state.takeAction(bestAction)

        return newState
