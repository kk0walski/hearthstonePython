import unittest

from game import config as cfg
from game.State import GameState
from game.cards.availableCards import get_all_available_cards
from game.players.Player import BasePlayer
from game.cards.card import MinionCard


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.playerA = BasePlayer("FIRST")
        self.playerB = BasePlayer("SECOND")
        self.state = GameState(self.playerA, self.playerB, curr_step=1)

    def test_player_init(self):
        cards = get_all_available_cards()
        assert all(x in cards for x in self.playerA.deck)
        assert all(x in cards for x in self.playerB.deck)
        assert self.playerA.name == "FIRST"
        assert self.playerA.deck != cards
        assert self.playerA.mana == cfg.INITIAL_MANA + 1
        assert self.playerA.health == cfg.INITIAL_HEALTH
        assert len(self.playerA.hand) == 4
        assert len(self.playerA.minions) == 0
        assert self.playerB.name == "SECOND"
        assert self.playerB.deck != cards
        assert self.playerB.mana == cfg.INITIAL_MANA
        assert self.playerB.health == cfg.INITIAL_HEALTH
        assert len(self.playerB.hand) == 4
        assert len(self.playerB.minions) == 0


    def test_state(self):
        self.playerA, self.playerB == self.state.get_players()
        player1, player2 = self.state.get_players()
        possibleActions = self.state.get_possible_actions()
        assert len(possibleActions['attack_player']) == len([minion for minion in player1.minions if minion.can_attack])
        assert len(possibleActions['minion_puts']) == len([card for card in player1.hand if card.cost <= player1.mana])
        assert len(possibleActions['end_turn']) == 1


if __name__ == '__main__':
    unittest.main()