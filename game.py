import pygame

from board import Board

from Pieces import bishop, king, knight, pawn, piece, queen, rook

class Game:
    def __init__(self):
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
        pass

    def switch_turn(self):
        pass