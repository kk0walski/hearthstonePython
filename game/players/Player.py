class BasePlayer(object):

    def __init__(self, name, state):
        self.name = name
        self.state = state

    def play_turn(self):
        pass

    def getHero(self):
        if self.state.player_A.name == self.name:
            return self.state.player_A
        elif self.state.player_B.name == self.name:
            return self.state.player_B
        else:
            return None
