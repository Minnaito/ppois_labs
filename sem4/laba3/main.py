import pygame
from constants import *
from menu import Menu


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Moorhuhn")

    menu = Menu(screen)
    menu.run()


if __name__ == "__main__":
    main()
