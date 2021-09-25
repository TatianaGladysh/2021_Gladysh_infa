import pygame
import pygame.draw as dr
import numpy as np


def face(radius_face):
    dr.circle(screen, (0, 0, 0), (200, 200), radius_face + 2)
    dr.circle(screen, (255, 255, 0), (200, 200), radius_face)


def eye(radius_small, radius_big, side):
    dr.circle(screen, (0, 0, 0), (side * 270 + (1 - side) * 130, 180), radius_big + 2)
    dr.circle(screen, (255, 0, 0), (side * 270 + (1 - side) * 130, 180), radius_big)
    dr.circle(screen, (0, 0, 0), (side * 270 + (1 - side) * 130, 180), radius_small)


def mouth():
    dr.rect(screen, (0, 0, 0), (140, 270, 120, 20))


def eyebrow(x0, y0, angle, eyebrow_length, eyebrow_width):
    # eyebrow_width = 20
    dr.polygon(screen, (0, 0, 0), [(x0, y0), (x0 - eyebrow_length * np.cos(angle), y0 - eyebrow_length * np.sin(angle)),
                                   (x0 - eyebrow_length * np.cos(angle) + eyebrow_width * np.sin(angle),
                                    y0 - eyebrow_length * np.sin(angle) - eyebrow_width * np.cos(angle)),
                                   (x0 + eyebrow_width * np.sin(angle), y0 - eyebrow_width * np.cos(angle))])



pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

dr.rect(screen, (255, 255, 255), (0, 0, 400, 400))
face(150)
eye(15, 25, 1)
eye(13, 28, 0)
mouth()
eyebrow(180, 150, -1.13, 20, 120)
eyebrow(220, 170, 1.24, 20, 130)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
