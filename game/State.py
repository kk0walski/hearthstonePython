from game.players.base import Player

class GameState(object):

    def __init__(self, cfg):
        self.player_A = Player('Pyjter', cfg)
        self.player_B = Player('Mati', cfg)
        self.step_no = 1  # current game step number

    def isTerminal(self):
        """Check if game is over (one player lost)"""
        return self.player_A.health == 0 or self.player_B.health == 0

    def getPossibleActions(self):
        pass

    def takeAction(self, action):
        pass

    def getReward(self):
        pass

    def get_players(self):
        """Returns (current_player, opponent)"""
        if self.step_no % 2 == 1:
            return self.player_A, self.player_B
        return self.player_B, self.player_A
