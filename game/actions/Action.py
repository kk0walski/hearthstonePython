import game.config as cfg

class Action(object):
    """
    Single action like:
        * take card from deck (always forced; if no cards in deck,
                               loose health points)
        * play minion card (attack; against whom?)
        * put minion on field (max. 7 on field)
    """

    def perform(self):
        """Perform action"""
        pass


def increment_mana(player):
    if player.mana < cfg.MAX_MANA:
        player.mana += 1


def take_card(player):
    if not player.deck.is_empty():
        player.cards.append(player.deck.pop())
    else:
        player.deck.no_attempt_pop_when_empty += 1
        player.health -= player.deck.no_attempt_pop_when_empty

class PutMinion(Action):

    def __init__(self, card_indx):
        self.card = card_indx

    def perform(self, game_state):
        player, _ = game_state.get_players()
        # Get minion
        minion = player.cards[self.card]
        minion.can_attack = False
        player.minions.append(minion)
        player.cards.remove(minion)
        player.mana -= minion.cost


class PlayMinion(Action):

    def __init__(self, minion_idx, target_idx):
        self.minion = minion_idx
        self.target = target_idx

    def perform(self, game_state):
        player, opponent = game_state.get_players()

        if self.target == -1:
            target = opponent
        else:
            target = opponent.minions[self.target]

        minion = player.minions[self.minion]
        minion.apply(self.state, player, target)
        minion.can_attack = False
