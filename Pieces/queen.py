from piece import Piece

class Queen(Piece):
    def __init__(self, colour, pos):
        super().__init__(colour, pos, "Q")
    
    def get_legal_moves(self, board):
        legal_moves = []

        row, col = self.pos
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1), (1, -1), (1, 1)]

        for direction in directions:
            step = 1
            while True:
                move = (row + direction[0]*step, col + direction[1]*step)
                if not board.within_board(move):
                    break
                if board.is_empty(move):
                    legal_moves.append(move)
                    step += 1
                elif board.is_enemy(move, self.colour):
                    legal_moves.append(move)
                    break
                else:
                    break

        return legal_moves