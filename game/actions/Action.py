import game.config as cfg


class Action(object):
    """
    Single action like:
        * take card from deck (always forced; if no cards in deck,
                               loose health points)
        * play minion card (attack; against whom?)
        * put minion on field (max. 7 on field)
    """

    def perform(self, game_state):
        """Perform action"""
        pass


def increment_mana(player):
    if player.mana < cfg.MAX_MANA:
        player.mana += 1


def take_card(player):
    if player.deck:
        player.cards.append(player.deck.pop())
    else:
        player.health -= 1

class PutMinion(Action):

    def __init__(self, card_indx):
        self.card = card_indx

    def perform(self, game_state):
        player, _ = game_state.get_players()
        print("PUT_MINION: " + player.cards[self.card])
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

        print("ATTACK_MINION " + player.minions[self.minion] + " ON: " + target)
        minion = player.minions[self.minion]
        minion.apply(game_state, player, target)
        minion.can_attack = False


class EndTurn(Action):

    def perform(self, game_state):
        _, oponent = game_state.get_players()
        increment_mana(oponent)
        take_card(oponent)
        oponent.already_given_mana += 1
        for minion in oponent.minions:
            minion.can_attack = True
        game_state.curr_step += 1
        print("END_TURN")
