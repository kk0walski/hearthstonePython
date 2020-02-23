from abc import ABC, abstractmethod
from copy import deepcopy

from game import config
from game.actions.Action import PlayMinion, PutMinion, EndTurn, take_card
from game.cards import card as cards


class GameState(object):

    def __init__(self, playerA, playerB, curr_step=1):
        self.player_A = playerA
        self.player_B = playerB
        self.player_A.mana += 1
        self.player_A.turn_number += 1

        for _ in range(4):
            take_card(playerA)
            take_card(playerB)

        self.curr_step = curr_step

    def can_use_card(self, player, card):
        return card.cost <= player.mana

    def isTerminal(self):
        """Check if game is over (one player lost)"""
        return self.player_A.is_dead() or self.player_B.is_dead()

    def get_winning_player(self):
        """Return player that won the game"""

        if self.player_A.is_dead():
            return self.player_B
        elif self.player_B.is_dead():
            return self.player_A

        assert not self.isTerminal()
        raise ValueError('Do not call get_winning_player '
                         'before terminal state')

    def get_possible_actions(self):
        actions = {
            'minion_puts': [],
            'attack_player': [],
            'attack_minion': [],
            'end_turn': []
        }

        player, opponent = self.get_players()

        for idx, card in enumerate(player.hand):
            if not self.can_use_card(player, card):
                continue

            # Put minion cards
            elif isinstance(card, cards.MinionCard):
                actions['minion_puts'].append(
                    PutMinion(idx, card.name)
                )

        # Play minion (attack)
        for idx, minion in enumerate(player.minions):
            if not minion.can_attack:
                continue

            for target_idx in (-1, *list(range(len(opponent.minions)))):
                if target_idx == -1:
                    actions['attack_player'].append(
                        PlayMinion(idx, target_idx, player.minions[idx].name, opponent.name)
                    )
                else:
                    actions['attack_minion'].append(
                        PlayMinion(idx, target_idx, player.minions[idx].name, opponent.minions[target_idx].name)
                    )

        actions['end_turn'].append(EndTurn())

        return actions

    def takeAction(self, action):
        newState = deepcopy(self)
        action.perform(newState)
        return newState


    def get_players(self):
        """Returns (current_player, opponent)"""
        if self.curr_step % 2 == 1:
            return self.player_A, self.player_B
        return self.player_B, self.player_A

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

    def __repr__(self):
        return str((self.player_A, self.player_B, self.curr_step))


class PlayerState(ABC):

    def __init__(self, hero, state, initialState=None):
        self.hero = hero
        self.state = state
        if not initialState:
            self.initialState = deepcopy(state)
        else:
            self.initialState = initialState

    def getPossibleActions(self):
        """

        :rtype: object
        """
        reasult = []
        possible_actions = self.state.get_possible_actions().values()
        for item in possible_actions:
            reasult.extend(item)
        return reasult

    def getPossibleActionsDict(self):
        return self.state.get_possible_actions()

    def getOponent(self, my_state):
        if my_state.player_A.name == self.hero.name:
            return my_state.player_B
        else:
            return my_state.player_A

    @abstractmethod
    def takeAction(self, action):
        pass


class MCTSState(PlayerState):

    def __init__(self, hero, state, initialState=None):
        super(MCTSState, self).__init__(hero, state, initialState)

    def isTerminal(self):
        return self.state.isTerminal()

    def takeAction(self, action):
        return MCTSState(self.hero, self.state.takeAction(action), self.initialState)

    def getReward(self):
        return -1 if self.hero.is_dead() else 1


class TurnState(PlayerState):
    def __init__(self, hero, state, initialState=None):
        super(TurnState, self).__init__(hero, state, initialState)

    def isTerminal(self):
        return self.state.curr_step != self.initialState.curr_step


class AggressiveState(TurnState):

    def __init__(self, hero, state, initialState=None):
        super(AggressiveState, self).__init__(hero, state, initialState)

    def takeAction(self, action):
        return AggressiveState(self.hero, self.state.takeAction(action), self.initialState)

    def getReward(self):
        initialOponent = self.getOponent(self.initialState)
        oponent = self.getOponent(self.state)
        return (len(initialOponent.minions) - len(oponent.minions)) * 2 + (
                    len(self.hero.minions) - len(oponent.minions)) * 2 + (initialOponent.health - oponent.health) * 10


class ControlingState(TurnState):

    def __init__(self, hero, state, initialState=None):
        super(ControlingState, self).__init__(hero, state, initialState)

    def getPossibleActions(self):
        oponent = self.getOponent(self.state)
        reasult = []
        possible_actions = self.state.get_possible_actions()

        if len(oponent.minions) != 0:
            for key, value in possible_actions.items():
                if key != 'attack_player':
                    reasult.extend(value)
        else:
            for key, value in possible_actions.items():
                reasult.extend(value)

        return reasult

    def takeAction(self, action):
        return ControlingState(self.hero, self.state.takeAction(action), self.initialState)

    def getReward(self):
        initialOponent = self.getOponent(self.initialState)
        oponent = self.getOponent(self.state)
        if len(oponent.minions) > 0:
            return (len(initialOponent.minions) - len(oponent.minions)) * 10
        else:
            return (initialOponent.health - oponent.health)
