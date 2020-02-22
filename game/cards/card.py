class Card(object):
    """Base class for all cards
    """

    def __init__(self):
        pass

    def apply(self, game_state, source, target):
        """
            This method should be implemented in all classes, which inherit from
            this class. It should take the current game state, perform a deepcopy,
            modify the copy (according to the effect of the actual card) and return
            the modified game state.

            :param game_state: current game state, should NOT be modified directly
            :param source: the player which called this card
            :param target: the targeted player or enemy minion (if a card does not
                            need a target - like updating the stats of the current
                            player, then assume that "target = None")
            :return: modified copy of input game state
        """
        pass


class MinionCard(Card):

    def __init__(self, name, health, attack, cost):
        self.name = name
        self.health = health
        self.attack = attack
        self.cost = cost
        self.can_attack = True

    def apply(self, game_state, source, target):
        from game.Hero import Hero

        # Perform attack
        if isinstance(target, Hero):
            target.health -= self.attack
        elif isinstance(target, MinionCard):
            target.health -= self.attack
            self.health -= target.attack
        else:
            raise ValueError('Target not defined or not recognized!')

    def __repr__(self):
        return str((self.name, self.health, self.attack, self.can_attack))

    def __hash__(self):
        return hash((self.name, self.health, self.attack, self.can_attack))

    def __eq__(self, other):
        if isinstance(other, MinionCard):
            return hash(self) == hash(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
