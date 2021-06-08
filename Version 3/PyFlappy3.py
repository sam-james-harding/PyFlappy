import pygame

from Screens.Game import Game

#global vars
TITLE = "PyFlappy 3"

#pygame setup
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

pygame.init()
pygame.font.init()

#screens
game = Game(screen, clock)
game.Play()