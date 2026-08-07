import pygame

from game import Game


WIDTH = 800
HEIGHT = 600


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Python Chess")

    game = Game(screen)

    while game.running:
        game.handle_events()
        game.update()
        game.draw()

    pygame.quit()


if __name__ == "__main__":
    main()