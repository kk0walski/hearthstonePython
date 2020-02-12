import unittest

from game import config as cfg
from game.State import GameState
from game.cards.availableCards import get_all_available_cards
from game.players.Player import BasePlayer


class TestStringMethods(unittest.TestCase):

    def test_player_init(self):
        player = BasePlayer("TEST")
        cards = get_all_available_cards()
        assert set(player.deck) == set(cards)
        assert player.name == "TEST"
        cards[0].name = "TEST_CARD"
        assert player.deck != cards
        assert player.mana == cfg.INITIAL_MANA
        assert player.health == cfg.INITIAL_HEALTH


    def test_state(self):
        player1 = BasePlayer("FIRST")
        player2 = BasePlayer("SECOND")
        state = GameState(player1, player2, curr_step=1)
        assert player1, player2 == state.get_players()
        possibleActions = state.get_possible_actions()
        assert len(possibleActions['attack_player']) == len([minion for minion in player1.minions if minion.can_attack])
        assert len(possibleActions['minion_puts']) == len([card for card in player1.hand if card.cost <= player1.mana])
        assert len(possibleActions['end_turn']) == 1
        assert len(player1.hand) == 4
        assert len(player2.hand) == 4


if __name__ == '__main__':
    unittest.main()