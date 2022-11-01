import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

circle(screen, (230, 218, 57), (200, 175), 150)
circle(screen, (219, 20, 20), (270, 130), 25)
circle(screen, (219, 20, 20), (130, 130), 33)
circle(screen, (0, 0, 0), (270, 130), 15)
circle(screen, (0, 0, 0), (130, 130), 15)
rect(screen, (0, 0, 0), (120, 250, 160, 30))
line(screen, (0, 0, 0), (245, 120), (300, 80), 7)
line(screen, (0, 0, 0), (90, 60), (170, 120), 8)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()