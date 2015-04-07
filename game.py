import board
import move
from copy import deepcopy

class Game(object):
    # Players
    white = 0
    black = 1
    pnone = 2
    # Game state
    not_started = 0
    started = 1
    over = 2
    draw = 3
    # Output status
    success = 1
    failure = 2
    # Output text codes
    out_of_bounds = "Start or end positions are out of board bounds"
    invalid_player = "Not current player's move"
    already_over = "Game is already over"
    success_move = "Move successfully completed"
    invalid_move = "Invalid move"

    def __init__(self):
        self.turn = Game.white
        self.other = Game.black
        self.board = board.BasicBoard()
        self.game_state = Game.not_started
        self.players = [{'check':0}, {'check':0}]
        self.history = []
        self.history_output = []
        self.board.print_board()
        self.winner = Game.pnone

    '''
    Returns if a path is clear for movement
    Returns False if there is a piece in between
    Retruns True otherwise
    '''
    def _path_clear(self, path):
        for pos in path:
            if self.board.board[pos[0]][pos[1]].piece() != 0:
                # There is a piece in between
                return False
        return True

    '''
    Checks if a player's king is getting a check
    '''
    def _king_getting_checked(self, player, enemy):
        king_square = self.board.get_kings()[player]
        enemy_piece_squares = self.board.get_pieces(enemy)
        for enemy_piece_square in enemy_piece_squares:
            possible, moves = self._find_move(enemy_piece_square, king_square)
            if possible and self._path_clear(moves[1:-1]):
                return True
        return False

    '''
    Check if enemy player's king is getting checkmated
    '''
    def _checkmate(self):
        enemy_piece_squares = self.board.get_pieces(self.other)
        for piece_square in enemy_piece_squares:
            # Move this piece to all possible locations
            for row in self.board.board:
                for square in row:
                    self._make_move(piece_square, square)
                    if not self._king_getting_checked(self.other, self.turn):
                        return False
                    self._undo_move()
        return True

    '''
    Returns current state
    '''
    def _get_state_backup(self):
        return deepcopy(self.players)

    '''
    Restores backed up state
    '''
    def _set_state_from_backup(self, state):
        self.players = state

    '''
    Game over function
    '''
    def _game_over(self):
        self.game_state = Game.over
        self.winner = self.turn
        return {'winner': self.turn}

    '''
    Makes a move
    1. Checks for validity of the move
    2. Backups the current state and records the move in history
    3. Makes the move
    Returns true if move is valid otherwise False
    '''
    def _make_move(self, move):
        if not self._validate_move(move):
            return False, {}
        move_copy = deepcopy(move)
        self.board.move_piece(move.start, move.end)
        if self._king_getting_checked(self.turn, self.other):
            self._undo_move()
            return False, {}
        if self._king_getting_checked(self.other, self.turn):
            self.players[self.other] = {'checked': 1}
        old_state = self._get_state_backup()
        self.history.append([move_copy, old_state])
        return True, {'start': (move.start.getx(), move.start.gety()), 'end': (move.end.getx(), move.end.gety()), 'killed':move.attack}

    '''
    Undos the last move done
    1. Gets last move and state from history
    2. Replaces the square objects stored at specific board co-ordinates and restores state object
    '''
    def _undo_move(self):
        if len(self.history) <= 0:
            return
        _move, state = self.history[-1]
        self.history.pop()
        self._set_state_from_backup(state)
        self.board.set_square(_move.start.getx(), _move.start.get(), _move.start)
        self.board.set_square(_move.end.getx(), _move.end.get(), _move.end)

    '''
    Checks if a piece at starting_square(Square) can be moved to ending_square(Square)
    Does not check if the correct player is making the move or not
    Generic function to check if starting piece can be moved to ending square
    '''
    def _find_move(self, start_square, end_square):
        if start_square == end_square:
            return False, 0, []
        if start_square.get_piece() == 0:
            # There is no piece at start
            return False, 0, []
        piece_at_other_end = end_square.get_piece()
        possible = False
        positions = []
        attack = 0
        if piece_at_other_end != 0:
            # Piece at other end is not 0
            if piece_at_other_end.get_color() == start_square.get_piece().get_color():
                # Piece at other end is of the same player
                return False
            else:
                # Piece at other end is of the other player
                possible, positions = start_square.get_piece().amove((start_square.getx(), start_square.gety()), (end_square.getx(), end_square.gety()))
                attack = 1
        else:
            # There is not piece at end
            possible, positions = start_square.get_piece().move((start_square.getx(), start_square.gety()), (end_square.getx(), end_square.gety()))
        return possible, attack, positions

    '''
    Validates if a move is valid or not
    1. Make sure that the piece being moved belongs to the player who is moving interface
    2. Check if its possible to move to the target location(Check if path is empty, no other pieces lie in path)
    3. Make the move(Changes internal structure and takes a backup of state, records the move in history)
    4. Check if current player's king is getting checked due to this move. If yes then undo the move and return False
    5. Check if enemy King is getting check/checkmated. In case of check set appropriate flags, in case of checkmate set flags and end game
    '''
    def _validate_move(self, move):
        # Check if moving correct piece
        if move.piece() != self.turn:
            return False

        possible, attack, positions = self._find_move(move.start, move.end)
        move.attack = attack
        if not possible:
            return False

        # Exclude starting & ending point and check if path is fine
        positions = positions[1:-1]
        if not self._path_clear(positions):
            # There is a piece in the path
            return False

        # Path is fine move can be done
        self._make_move(move)

        # Check if current king is getting check due to the move
        if self._king_getting_checked(self.turn, self.other):
            self._undo_move()
            return False

        # Check if other king is getting checkmated
        if self._checkmate():
            # Current player wins!
            self.game_state = Game.over
            pass
        if self._king_getting_checked(self.other, self.turnf):
            self.players[self.other] = {'checked':1}
            pass
        return True


    '''
    Public interface for making a move
    Player = player making the move
    start = starting co-ordinates of the piece
    end = Desired co-ordinates of the piece
    '''
    def make_move(self, player, start, end):
        if not board.bounds(start[0], start[1]) or not board.bounds(end[0], end[1]):
            return {'status': Game.failure, 'status_code': Game.out_of_bounds, 'checkinfo': self.players}
        if player != self.turn:
            return {'status': Game.failure, 'status_code': Game.invalid_player, 'checkinfo': self.players}
        if self.game_state == Game.over or self.game_state == Game.draw:
            return {'status': Game.failure, 'status_code': Game.already_over, 'checkinfo': self.players}
        current_move = move.Move(self.turn, self.board.get_square(start[0], start[1]), self.board.get_square(end[0], end[1]))
        possible, output = self._make_move(current_move)
        if not possible:
            return {'status': Game.failure, 'status_code': Game.invalid_move, 'checkinfo': self.players}
        if self._checkmate():
            output = self._game_over()
        return {'status': Game.success, 'status_code': Game.success_move, 'checkinfo': self.players, 'outupt':output}

if __name__=="__main__":
    g = Game()