"""Player module"""

class Player(object):
    """
    Health
    Mana points

    Cards
    Minions
    """
    def __init__(self, name, cfg):
        self.name = name
        self.health = cfg.INITIAL_HEALTH
        self.mana = cfg.INITIAL_MANA
        self.minions = []
        self.cfg = cfg

    def is_dead(self):
        return self.health <= 0

    def play_turn(self, game_state):
        """This method should be implemented in classes, which inherit
        from this one. Here the actual actions should be chosen and
        packed into a Turn object."""
        pass

    def __hash__(self):
        return hash((self.name, self.health, self.mana, tuple(self.minions)))

    def __eq__(self, other):
        if isinstance(other, Player):
            return hash(self) == hash(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        plr_str  = "Player: {name}; Health: {current_health}/{max_health}; " \
            "Mana: {current_mana}/{max_mana}; " \
            "Minions: {minions}"

        return plr_str.format(name=self.name,
                              current_health=self.health,
                              max_health=self.cfg.INITIAL_HEALTH,
                              current_mana=self.mana,
                              max_mana=self.cfg.INITIAL_MANA,
                              minions=self.minions)