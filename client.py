import os
import sys

import pygame
from network import Network

# initialise pygame
pygame.init()

width = 600
height = 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(window, player, player2):
    window.fill((90, 90, 90)) # fill window with a background colour
    player.draw(window)
    player2.draw(window)
    pygame.display.update()


def main():
    run = True
    n = Network()
    p = n.getP()    
    clock = pygame.time.Clock()

    # game loop
    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(window, p, p2)

main()