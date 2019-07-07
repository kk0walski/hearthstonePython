from copy import deepcopy

from game.actions import Action as actions
from game.cards import card as cards
from game.players.base import Player


class GameState(object):

    def __init__(self, cfg):
        self.player_A = Player('Pyjter', cfg)
        self.player_B = Player('Mati', cfg)
        self.step_no = 1  # current game step number

    def can_use_card(self, player, card):
        return player.already_used_mana + card.cost <= player.mana

    def isTerminal(self):
        """Check if game is over (one player lost)"""
        return self.player_A.health == 0 or self.player_B.health == 0

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

        return possibleMoves

    def takeAction(self, action):
        newState = deepcopy(self)
        actions.perform(newState)
        return newState

    def getReward(self):
        pass

    def get_players(self):
        """Returns (current_player, opponent)"""
        if self.step_no % 2 == 1:
            return self.player_A, self.player_B
        return self.player_B, self.player_A
