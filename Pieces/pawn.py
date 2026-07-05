class Pawn(Piece):
    def __init__(self, colour, pos):
        super().__init__(colour, pos, "P")

    def get_legal_moves(self, board):
        legal_moves = []
        direction = 1 if self.colour == "b" else -1
        row, col = self.pos
        move_1 = (row + direction, col) 
        move_2 = (row + 2*direction, col)
        #Forward Movement
        if board.within_board(move_1) and board.is_empty(move_1):
            legal_moves.append(move_1)
            if board.within_board(move_2) and board.is_empty(move_2) and not self.has_moved:
                legal_moves.append(move_2)
        #Diagonal Movement (Piece Capture)
        if board.within_board((row + direction, col + 1)) and board.is_enemy((row + direction, col + 1), self.colour):
            legal_moves.append((row + direction, col + 1))
        if board.within_board((row + direction, col -1)) and board.is_enemy((row + direction, col - 1), self.colour):
            legal_moves.append((row + direction, col - 1))
        
        return legal_moves