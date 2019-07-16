import game.config as cfg
from game.State import GameState
from game.cards.availableCards import get_all_available_cards
from game.players.Player import BasePlayer


def test_player_init():
    player = BasePlayer("TEST")
    cards = get_all_available_cards()
    assert player.deck == cards
    assert player.name == "TEST"
    cards[0].name = "TEST_CARD"
    assert player.deck != cards
    assert player.mana == cfg.INITIAL_MANA
    assert player.health == cfg.INITIAL_HEALTH


def test_state():
    player1 = BasePlayer("FIRST")
    player2 = BasePlayer("SECOND")
    state = GameState(player1, player2, curr_step=1)
    assert player1, player2 == state.get_players()
    possibleActions = state.get_possible_actions()
    assert possibleActions['minion_puts'] != []
    assert possibleActions['minion_plays'] == []
    assert len(possibleActions['end_turn']) == 1
    assert len(player1.cards) == 4
    assert len(player2.cards) == 4
    chosenAction = possibleActions['end_turn'][0]
    state = state.takeAction(chosenAction)
    assert player1, player2 != state.get_players()
    player, oponent = state.get_players()
    assert oponent.name == player1.name
    assert len(oponent.cards) == len(player1.cards)
    assert len(player.cards) == len(player2.cards) + 1
