from piece import Piece

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
        
        return legal_moves