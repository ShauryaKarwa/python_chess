from Pieces.piece import Piece
from Pieces.rook import Rook

class King(Piece):
    def __init__(self, colour, pos):
        super().__init__(colour, pos, "K")
    
    def get_legal_moves(self, board):
        legal_moves = []

        row, col = self.pos
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1), (1, -1), (1, 1)]

        for direction in directions:
            move = (row + direction[0], col + direction[1])
            if board.within_board(move):
                if board.is_empty(move) or board.is_enemy(move, self.colour):
                    legal_moves.append(move)

        #Castling (King side)
        rook_king = board.get_piece((self.pos[0], self.pos[1] + 3))
        if not self.has_moved and isinstance(rook_king, Rook) and not rook_king.has_moved:
            path_empty = True
            for i in range(1, 3):
                if board.get_piece((self.pos[0], self.pos[1] + i)) is not None:
                    path_empty = False
                    break
            if path_empty:
                castling_move = (self.pos[0], self.pos[1] + 2)
                legal_moves.append(castling_move)
                
        #Castling (Queen side)
        rook_queen = board.get_piece((self.pos[0], self.pos[1] - 4))
        if not self.has_moved and isinstance(rook_queen, Rook) and not rook_queen.has_moved:
            path_empty = True
            for i in range(1, 4):
                if board.get_piece((self.pos[0], self.pos[1] - i)) is not None:
                    path_empty = False
                    break
            if path_empty:
                castling_move = (self.pos[0], self.pos[1] - 2)
                legal_moves.append(castling_move)
                
        
        
        return legal_moves