import pygame
from pygame.locals import *

from board import Board

from Pieces import bishop, king, knight, pawn, piece, queen, rook

pygame.init()
pygame.display.set_mode((1,1))

board = Board()
board.setup()

rook1 = board.get_piece((7, 0)) # White rook
print(rook1.get_legal_moves(board))

board.grid[6][0] = None # Removing white pawn to see changes
print(rook1.get_legal_moves(board))

knight1 = board.get_piece((0, 1)) # Black Knight
print(knight1.get_legal_moves(board))

board.grid[1][3] = None
print(knight1.get_legal_moves(board))

bishop1 = board.get_piece((0, 2)) #Black Bishop
print(bishop1.get_legal_moves(board))

queen1 = board.get_piece((0, 3)) # Black queen
print(queen1.get_legal_moves(board))

king1 = board.get_piece((0, 4)) #Black King
print(king1.get_legal_moves(board))

pawn1 = board.get_piece((6, 6)) #White pawn
print(pawn1.get_legal_moves(board))

board.grid[5][5] = board.get_piece((1,1)) # adding black pawn to see changes
print(pawn1.get_legal_moves(board))







