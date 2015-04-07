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
        if self.color == "white":
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
        if (x2-x1)==0 or (y2-y1)==0 or (abs(x2-x1) == 1 and abs(x2-x1)==abs(y2-y1)):
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
            movement = 1 if x2>=x1 else -1
            moves = [(x,slope*x) for x in xrange(x1,x2+movement,movement)]
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
        self.name = "White pawn"
        self.moved = 0
        self.color_code = -1 if pawn_color == "white" else 1
        self.code = "p"
    def _can_move(self, start, end):
        if start == end:
            return False
        x1,y1 = start
        x2,y2 = end
        if x1==x2 and ( (y2==y1+self.color_code and self.moved) or (y2==y1+2*self.color_code and not self.moved) ):
            return True
        else:
            return False
    def _can_amove(self, start, end):
        if start == end:
            return False
        x1,y1 = start
        x2,y2 = end
        if x2==x1+1 and y2==y1+self.color_code:
            return True
        else:
            return False
    def _moves(self, start, end):
        x1,y1 = start
        x2,y2 = end
        return [(x1,y) for y in xrange(y1,y2+self.color_code,type)]
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

class TestKing(unittest.TestCase):
    def setUp(self):
        self.piece = King(Square(0,0,"white"), "white")
    def test_move(self):
        # Move to invalid point
        possible, moves = self.piece.move((3,1))
        self.assertEqual(possible, False)
        self.assertEqual(moves, [])
        # Move to corner +ve
        possible, moves = self.piece.move((1,1))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(0,0),(1,1)])
        # Move to same point
        possible, moves = self.piece.move((0,0))
        self.assertEqual(possible, False)
        self.assertEqual(moves, [])
    def test_name(self):
        self.assertEqual(self.piece.get_name(), "King")

class TestQueen(unittest.TestCase):
    def setUp(self):
        self.piece = Queen(Square(0,0,"white"), "white")
    def test_move(self):
        # Invalid move
        possible, moves = self.piece.move((1,3))
        self.assertEqual(possible, False)
        self.assertEqual(moves, [])
        # Corner move
        possible, moves = self.piece.move((1,1))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(0,0),(1,1)])
        # Corner move back
        possible, moves = self.piece.move((-1,-1))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(0,0),(-1,-1)])
        # Horizontal move
        possible, moves = self.piece.move((0,2))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(0,0),(0,1),(0,2)])
        # Vertical move
        possible, moves = self.piece.move((2,0))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(0,0),(1,0),(2,0)])
        # Vertical move -ve
        possible, moves = self.piece.move((-2,0))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(0,0),(-1,0),(-2,0)])
        # Move to same location
        possible, moves = self.piece.move((0,0))
        self.assertEqual(possible, False)
        self.assertEqual(moves, [])
    def test_name(self):
        self.assertEqual(self.piece.get_name(), "Queen")

class TestRook(unittest.TestCase):
    def setUp(self):
        self.piece = Rook(Square(0,0,"white"), "white")
    def test_move(self):
        # Invalid move
        possible, moves = self.piece.move((1,1))
        self.assertEqual(possible, False)
        self.assertEqual(moves, [])
        # Horizontal move +ve
        possible, moves = self.piece.move((0,2))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(0,0),(0,1),(0,2)])
        # Horizontal move -ve
        possible, moves = self.piece.move((0,-2))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(0,0),(0,-1),(0,-2)])
        # Vertical move
        possible, moves = self.piece.move((2,0))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(0,0),(1,0),(2,0)])
        # Vertical move -ve
        possible, moves = self.piece.move((-2,0))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(0,0),(-1,0),(-2,0)])
        # Move to same location
        possible, moves = self.piece.move((0,0))
        self.assertEqual(possible, False)
        self.assertEqual(moves, [])
    def test_name(self):
        self.assertEqual(self.piece.get_name(), "Rook")

class TestKnight(unittest.TestCase):
    def setUp(self):
        self.piece = Knight(Square(2,2,"white"), "white")
    def test_move(self):
        # Invalid moves
        possible, moves = self.piece.move((3,3))
        self.assertEqual(possible, False)
        self.assertEqual(moves, [])
        possible, moves = self.piece.move((31,31))
        self.assertEqual(possible, False)
        self.assertEqual(moves, [])
        possible, moves = self.piece.move((3,5))
        self.assertEqual(possible, False)
        self.assertEqual(moves, [])
        # Top right 1
        possible, moves = self.piece.move((0,3))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(2,2),(0,3)])
        # Top right 2
        possible, moves = self.piece.move((1,4))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(2,2),(1,4)])
        # Bottom right 1
        possible, moves = self.piece.move((4,3))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(2,2),(4,3)])
        # Bottom right 2
        possible, moves = self.piece.move((3,4))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(2,2),(3,4)])
        # Top left 1
        possible, moves = self.piece.move((0,1))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(2,2),(0,1)])
        # Top left 2
        possible, moves = self.piece.move((1,0))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(2,2),(1,0)])
        # Bottom left 1
        possible, moves = self.piece.move((4,1))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(2,2),(4,1)])
        # Bottom left 2
        possible, moves = self.piece.move((3,0))
        self.assertEqual(possible, True)
        self.assertEqual(moves, [(2,2),(3,0)])
        # Move to same location
        possible, moves = self.piece.move((0,0))
        self.assertEqual(possible, False)
        self.assertEqual(moves, [])
    def test_name(self):
        self.assertEqual(self.piece.get_name(), "Knight")

if __name__=="__main__":
    unittest.main()