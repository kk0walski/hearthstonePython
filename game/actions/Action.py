
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


class PutMinion(Action):

    def __init__(self, card_indx, game_state):
        self.card = card_indx
        self.state = game_state

    def perform(self):
        player, _ = self.state.get_players()
        # Get minion
        minion = player.cards[self.card]
        minion.can_attack = False
        player.minions.append(minion)
        player.cards.remove(minion)
        player.mana -= minion.cost
