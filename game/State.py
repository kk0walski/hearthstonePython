from copy import deepcopy

from game.Hero import Hero
from game.actions import Action as actions
from game.cards import card as cards


class GameState(object):

    def __init__(self, nameA, nameB, cfg):
        self.player_A = Hero(nameA, cfg)
        self.player_B = Hero(nameB, cfg)
        self.curr_step = 1


    def can_use_card(self, player, card):
        return player.already_used_mana + card.cost <= player.mana

    def isTerminal(self):
        """Check if game is over (one player lost)"""
        return self.player_A.is_dead() or self.player_B.is_dead()

    def get_winning_player(self):
        """Return player that won the game"""

        if self.player_A.is_dead():
            return self.player_B
        elif self.player_B.is_dead():
            return self.player_A

        assert not self.is_terminal_state()
        raise ValueError('Do not call get_winning_player '
                         'before terminal state')

    def getPossibleActions(self):

        possibleMoves = []

        player, opponent = self.get_players()

        for idx, card in enumerate(player.cards):
            if not self.can_use_card(player, card):
                continue

            # Play minion cards
            if isinstance(card, cards.MinionCard):
                possibleMoves.append(actions.PutMinion(idx))

        # Play minion (attack)
        for idx, minion in enumerate(player.minions):
            if not minion.can_attack:
                continue

            for target_idx in (-1, *list(range(len(opponent.minions)))):
                possibleMoves.append(actions.PlayMinion(idx, target_idx))

        possibleMoves.append(actions.EndTurn())

        return possibleMoves

    def takeAction(self, action):
        newState = deepcopy(self)
        action.perform(newState)
        return newState

    def getReward(self):
        pass

    def get_players(self):
        """Returns (current_player, opponent)"""
        if self.step_no % 2 == 1:
            return self.player_A, self.player_B
        return self.player_B, self.player_A

    def __repr__(self):
        return "GameState"

    def __hash__(self):
        return hash((self.player_A, self.player_B, self.curr_step))

    def __eq__(self, other):
        if isinstance(other, GameState):
            return hash(self) == hash(other)
            # return self.player_A == other.player_A and \
            #        self.player_B == other.player_B and \
            #        self.curr_step == other.curr_step
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
