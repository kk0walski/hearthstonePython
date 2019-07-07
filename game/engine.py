from game.State import GameState

class GameEngine(object):
    """
    Main loop of game
    """

    def __init__(self, cfg):
        self.gameState = GameState(cfg)

    def run(self):
        while not self.gameState.isTerminal():
            pass
        # Update game state (increment stepNumber, set current player)
        # Choose player and get turn from player
        # Apply tyrn on game state
