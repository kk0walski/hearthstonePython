from mcts import mcts

from game.State import ControlingState
from game.players.Player import BasePlayer


class ControllingPlayer(BasePlayer):

    attackHeroMul = 10
    attackMinionMul = 100
    cardsMul = 10
    deadlyShotMul = 3
    endRoundMul = 1

    def __init__(self, name):
        super(ControllingPlayer, self).__init__(name)

    def play_turn(self, game_state):
        mctsAI = mcts(timeLimit=10000, rolloutPolicy=self.policy)
        player, oponent = game_state.get_players()
        playerState = ControlingState(player, game_state)
        bestAction = mctsAI.search(initialState=playerState)

        print(str(self.name) + " " + str(bestAction))

        newPlayerState = playerState.takeAction(bestAction)
        newState = newPlayerState.state

        return newState

    def policy(self, state):
        while not state.isTerminal():
            bestFound = None
            bestFoundValue = -sys.maxsize -1
            for action in state.getPossibleActions():
                currentValue = self.evaluateMove(state, action)
                if currentValue > bestFoundValue:
                    bestFound = action
                    bestFound = currentValue

            state = state.takeAction(bestFound)
            
        return state.getReward()

    def evaluateMove(self, state, move):
        boardSize = 1 if len(state.hero.minions) == 0 else len(state.hero.minions)
        if isinstance(move, PlayMinion):
            if(move.target_idx == -1):
                card = move.getCard()
                return  attackHeroMul * card.attack - (1/boardSize)*cardsMul
            else:
                card = move.getCard()
                return attackMinionMul * card.attack - card.cost + (1 / boardSize) * cardsMul
        if isinstance(move, PutMinion):
            card = move.getCard()
            return attackMinionMul * card.attack - card.cost + (1 / boardSize) * cardsMul
        if isinstance(move, EndTurn):
            return endRoundMul