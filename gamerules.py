import board
import square
import piece
import move

class GameRules(object):
    def __init__(self, board):
        self.board = board
    def validate(self):
        raise NotImplementedError("Provide implementation for this method")
    def gameover(self):
        raise NotImplementedError("Provide implementation for this method")
    def gamedraw(self):
        raise NotImplementedError("Provide implementation for this method")