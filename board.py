import pygame
from pygame.locals import *

from Pieces import bishop, king, knight, pawn, piece, queen, rook

class Board:
    def __init__(self):
        self.grid = [[None for i in range(8)] for j in range(8)] #[row][col]
        # Square Size
        self.height = 70
        self.width = 70
        self.light = (240, 217, 181)
        self.dark = (181, 136, 99)
        self.colours = (self.light, self.dark)
        self.dimensions = (8, 8) #(row, col)

    def draw(self, screen):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                #Drawing Squares
                colour = self.light if (i + j) % 2 == 0 else self.dark
                pygame.draw.rect(screen, colour, [120 + self.width*j, 20 + self.height*i, self.width, self.height], 1) 
                #Drawing Pieces
                if self.grid[i][j] is not None:
                    self.grid[i][j].draw(screen) #Implement in Piece classes
    
    def setup(self):
        # black Pieces
        self.grid[0][0] = rook.Rook("b", (0, 0))
        self.grid[0][1] = knight.Knight("b", (0, 1))
        self.grid[0][2] = bishop.Bishop("b", (0, 2))
        self.grid[0][3]= queen.Queen("b", (0, 3))
        self.grid[0][4]= king.King("b", (0, 4))
        self.grid[0][5] = bishop.Bishop("b", (0, 5))
        self.grid[0][6] = knight.Knight("b", (0, 6))
        self.grid[0][7] = rook.Rook("b", (0, 7))
        for i in range(8):
            self.grid[1][i] = pawn.Pawn("b", (1, i))
        # white Pieces
        self.grid[7][0] = rook.Rook("w", (7, 0))
        self.grid[7][1] = knight.Knight("w", (7, 1))
        self.grid[7][2] = bishop.Bishop("w", (7, 2))
        self.grid[7][3]= queen.Queen("w", (7, 3))
        self.grid[7][4]= king.King("w", (7, 4))
        self.grid[7][5] = bishop.Bishop("w", (7, 5))
        self.grid[7][6] = knight.Knight("w", (7, 6))
        self.grid[7][7] = rook.Rook("w", (7, 7))
        for i in range(8):
            self.grid[6][i] = pawn.Pawn("w", (6, i))
        
    def get_piece(self, pos : tuple):
        return self.grid[pos[0]][pos[1]]
    
    def move_piece(self, piece, pos):
        self.grid[piece.pos[0]][piece.pos[1]] = None
        self.grid[pos[0]][pos[1]] = piece
        piece.pos = pos
        piece.has_moved = True
    
    def is_empty(self, pos):
        return self.get_piece(pos) is None 
    
    def is_enemy(self, pos, colour):
        piece = self.get_piece(pos)

        return piece is not None and piece.colour != colour 
    
    def within_board(self, pos):
        return 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7 
    
    def mouse_to_square(self, mouse):
        row = (mouse[0] - 120)//70
        col = (mouse[1] - 20)//70
        return (row, col) if self.within_board((row, col)) else None
                


