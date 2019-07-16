from mcts import mcts

from game.State import ControlingState
from game.players.Player import BasePlayer


class ControllingPlayer(BasePlayer):

    def __init__(self, name):
        super(ControllingPlayer, self).__init__(name)

    def play_turn(self, game_state):
        mctsAI = mcts(timeLimit=2000)
        player, oponent = game_state.get_players()
        playerState = ControlingState(player, game_state)
        bestAction = mctsAI.search(initialState=playerState)

        print(bestAction)

        newPlayerState = playerState.takeAction(bestAction)
        newState = newPlayerState.state

        return newState
