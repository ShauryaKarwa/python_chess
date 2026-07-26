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
                moves = self.selected_piece.get_legal_moves(self.board)
                if piece and piece.colour == self.current_turn:
                    self.selected_piece = piece
                else:
                    if pos in moves:
                        self.board.move_piece(self.selected_piece, pos)
                        self.selected_piece = None
                        self.switch_turn()
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

            legal_moves = self.selected_piece.get_legal_moves(self.board)
            for move in legal_moves:
                row_move, col_move = move
                pygame.draw.circle(self.screen, (255, 0, 0),  [155 + self.board.width*col_move, 55 + self.board.height*row_move, self.board.width, self.board.height], 20, 2)

        pygame.display.flip()



    def switch_turn(self):
        if self.current_turn == "w":
            self.current_turn = "b"
        else:
            self.current_turn = "w"