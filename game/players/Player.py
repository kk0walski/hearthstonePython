from game.Hero import Hero


class BasePlayer(Hero):

    def __init__(self, name):
        super(BasePlayer, self).__init__(name)

    def play_turn(self, game_state):
        pass
