import pygame
from pygame.locals import *


class Piece:
    def __init__(self, colour, pos, piece_type):
        self.colour = colour
        self.pos = pos
        self.type = piece_type
        self.image = pygame.image.load(f"python_chess/assets/lichess-org lila master public-piece_cburnett/{self.colour}{self.type}.svg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.has_moved = False
    
    def draw(self, screen):
        row, col = self.pos
        #Screen Coordinates
        x = 120 + col*70 + 10
        y = 20 + row*70 + 10
        screen.blit(self.image, (x, y))
    
    def get_legal_moves(self, board):
        raise NotImplementedError("Subclasses must implement get_legal_moves()")
            

        


