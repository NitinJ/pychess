class Square(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.piece = 0
        self.color = color
    def __repr__(self):
        piece = self.piece.get_code() if self.piece else "--"
        return piece
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def get_piece(self):
        return self.piece
    def set_piece(self, piece):
        self.piece = piece
    def get_color(self):
        return self.color