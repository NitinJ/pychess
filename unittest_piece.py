from square import Square
from piece import *

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