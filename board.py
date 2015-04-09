import square
import piece
from pprint import pprint

class Board(object):
    white = 0
    black = 1
    def __init__(self, n, m):
        self.rows = n
        self.cols = m
        self._built_board()

    def _built_board(self):
        raise NotImplementedError("Need implementation of this method")

    def bounds(self, x, y):
        if x >= 0 and x < self.cols and y >= 0 and y < self.rows:
            return True
        else:
            return False

    '''
    Takes an array of squares which got changed.
    Updates kings' location incase their location got changed
    '''
    def _update_kings(self, squares):
        for _square in squares:
            if _square.get_piece() and _square.get_piece().get_name() == "King":
                self.kings[_square.get_piece().get_color()] = _square

    '''
    Move a piece from start_square to end_square
    Internally updates the location of both kings
    '''
    def move_piece(self, start_square, end_square):
        # if not start_square.get_piece():
            # print "Cannot move. NO piece present at start_square"
            # return False
        print "Moving", start_square, end_square
        # end_sq_piece = end_square.get_piece()
        end_square.set_piece(start_square.get_piece())
        end_square.get_piece().set_position(end_square)
        start_square.set_piece(0)
        self._update_kings([start_square, end_square])

    def get_kings(self):
        return self.kings

    '''
    Returns an array of squares which hold pieces of the given player
    '''
    def get_pieces(self, player):
        result = []
        for i in xrange(0, self.rows):
            for j in xrange(0, self.cols):
                _square = self.board[i][j]
                piece = _square.get_piece()
                if piece and piece.get_color() == player:
                    result.append(_square)
        return result

    def get_square(self, x, y):
        if not self.bounds(x,y):
            raise Exception("Out of board bounds exception")
        return self.board[x][y]

    def set_square(self, x, y, square):
        if not self.bounds(x,y):
            raise Exception("Out of board bounds exception")
        self.board[x][y].set_piece(square.get_piece())
        print "Set board", x, y, square
        self._update_kings([square])

    def print_board(self):
        pprint(self.board)

class BasicBoard(Board):
    def __init__(self):
        super(BasicBoard, self).__init__(8,8)
        self.kings = [self.board[0][3], self.board[7][4]]

    def _built_board(self):
        colors = ["white", "black"]*(self.cols+2)
        self.board = [[square.Square(i,j,colors[j+i%2]) for j in range(self.cols)] for i in range(self.rows)]
        # Black pieces
        # Rook, Knight, Bishop, King, Queen, Pawns
        self.board[0][0].set_piece(piece.Rook  (self.board[0][0], Board.black))
        self.board[0][7].set_piece(piece.Rook  (self.board[0][7], Board.black))
        self.board[0][1].set_piece(piece.Knight(self.board[0][1], Board.black))
        self.board[0][6].set_piece(piece.Knight(self.board[0][6], Board.black))
        self.board[0][2].set_piece(piece.Bishop(self.board[0][2], Board.black))
        self.board[0][5].set_piece(piece.Bishop(self.board[0][5], Board.black))
        self.board[0][3].set_piece(piece.King  (self.board[0][3], Board.black))
        self.board[0][4].set_piece(piece.Queen (self.board[0][4], Board.black))
        for j in xrange(0, self.cols):
            self.board[1][j].set_piece(piece.Pawn(self.board[1][j], Board.black))
        # White pieces
        # Rook, Knight, Bishop, King, Queen, Pawns
        self.board[7][0].set_piece(piece.Rook  (self.board[7][0], Board.white))
        self.board[7][7].set_piece(piece.Rook  (self.board[7][7], Board.white))
        self.board[7][1].set_piece(piece.Knight(self.board[7][1], Board.white))
        self.board[7][6].set_piece(piece.Knight(self.board[7][6], Board.white))
        self.board[7][2].set_piece(piece.Bishop(self.board[7][2], Board.white))
        self.board[7][5].set_piece(piece.Bishop(self.board[7][5], Board.white))
        self.board[7][4].set_piece(piece.King  (self.board[7][4], Board.white))
        self.board[7][3].set_piece(piece.Queen (self.board[7][3], Board.white))
        for j in xrange(0, self.cols):
            self.board[6][j].set_piece(piece.Pawn(self.board[6][j], Board.white))
        self.kings = [self.board[0][3],self.board[7][4]]

class FarziBoard(Board):
    def __init__(self):
        super(FarziBoard, self).__init__(8,8)
        self.kings = [self.board[7][7], self.board[0][0]]

    def _built_board(self):
        colors = ["white", "black"]*(self.cols+2)
        self.board = [[square.Square(i,j,colors[j+i%2]) for j in range(self.cols)] for i in range(self.rows)]
        # Black pieces
        self.board[0][0].set_piece(piece.King  (self.board[0][0], Board.black))
        # White pieces
        self.board[7][7].set_piece(piece.King  (self.board[7][7], Board.white))
        self.board[0][2].set_piece(piece.Rook  (self.board[0][2], Board.white))
        self.board[2][0].set_piece(piece.Rook  (self.board[2][0], Board.white))
        self.board[4][0].set_piece(piece.Queen (self.board[4][0], Board.white))
        self.kings = [self.board[7][7], self.board[0][0]]

if __name__=="__main__":
    b = FarziBoard()
    b.print_board()
    print b.get_pieces(Board.white)