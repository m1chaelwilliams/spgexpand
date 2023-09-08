import pygame
import sys
from spgexpand import SPGExpandableSurface

pygame.init()
screen = pygame.display.set_mode((600, 400), pygame.SCALED)

surface = SPGExpandableSurface(
    pygame.image.load('example_surface.png').convert_alpha(),
    400,
    300,
    (3,3)
)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('lightblue')
    screen.blit(surface.surface, (100, 50))

    pygame.display.update()