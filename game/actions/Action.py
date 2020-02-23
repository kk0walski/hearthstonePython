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

    def getCard():
        """Get Card"""
        return None


def increment_mana(player):
    if player.turn_number <= cfg.MAX_MANA:
        player.mana = player.turn_number


def take_card(player):
    if player.deck:
        player.hand.append(player.deck.pop())
    else:
        player.health -= 1

class PutMinion(Action):

    def __init__(self, minion_indx, name):
        self.minion = minion_indx
        self.name = name

    def perform(self, game_state):
        player, _ = game_state.get_players()
        # Get minion
        minion = player.hand[self.minion]
        minion.can_attack = False
        player.minions.append(minion)
        player.hand.remove(minion)
        player.mana -= minion.cost

    def getCard():
         player, _ = game_state.get_players()
         minion = player.hand[self.minion]
         return minion

    def __repr__(self):
        return "PUT_MINION " + str(self.name)


class PlayMinion(Action):

    def __init__(self, minion_idx, target_idx, minion_name, target_name):
        self.minion_idx = minion_idx
        self.target_idx = target_idx
        self.minion_name = minion_name
        self.target_name = target_name

    def perform(self, game_state):
        player, opponent = game_state.get_players()

        if self.target_idx == -1:
            target = opponent
        else:
            target = opponent.minions[self.target_idx]

        minion = player.minions[self.minion_idx]
        minion.apply(game_state, player, target)
        if minion.health <= 0:
            del player.minions[self.minion_idx]

        if self.target_idx != -1 and opponent.minions[self.target_idx].health <= 0:
            del opponent.minions[self.target_idx]

        minion.can_attack = False

    def getCard():
        player, _ = game_state.get_players()
        minion = player.minions[self.minion_idx]

    def __repr__(self):
        return "ATTACK_MINION " + str(self.minion_name) + " ON: " + str(self.target_name)


class EndTurn(Action):

    def perform(self, game_state):
        _, oponent = game_state.get_players()
        oponent.turn_number += 1
        increment_mana(oponent)
        take_card(oponent)
        oponent.already_given_mana += 1
        for minion in oponent.minions:
            minion.can_attack = True
        game_state.curr_step += 1

    def __repr__(self):
        return "END_TURN"
