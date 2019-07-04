
class GameState(object):

    def __init__(self, player_A, player_B, curr_step):
        self.player_A = player_A
        self.player_B = player_B
        self.current_player = None  # player_A.name or player_B.name
        self.step_no = None  # current game step number

    def is_terminal_state(self):
        pass