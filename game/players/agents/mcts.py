from mcts import mcts

from game.State import PlayerState
from game.players.Player import BasePlayer


class MCTSPlayer(BasePlayer):

    def __init__(self, name):
        super(MCTSPlayer, self).__init__(name)

    def play_turn(self, game_state):
        mctsAI = mcts(timeLimit=1000)
        player, oponent = game_state.get_players()
        playerState = PlayerState(player, game_state)
        bestAction = mctsAI.search(initialState=playerState)
        newPlayerState = playerState.takeAction(bestAction)
        newState = newPlayerState.state

        return newState
