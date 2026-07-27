import pygame

from board import Board

from Pieces import bishop, king, knight, pawn, piece, queen, rook

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.current_turn = "w"
        self.selected_piece = None
        self.running = True

        self.board.setup()

    def handle_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = event.pos
                    self.handle_click(mouse)

    def handle_click(self, pos):
        pos = self.board.mouse_to_square(pos)
        if pos:
           piece = self.board.get_piece(pos)
           if self.selected_piece:
                legal_moves = self.get_legal_moves(self.selected_piece)

                if piece and piece.colour == self.current_turn:
                    self.selected_piece = piece
                else:
                    if pos in legal_moves:
                        self.board.move_piece(self.selected_piece, pos)
                        self.selected_piece = None
                        self.switch_turn()
                        if self.is_checkmate(self.current_turn):
                            print(f"{self.current_turn} is checkmated!")
                            self.running = False
                        elif self.is_stalemate(self.current_turn):
                            print("It's a stalemate!")
                            self.running = False
           else:
               if piece and piece.colour == self.current_turn:
                    self.selected_piece = piece
                   
    def update(self):
        pass

    def draw(self):
        colour = (255, 255, 255)
        self.screen.fill(colour)

        self.board.draw(self.screen)

        if self.selected_piece is not None:
            row, col = self.selected_piece.pos
            highlight = (255, 139, 39)
            pygame.draw.rect(self.screen, highlight, [120 + self.board.width*col, 20 + self.board.height*row, self.board.width, self.board.height], 3)

            legal_moves = self.get_legal_moves(self.selected_piece)

            for move in legal_moves:
                row_move, col_move = move
                pygame.draw.circle(self.screen, (255, 0, 0),  [155 + self.board.width*col_move, 55 + self.board.height*row_move, self.board.width, self.board.height], 20, 2)

        pygame.display.flip()

    def switch_turn(self):
        if self.current_turn == "w":
            self.current_turn = "b"
        else:
            self.current_turn = "w"

    def is_in_check(self, colour):
        if self.board.find_king(colour) is None:
            raise ValueError(f"No {colour} king found on the board.")
        pos = self.board.find_king(colour).pos
        for row in self.board.grid:
            for piece in row:
                if piece is not None and piece.colour != colour:
                    moves = piece.get_legal_moves(self.board)
                    if pos in moves:
                        return True
        return False

    def is_move_safe(self, piece, destination):
        crow, ccol = piece.pos
        target_piece = self.board.get_piece(destination)
        trow, tcol = destination

        self.board.grid[crow][ccol] = None
        self.board.grid[trow][tcol] = piece
        piece.pos = destination
        check = self.is_in_check(piece.colour)

        self.board.grid[trow][tcol] = target_piece
        self.board.grid[crow][ccol] = piece
        piece.pos = (crow, ccol)

        return not check

    def get_legal_moves(self, piece):
        pseudo_moves = piece.get_legal_moves(self.board)
        legal_moves = []
                    
        for move in pseudo_moves:
            if self.is_move_safe(piece, move):
                legal_moves.append(move)

        return legal_moves

    def has_legal_moves(self, colour):
        for row in self.board.grid:
            for piece in row:
                if piece is not None and piece.colour == colour:
                    if self.get_legal_moves(piece):
                        return True
        return False

    def is_checkmate(self, colour):
        return self.is_in_check(colour) and not self.has_legal_moves(colour)

    def is_stalemate(self, colour):
        return not self.is_in_check(colour) and not self.has_legal_moves(colour)

