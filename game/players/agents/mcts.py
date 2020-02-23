from mcts import mcts

from game.State import MCTSState
from game.players.Player import BasePlayer


class MCTSPlayer(BasePlayer):

    def __init__(self, name):
        super(MCTSPlayer, self).__init__(name)

    def play_turn(self, game_state):
        mctsAI = mcts(timeLimit=20000)
        player, oponent = game_state.get_players()
        playerState = MCTSState(player, game_state)
        bestAction = mctsAI.search(initialState=playerState)

        print(str(self.name) + " " + str(bestAction))

        newPlayerState = playerState.takeAction(bestAction)
        newState = newPlayerState.state

        return newState
