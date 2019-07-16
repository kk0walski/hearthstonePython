from copy import deepcopy

from game import config
from game.actions.Action import PlayMinion, PutMinion, EndTurn, take_card
from game.cards import card as cards


class GameState(object):

    def __init__(self, playerA, playerB, curr_step=1):
        self.player_A = playerA
        self.player_B = playerB
        self.player_A.mana += 1

        for i in range(4):
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
            'minion_plays': [],
            'end_turn': []
        }

        player, opponent = self.get_players()

        for idx, card in enumerate(player.cards):
            if not self.can_use_card(player, card):
                continue

            # Put minion cards
            elif isinstance(card, cards.MinionCard):
                actions['minion_puts'].append(
                    PutMinion(idx)
                )

        # Play minion (attack)
        for idx, minion in enumerate(player.minions):
            if not minion.can_attack:
                continue

            for target_idx in (-1, *list(range(len(opponent.minions)))):
                actions['minion_plays'].append(
                    PlayMinion(idx, target_idx)
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
        game_state_str = "\n" \
                         "Player B {player_B_name} (mana: " \
                         "{player_B_total_mana}, " \
                         "health: {player_B_health}/{total_health})\n" \
                         "cards: {player_B_cards}\n" \
                         "Minions: {player_B_minions}\n" \
                         "==============================\n" \
                         "Minions: {player_A_minions}\n" \
                         "cards: {player_A_cards}\n" \
                         "Player A {player_A_name} (mana: " \
                         "{player_A_total_mana}, " \
                         "health: {player_A_health}/{total_health})\n" \
                         "\n"

        game_state_str = game_state_str.format(
            player_B_name=self.player_B.name,
            player_B_health=self.player_B.health,
            player_B_total_mana=self.player_B.mana,
            player_B_cards=self.player_B.cards,
            player_B_minions=self.player_B.minions,

            player_A_name=self.player_A.name,
            player_A_cards=self.player_A.cards,
            player_A_health=self.player_A.health,
            player_A_total_mana=self.player_A.mana,
            player_A_minions=self.player_A.minions,
            total_health=config.INITIAL_HEALTH
        )

        return game_state_str

class PlayerState(object):

    def __init__(self, hero, state):
        self.hero = hero
        self.state = state

    def can_use_card(self, player, card):
        return player.already_used_mana + card.cost <= player.mana

    def getPossibleActions(self):
        reasult = []
        possible_actions = self.state.get_possible_actions().values()
        for item in possible_actions:
            reasult.extend(item)
        return reasult

    def isTerminal(self):
        return self.state.isTerminal()

    def takeAction(self, action):
        return PlayerState(self.hero, self.state.takeAction(action))

    def getReward(self):
        if self.isTerminal():
            if self.hero.is_dead():
                return -1
            else:
                return 1
        else:
            return 0