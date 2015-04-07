class Move(object):
    def __init__(self, player, start, end):
        self.player = player
        self.piece = start.get_piece()
        self.start = start
        self.end = end
        self.attack = 0