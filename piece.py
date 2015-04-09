from square import Square
import unittest

class Piece(object):
    def __init__(self, square, color):
        self.name = "Piece"
        self.color = color
        self.set_position(square)
        self.code = "P"
    # Methods returning feasibility of moves for simple move and attack move respectively
    def _can_move(self, start, end):
        raise NotImplementedError("Need implementation")
    def _can_amove(self, start, end):
        return self._can_move(start, end)
    # Methods returning sequence of moves for simple move and attack move respectively
    def _moves(self, start, end):
        raise NotImplementedError("Need implementation")
    def _amoves(self, start, end):
        return self._amoves(start, end)
    # Default implementation of normal move method
    def _move(self, start, end):
        if self._can_move(start, end):
            return True, self._moves(start,end)
        else:
            return False, []
    # Default implementation of attack move method
    def _amove(self, start, end):
        return self._move(start, end)
    # Public interface
    def set_position(self, square):
        self.pos = (square.getx(), square.gety())
    def amove(self, end):
        return self._amove(self.pos, end)
    def move(self, end):
        return self._move(self.pos, end)
    def get_name(self):
        return self.name
    def get_color(self):
        return self.color
    def get_code(self):
        if self.color == 0:
            return "w"+self.code
        else:
            return "b"+self.code

class King(Piece):
    def __init__(self, square, color):
        super(King, self).__init__(square, color)
        self.name = "King"
        self.code = "K"
    def _can_move(self, start, end):
        if start == end:
            return False
        x1,y1 = start
        x2,y2 = end
        if abs(x2-x1)==1 and abs(y2-y1)==1:
            return True
        else:
            return False
    def _moves(self, start, end):
        return [start,end]

class Queen(Piece):
    def __init__(self, square, color):
        super(Queen, self).__init__(square, color)
        self.name = "Queen"
        self.code = "Q"
    def _can_move(self, start, end):
        if start == end:
            return False
        x1,y1 = start
        x2,y2 = end
        if (x2-x1)==0 or (y2-y1)==0 or (abs(x2-x1)==abs(y2-y1)):
            return True
        else:
            return False
    def _moves(self, start, end):
        x1,y1 = start
        x2,y2 = end
        moves = []
        if x2-x1 == 0:
            movement = 1 if y2>=y1 else -1
            moves = [(x1,y) for y in xrange(y1,y2+movement,movement)]
        elif y2-y1 == 0:
            movement = 1 if x2>=x1 else -1
            moves = [(x,y1) for x in xrange(x1,x2+movement,movement)]
        else:
            slope = (y2-y1)/(x2-x1)
            movement = 1 if y2>=y1 else -1
            moves = [(x1+y/slope, y1+y) for y in xrange(0,y2-y1+movement,movement)]
        return moves

class Rook(Piece):
    def __init__(self, square, color):
        super(Rook, self).__init__(square, color)
        self.name = "Rook"
        self.code = "R"
    def _can_move(self, start, end):
        if start == end:
            return False
        x1,y1 = start
        x2,y2 = end
        if (x2-x1)==0 or (y2-y1)==0:
            return True
        else:
            return False
    def _moves(self, start, end):
        x1,y1 = start
        x2,y2 = end
        moves = []
        if x2-x1 == 0:
            movement = 1 if y2>=y1 else -1
            moves = [(x1,y) for y in xrange(y1,y2+movement,movement)]
        elif y2-y1 == 0:
            movement = 1 if x2>=x1 else -1
            moves = [(x,y1) for x in xrange(x1,x2+movement,movement)]
        return moves

class Knight(Piece):
    def __init__(self, square, color):
        super(Knight, self).__init__(square, color)
        self.name = "Knight"
        self.code = "K"
    def _can_move(self, start, end):
        if start == end:
            return False
        x1,y1 = start
        x2,y2 = end
        if (abs(x2-x1) + abs(y2-y1)) == 3:
            return True
        else:
            return False
    def _moves(self, start, end):
        return [start, end]

class Bishop(Piece):
    def __init__(self, square, color):
        super(Bishop, self).__init__(square, color)
        self.name = "Bishop"
        self.code = "B"
    def _can_move(self, start, end):
        if start == end:
            return False
        x1,y1 = start
        x2,y2 = end
        if abs(x2-x1) == 1 and abs(x2-x1)==abs(y2-y1):
            return True
        else:
            return False
    def _moves(self, start, end):
        x1,y1 = start
        x2,y2 = end
        slope = (y2-y1)/(x2-x1)
        movement = 1 if x2>=x1 else -1
        return [(x,slope*x) for x in xrange(x1,x2+movement,movement)]

class Pawn(Piece):
    def __init__(self, square, pawn_color):
        super(Pawn, self).__init__(square, pawn_color)
        # print pawn_color
        self.name = "White pawn" if pawn_color == 0 else "Black pawn"
        self.moved = 0
        self.color_code = -1 if pawn_color == 0 else 1
        self.code = "p"
    def _can_move(self, start, end):
        # print start,end,self.color_code
        if start == end:
            return False
        x1,y1 = start
        x2,y2 = end
        if y1==y2 and ( (x2==x1+self.color_code) or (x2==x1+2*self.color_code and not self.moved) ):
            return True
        else:
            return False
    def _can_amove(self, start, end):
        if start == end:
            return False
        x1,y1 = start
        x2,y2 = end
        if (y2==y1+1 or y2==y1-1) and x2==x1+self.color_code:
            return True
        else:
            return False
    def _moves(self, start, end):
        x1,y1 = start
        x2,y2 = end
        return [(x,y1) for x in xrange(x1,x2+self.color_code,self.color_code)]
    def _amoves(self, start, end):
        x1,y1 = start
        x2,y2 = end
        return [start, end]
    def _amove(self, start, end):
        if self._can_amove(start, end):
            return True, self._amoves(start,end)
        else:
            return False, []
    def set_position(self, square):
        self.pos = (square.getx(), square.gety())
        self.moved = 1
    def has_moved(self):
        return self.moved

if __name__=="__main__":
    from unittest_piece import *
    unittest.main()