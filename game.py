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
        self.awaiting_promotion = False
        self.promotion_piece = None
        self.last_move = None

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
        if self.awaiting_promotion:

            x, y = pos

            if 170 <= x <= 220 and 180 <= y <= 230:
                self.promotion(self.promotion_piece, queen.Queen)

            elif 240 <= x <= 290 and 180 <= y <= 230:
                self.promotion(self.promotion_piece, rook.Rook)

            elif 310 <= x <= 360 and 180 <= y <= 230:
                self.promotion(self.promotion_piece, bishop.Bishop)

            elif 380 <= x <= 430 and 180 <= y <= 230:
                self.promotion(self.promotion_piece, knight.Knight)

            else:
                return

            self.awaiting_promotion = False
            self.promotion_piece = None
            self.selected_piece = None
            self.switch_turn()

            if self.is_checkmate(self.current_turn):
                print(f"{self.current_turn} is checkmated!")
                self.running = False
            elif self.is_stalemate(self.current_turn):
                print("It's a stalemate!")
                self.running = False

            return
        
        pos = self.board.mouse_to_square(pos)
        if pos:
           piece = self.board.get_piece(pos)
           if self.selected_piece:
                legal_moves = self.get_legal_moves(self.selected_piece)

                if piece and piece.colour == self.current_turn:
                    self.selected_piece = piece
                else:
                    if pos in legal_moves:
                        start = self.selected_piece.pos
                        self.board.move_piece(self.selected_piece, pos)
                        self.last_move = (self.selected_piece, start, self.selected_piece.pos)
                        if self.needs_promotion(self.selected_piece):
                            self.awaiting_promotion = True
                            self.promotion_piece = self.selected_piece
                        else:
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

        if self.awaiting_promotion:

            pygame.draw.rect(self.screen, (255,255,255), [160,170,290,70])
            pygame.draw.rect(self.screen, (0,0,0), [160,170,290,70], 2)

            q = queen.Queen(self.promotion_piece.colour, (0,0))
            r = rook.Rook(self.promotion_piece.colour, (0,0))
            b = bishop.Bishop(self.promotion_piece.colour, (0,0))
            k = knight.Knight(self.promotion_piece.colour, (0,0))

            self.screen.blit(q.image, (170,180))
            self.screen.blit(r.image, (240,180))
            self.screen.blit(b.image, (310,180))
            self.screen.blit(k.image, (380,180))
        
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
            #Check for castling
            if isinstance(piece, king.King) and abs(move[1] - piece.pos[1]) == 2:
                direction = 1 if move[1] > piece.pos[1] else -1
                middle =  (piece.pos[0], piece.pos[1] + direction)
                if not self.is_in_check(piece.colour) and self.is_move_safe(piece, move) and self.is_move_safe(piece, middle):
                    legal_moves.append(move)
            #En passant
            elif self.last_move is not None and isinstance(piece, pawn.Pawn) and isinstance(self.last_move[0], pawn.Pawn) and self.is_move_safe(piece, move):
                if abs(self.last_move[2][0] - self.last_move[1][0]) == 2 and abs(move[0] - self.last_move[2][0]) == 1 and move[1] == self.last_move[2][1] and self.board.is_empty(move):
                    adjacent_piece = self.board.get_piece((piece.pos[0], move[1]))
                    if adjacent_piece is self.last_move[0]:
                        legal_moves.append(move) 

            elif self.is_move_safe(piece, move):
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

    def needs_promotion(self, piece):
        if isinstance(piece, pawn.Pawn):
            if (piece.colour == "w" and piece.pos[0] == 0) or (piece.colour == "b" and piece.pos[0] == 7):
                return True
        return False

    def promotion(self, piece, promotion_type):
        new_piece = promotion_type(piece.colour, piece.pos)
        row, col = piece.pos
        self.board.grid[row][col] = new_piece

