import pygame
from pygame.locals import *

board = [(i, j) for j in range(0, 8) for i in range(0, 8)]
print(board)

class Sq(pygame.sprite.Sprite):
    def __init__(self, index):
        super().__init__()
        self.surf = pygame.Surface((70, 70))
        self.index = index
        self.surf.fill((240, 217, 181)) if sum(self.index) % 2 == 0 else self.surf.fill((181, 136, 99))

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Chess")

clock = pygame.time.Clock()

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    
    screen.fill((255, 255, 255))
    for index in board:
        s = Sq(index)
        screen.blit(s.surf, (120 + s.surf.get_width()*index[0], 20 + s.surf.get_height()*index[1]))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()