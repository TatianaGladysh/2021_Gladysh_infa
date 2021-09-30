import pygame
import pygame.draw as dr
import numpy as np

pygame.init()


def triangle(x, y, triangle_side, angle, color_triangle):
    dr.polygon(screen, color_triangle, [(x, y), (
        x + np.cos(angle / 180 * np.pi) * triangle_side, y - np.sin(angle / 180 * np.pi) * triangle_side),
                                        (x + np.cos((angle + 60) / 180 * np.pi) * triangle_side,
                                         y - np.sin((angle + 60) / 180 * np.pi) * triangle_side)])
    dr.polygon(screen, (0, 0, 0), [(x, y), (
        x + np.cos(angle / 180 * np.pi) * triangle_side, y - np.sin(angle / 180 * np.pi) * triangle_side),
                                   (x + np.cos((angle + 60) / 180 * np.pi) * triangle_side,
                                    y - np.sin((angle + 60) / 180 * np.pi) * triangle_side)], int(triangle_side / 30))


def face(x, y, radius_face):
    dr.circle(screen, (0, 0, 0), (x, y), radius_face + 2)
    dr.circle(screen, (245, 211, 211), (x, y), radius_face)


def mouth(x, y, radius_mouth):
    dr.polygon(screen, (235, 16, 53), [(x, y + radius_mouth * 2 / 3), (x + radius_mouth / 2, y + radius_mouth / 3),
                                       (x - radius_mouth / 2, y + radius_mouth / 3)])
    dr.polygon(screen, (0, 0, 0), [(x, y + radius_mouth * 2 / 3), (x + radius_mouth / 2, y + radius_mouth / 3),
                                   (x - radius_mouth / 2, y + radius_mouth / 3)], int(radius_mouth / 50))


def eyes(x, y, radius_eyes, color_eyes):
    dr.ellipse(screen, color_eyes,
               (x + radius_eyes * 0.8 / 4 - 0.01 * radius_eyes, y - radius_eyes / 4 - 0.01 * radius_eyes,
                radius_eyes / 3.5 + 0.02 * radius_eyes, radius_eyes / 4 + 0.02 * radius_eyes), int(radius_eyes / 2))
    dr.ellipse(screen, (0, 0, 0),
               (x + radius_eyes * 0.8 / 4 - 0.01 * radius_eyes, y - radius_eyes / 4 - 0.01 * radius_eyes,
                radius_eyes / 3.5 + 0.02 * radius_eyes, radius_eyes / 4 + 0.02 * radius_eyes),
               int(radius_eyes / 100 * 3))
    dr.ellipse(screen, (0, 0, 0),
               (x + radius_eyes / 3.5, y - radius_eyes * 0.6 / 4, radius_eyes / 10, radius_eyes / 11))
    dr.ellipse(screen, color_eyes,
               (x + radius_eyes * 0.8 / 4 - 2 * (radius_eyes / 3.5 + 0.02 * radius_eyes), y - radius_eyes / 4,
                radius_eyes / 3.5, radius_eyes / 4), int(radius_eyes / 2))
    dr.ellipse(screen, (0, 0, 0),
               (x + radius_eyes * 0.8 / 4 - 0.01 * radius_eyes - 2 * (radius_eyes / 3.5 + 0.02 * radius_eyes),
                y - radius_eyes / 4 - 0.01 * radius_eyes,
                radius_eyes / 3.5 + 0.02 * radius_eyes, radius_eyes / 4 + 0.02 * radius_eyes),
               int(radius_eyes / 100 * 3))
    dr.ellipse(screen, (0, 0, 0),
               (x + radius_eyes / 3.5 - 2 * (radius_eyes / 3.5 + 0.02 * radius_eyes), y - radius_eyes * 0.6 / 4,
                radius_eyes / 10, radius_eyes / 11))


def nose(x, y, radius_nose):
    dr.polygon(screen, (117, 97, 101), [(x, y + radius_nose / 8), (x + radius_nose / 40, y),
                                        (x - radius_nose / 40, y)])
    dr.polygon(screen, (0, 0, 0), [(x, y + radius_nose / 8), (x + radius_nose / 40, y),
                                   (x - radius_nose / 40, y)], int(radius_nose / 50))


def hair(x, y, radius_hair, color_hair=(175, 19, 207)):
    number_hair = 10
    angle_hair = -120 / number_hair
    for i in range(number_hair + 1):
        for j in range(i // 2, 0, -1):
            triangle(x - radius_hair * np.sin(angle_hair * (j - 0.5) / 180 * np.pi),
                     y - radius_hair * np.cos(angle_hair * (j - 0.5) / 180 * np.pi),
                     radius_hair / number_hair * 4, angle_hair * j, color_hair)
        for j in range(i - i // 2):
            triangle(x - radius_hair * np.sin(-angle_hair * (j + 0.5) / 180 * np.pi),
                     y - radius_hair * np.cos(-angle_hair * (j + 0.5) / 180 * np.pi),
                     radius_hair / number_hair * 4, -angle_hair * j, color_hair)


def head(x, y, radius_head, color_head_hair, color_head_eyes):
    face(x, y, radius_head)
    mouth(x, y, radius_head)
    eyes(x, y, radius_head, color_head_eyes)
    nose(x, y, radius_head)
    hair(x, y, radius_head, color_head_hair)


def body(x, y, radius_body, body_color):
    dr.ellipse(screen, body_color,
               (x - radius_body * 1.2, y + 0.8 * radius_body, radius_body * 2.4, 2.5 * radius_body))
    dr.ellipse(screen, (0, 0, 0),
               (x - radius_body * 1.2, y + 0.8 * radius_body, radius_body * 2.4, 2.5 * radius_body),
               int(radius_body / 100 * 3))


def shoulders(x, y, radius_shoulders):
    angle = 75
    dr.polygon(screen, (245, 211, 211), [(x + radius_shoulders, y + radius_shoulders),
                                         (x + radius_shoulders + 3 * radius_shoulders * np.cos(angle / 180 * np.pi),
                                          y + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)),
                                         (x + radius_shoulders + 3 * radius_shoulders * np.cos(angle / 180 * np.pi)
                                          + radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                          y + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)
                                          - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi)),
                                         (x + radius_shoulders + radius_shoulders / 7 * np.cos(
                                             (angle + 90) / 180 * np.pi),
                                          y + radius_shoulders - radius_shoulders / 7 * np.sin(
                                              (angle + 90) / 180 * np.pi))])
    dr.polygon(screen, (0, 0, 0), [(x + radius_shoulders, y + radius_shoulders),
                                   (x + radius_shoulders + 3 * radius_shoulders * np.cos(angle / 180 * np.pi),
                                    y + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)),
                                   (x + radius_shoulders + 3 * radius_shoulders * np.cos(angle / 180 * np.pi)
                                    + radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                    y + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)
                                    - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi)),
                                   (x + radius_shoulders + radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                    y + radius_shoulders - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi))],
               int(radius_shoulders / 100))
    dr.polygon(screen, (245, 211, 211), [(x - radius_shoulders, y + radius_shoulders),
                                         (x - radius_shoulders - 3 * radius_shoulders * np.cos(angle / 180 * np.pi),
                                          y + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)),
                                         (x - radius_shoulders - 3 * radius_shoulders * np.cos(angle / 180 * np.pi)
                                          - radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                          y + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)
                                          - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi)),
                                         (x - radius_shoulders - radius_shoulders / 7 * np.cos(
                                             (angle + 90) / 180 * np.pi),
                                          y + radius_shoulders - radius_shoulders / 7 * np.sin(
                                              (angle + 90) / 180 * np.pi))])
    dr.polygon(screen, (0, 0, 0), [(x - radius_shoulders, y + radius_shoulders),
                                   (x - radius_shoulders - 3 * radius_shoulders * np.cos(angle / 180 * np.pi),
                                    y + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)),
                                   (x - radius_shoulders - 3 * radius_shoulders * np.cos(angle / 180 * np.pi)
                                    - radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                    y + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)
                                    - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi)),
                                   (x - radius_shoulders - radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                    y + radius_shoulders - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi))],
               int(radius_shoulders / 100))


def sleeves(x, y, radius_sleeves, sleeves_color, angle, n):
    dr.polygon(screen, sleeves_color, [(x, y), (x + n * np.cos(angle / 180 * np.pi) * radius_sleeves,
                                                y - np.sin(angle / 180 * np.pi) * radius_sleeves),
                                       (x + n * np.cos((angle + 180 / 5) / 180 * np.pi) * radius_sleeves * (
                                               np.sqrt(5) + 1) / 2,
                                        y - np.sin((angle + 180 / 5) / 180 * np.pi) * radius_sleeves * (
                                                np.sqrt(5) + 1) / 2),
                                       (x + n * np.cos((angle + 180 * 2 / 5) / 180 * np.pi) * radius_sleeves * (
                                               np.sqrt(5) + 1) / 2,
                                        y - np.sin((angle + 180 * 2 / 5) / 180 * np.pi) * radius_sleeves * (
                                                np.sqrt(5) + 1) / 2),
                                       (x + n * np.cos((angle + 180 * 3 / 5) / 180 * np.pi) * radius_sleeves,
                                        y - np.sin((angle + 180 * 3 / 5) / 180 * np.pi) * radius_sleeves)
                                       ])
    dr.polygon(screen, (0, 0, 0), [(x, y), (x + n * np.cos(angle / 180 * np.pi) * radius_sleeves,
                                            y - np.sin(angle / 180 * np.pi) * radius_sleeves),
                                   (x + n * np.cos((angle + 180 / 5) / 180 * np.pi) * radius_sleeves * (
                                           np.sqrt(5) + 1) / 2,
                                    y - np.sin((angle + 180 / 5) / 180 * np.pi) * radius_sleeves * (
                                            np.sqrt(5) + 1) / 2),
                                   (x + n * np.cos((angle + 180 * 2 / 5) / 180 * np.pi) * radius_sleeves * (
                                           np.sqrt(5) + 1) / 2,
                                    y - np.sin((angle + 180 * 2 / 5) / 180 * np.pi) * radius_sleeves * (
                                            np.sqrt(5) + 1) / 2),
                                   (x + n * np.cos((angle + 180 * 3 / 5) / 180 * np.pi) * radius_sleeves,
                                    y - np.sin((angle + 180 * 3 / 5) / 180 * np.pi) * radius_sleeves)
                                   ], int(radius_sleeves / 30))


def hands(x, y, radius_body, body_color):
    shoulders(x, y, radius_body)
    dr.ellipse(screen, (245, 211, 211),
               (x + radius_body * 1.3, y - 2.2 * radius_body, radius_body / 2, radius_body))
    dr.ellipse(screen, (0, 0, 0),
               (x + radius_body * 1.3, y - 2.2 * radius_body, radius_body / 2, radius_body),
               int(radius_body / 100))
    dr.ellipse(screen, (245, 211, 211),
               (x - radius_body * 1.8, y - 2.2 * radius_body, radius_body / 2, radius_body))
    dr.ellipse(screen, (0, 0, 0),
               (x - radius_body * 1.8, y - 2.2 * radius_body, radius_body / 2, radius_body),
               int(radius_body / 100))
    sleeves(x + radius_body * 0.8, y + radius_body * 1.5, radius_body / 2, body_color, 20, 1)
    sleeves(x - radius_body * 0.8, y + radius_body * 1.5, radius_body / 2, body_color, 20, -1)


pygame.init()

FPS = 30
k = 1.5
screen = pygame.display.set_mode((int(400 * k * 1.75), int(400 * k)))

dr.rect(screen, (212, 205, 205), (0, 0, int(400 * k * 1.75), int(400 * k)))
body(200 * k, 220 * k, 100 * k, (13, 74, 13))
head(200 * k, 220 * k, 100 * k, (245, 233, 100), (150, 137, 137))
hands(200 * k, 220 * k, 100 * k, (13, 74, 13))

body(500 * k, 220 * k, 100 * k, (240, 147, 26))
head(500 * k, 220 * k, 100 * k, (175, 19, 207), (23, 160, 191))
hands(500 * k, 220 * k, 100 * k, (240, 147, 26))

# PYTHON is AMAZING
dr.rect(screen, (151, 245, 100), (0, 0, int(400 * k * 1.75), int(60 * k)))
dr.rect(screen, (0, 0, 0), (0, 0, int(400 * k * 1.75), int(60 * k)), int(2 * k))
font = pygame.font.Font(None, 72)
text = font.render(
    "PYTHON is  REALLY AMAZING!", True, (0, 0, 0))
place = text.get_rect(
    center=(200 * k * 1.75, 30 * k))
screen.blit(text, place)

# dr.circle(screen, (0, 0, 0), (200, 200), 150, 10)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
