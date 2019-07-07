from game.players import Player

class GameState(object):

    def __init__(self, cfg):
        self.player_A = Player('Pyjter', cfg)
        self.player_B = Player('Mati', cfg)
        self.current_player = None  # player_A.name or player_B.name
        self.step_no = None  # current game step number

    def isTerminal(self):
        """Check if game is over (one player lost)"""
        return self.player_A.health == 0 or self.player_B.health == 0

    def getPossibleActions(self):
        pass

    def takeAction(self, action):
        pass

    def getReward(self):
        pass
