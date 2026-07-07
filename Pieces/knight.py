from piece import Piece

class Knight(Piece):
    def __init__(self, colour, pos):
        super().__init__(colour, pos, "N")
    
    def get_legal_moves(self, board):
        legal_moves = []
        row, col = self.pos
        offsets = [(-2, -1), (-2, 1),
                   (-1, -2), (-1, 2),
                   (1, -2), (1, 2),
                   (2, -1), (2, 1)]
        for offset in offsets:
            pos = (row + offset[0], col + offset[1])
            if board.within_board(pos) and (board.is_empty(pos) or board.is_enemy(pos, self.colour)):
                legal_moves.append(pos)
        
        return legal_moves

