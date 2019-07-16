from mcts import mcts

from game.State import AggressiveState
from game.players.Player import BasePlayer


class AggressivePlayer(BasePlayer):

    def __init__(self, name):
        super(AggressivePlayer, self).__init__(name)

    def play_turn(self, game_state):
        mctsAI = mcts(timeLimit=2000)
        player, oponent = game_state.get_players()
        playerState = AggressiveState(player, game_state)
        bestAction = mctsAI.search(initialState=playerState)

        print(bestAction)

        newPlayerState = playerState.takeAction(bestAction)
        newState = newPlayerState.state

        return newState
