from mcts import mcts
import sys

from game.State import AggressiveState
from game.actions.Action import PutMinion, PlayMinion, EndTurn
from game.players.Player import BasePlayer


attackHeroMul = 100
attackMinionMul = 10
cardsMul = 10
deadlyShotMul = 3
endRoundMul = 1

class AggressivePlayer(BasePlayer):

    def __init__(self, name):
        super(AggressivePlayer, self).__init__(name)

    def play_turn(self, game_state):
        player, oponent = game_state.get_players()
        playerState = AggressiveState(player, game_state)
        return self.policy(playerState)

    def policy(self, playerState):
        while not playerState.isTerminal():
            bestFound = None
            bestFoundValue = -sys.maxsize -1
            for action in playerState.getPossibleActions():
                currentValue = self.evaluateMove(playerState, action)
                if currentValue > bestFoundValue:
                    bestFound = action
                    bestFoundValue = currentValue

            print(str(self.name) + " " + str(bestFound))
            playerState = playerState.takeAction(bestFound)
            if not isinstance(bestFound, EndTurn):
                print(playerState.state)
            
        return playerState.state

    def evaluateMove(self, state, move):
        boardSize = 1 if len(state.hero.minions) == 0 else len(state.hero.minions)
        newState = state.takeAction(move)
        mark = newState.getReward()
        if isinstance(move, PlayMinion):
            if(move.target_idx == -1):
                card = move.getCard(state)
                return  attackHeroMul * card.attack - (1/boardSize)*cardsMul + mark
            else:
                card = move.getCard(state)
                return attackMinionMul * card.attack - card.cost + (1 / boardSize) * cardsMul + mark
        if isinstance(move, PutMinion):
            card = move.getCard(state)
            return attackMinionMul * card.attack - card.cost + (1 / boardSize) * cardsMul + mark
        if isinstance(move, EndTurn):
            return endRoundMul