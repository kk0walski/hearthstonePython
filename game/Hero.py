import game.config as cfg
from game.cards.availableCards import get_all_available_cards


class Hero(object):
    """
    Health
    Mana points

    Cards
    Minions
    """

    def __init__(self, name, mana=cfg.INITIAL_MANA, health=cfg.INITIAL_HEALTH):
        self.name = name
        self.health = health
        self.mana = mana
        self.deck = get_all_available_cards()
        self.already_given_mana = mana
        self.minions = []
        self.cards = []
        self.turn_number = 0

    def is_dead(self):
        return self.health <= 0

    def __hash__(self):
        return hash((self.name, self.health, self.mana, tuple(self.minions)))

    def __eq__(self, other):
        if isinstance(other, Hero):
            return hash(self) == hash(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        plr_str = "Player: {name}; Health: {current_health}/{max_health}; " \
                  "Mana: {current_mana}/{max_mana}; " \
                  "Minions: {minions}"

        return plr_str.format(name=self.name,
                              current_health=self.health,
                              max_health=cfg.INITIAL_HEALTH,
                              current_mana=self.mana,
                              max_mana=cfg.INITIAL_MANA,
                              minions=self.minions)
