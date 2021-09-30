import pygame
import pygame.draw as dr
import numpy as np

pygame.init()


def face(x, y, radius_face):
    dr.circle(screen, (0, 0, 0), (x, y), radius_face + 2)
    dr.circle(screen, (245, 211, 211), (x, y), radius_face)


def nose(x, y, radius_nose):
    dr.polygon(screen, (117, 97, 101), [(x, y + radius_nose / 8), (x + radius_nose / 40, y),
                                        (x - radius_nose / 40, y)])
    dr.polygon(screen, (0, 0, 0), [(x, y + radius_nose / 8), (x + radius_nose / 40, y),
                                   (x - radius_nose / 40, y)], int(radius_nose / 50))


def eyes(x, y, radius_eyes):
    dr.ellipse(screen, (23, 160, 191),
               (x + radius_eyes * 0.8 / 4 - 0.01 * radius_eyes, y - radius_eyes / 4 - 0.01 * radius_eyes,
                radius_eyes / 3.5 + 0.02 * radius_eyes, radius_eyes / 4 + 0.02 * radius_eyes), int(radius_eyes / 2))
    dr.ellipse(screen, (0, 0, 0),
               (x + radius_eyes * 0.8 / 4 - 0.01 * radius_eyes, y - radius_eyes / 4 - 0.01 * radius_eyes,
                radius_eyes / 3.5 + 0.02 * radius_eyes, radius_eyes / 4 + 0.02 * radius_eyes),
               int(radius_eyes / 100 * 3))
    dr.ellipse(screen, (0, 0, 0),
               (x + radius_eyes / 3.5, y - radius_eyes * 0.6 / 4, radius_eyes / 10, radius_eyes / 11))
    dr.ellipse(screen, (23, 160, 191),
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


def mouth(x, y, radius_mouth):
    dr.polygon(screen, (235, 16, 53), [(x, y + radius_mouth * 2 / 3), (x + radius_mouth / 2, y + radius_mouth / 3),
                                       (x - radius_mouth / 2, y + radius_mouth / 3)])
    dr.polygon(screen, (0, 0, 0), [(x, y + radius_mouth * 2 / 3), (x + radius_mouth / 2, y + radius_mouth / 3),
                                   (x - radius_mouth / 2, y + radius_mouth / 3)], int(radius_mouth / 50))


def eyebrow(x0, y0, angle, eyebrow_length, eyebrow_width):
    # eyebrow_width = 20
    dr.polygon(screen, (0, 0, 0), [(x0, y0), (x0 - eyebrow_length * np.cos(angle), y0 - eyebrow_length * np.sin(angle)),
                                   (x0 - eyebrow_length * np.cos(angle) + eyebrow_width * np.sin(angle),
                                    y0 - eyebrow_length * np.sin(angle) - eyebrow_width * np.cos(angle)),
                                   (x0 + eyebrow_width * np.sin(angle), y0 - eyebrow_width * np.cos(angle))])


def head(x, y, radius_head):
    face(x, y, radius_head)
    mouth(x, y, radius_head)
    eyes(x, y, radius_head)
    nose(x, y, radius_head)
    hair(x, y, radius_head)


def triangle(x, y, triangle_side, angle):
    dr.polygon(screen, (175, 19, 207), [(x, y), (
        x + np.cos(angle / 180 * np.pi) * triangle_side, y - np.sin(angle / 180 * np.pi) * triangle_side),
                                        (x + np.cos((angle + 60) / 180 * np.pi) * triangle_side,
                                         y - np.sin((angle + 60) / 180 * np.pi) * triangle_side)])
    dr.polygon(screen, (0, 0, 0), [(x, y), (
        x + np.cos(angle / 180 * np.pi) * triangle_side, y - np.sin(angle / 180 * np.pi) * triangle_side),
                                   (x + np.cos((angle + 60) / 180 * np.pi) * triangle_side,
                                    y - np.sin((angle + 60) / 180 * np.pi) * triangle_side)], int(triangle_side / 30))


def body(x, y, radius_body):
    dr.ellipse(screen, (240, 147, 26),
               (x - radius_body * 1.2, y + 0.8 * radius_body, radius_body * 2.4, 2.5 * radius_body))
    dr.ellipse(screen, (0, 0, 0),
               (x - radius_body * 1.2, y + 0.8 * radius_body, radius_body * 2.4, 2.5 * radius_body),
               int(radius_body / 100 * 3))


def body2(x, y, radius_body):
    angle = 75
    dr.polygon(screen, (245, 211, 211), [(x + radius_body, y + radius_body),
                                         (x + radius_body + 3 * radius_body * np.cos(angle / 180 * np.pi),
                                          y + radius_body - 3 * radius_body * np.sin(angle / 180 * np.pi)),
                                         (x + radius_body + 3 * radius_body * np.cos(angle / 180 * np.pi)
                                          + radius_body / 7 * np.cos((angle + 90) / 180 * np.pi),
                                          y + radius_body - 3 * radius_body * np.sin(angle / 180 * np.pi)
                                          - radius_body / 7 * np.sin((angle + 90) / 180 * np.pi)),
                                         (x + radius_body + radius_body / 7 * np.cos((angle + 90) / 180 * np.pi),
                                          y + radius_body - radius_body / 7 * np.sin((angle + 90) / 180 * np.pi))])
    dr.polygon(screen, (0, 0, 0), [(x + radius_body, y + radius_body),
                                   (x + radius_body + 3 * radius_body * np.cos(angle / 180 * np.pi),
                                    y + radius_body - 3 * radius_body * np.sin(angle / 180 * np.pi)),
                                   (x + radius_body + 3 * radius_body * np.cos(angle / 180 * np.pi)
                                    + radius_body / 7 * np.cos((angle + 90) / 180 * np.pi),
                                    y + radius_body - 3 * radius_body * np.sin(angle / 180 * np.pi)
                                    - radius_body / 7 * np.sin((angle + 90) / 180 * np.pi)),
                                   (x + radius_body + radius_body / 7 * np.cos((angle + 90) / 180 * np.pi),
                                    y + radius_body - radius_body / 7 * np.sin((angle + 90) / 180 * np.pi))],
               int(radius_body / 100))
    dr.polygon(screen, (245, 211, 211), [(x - radius_body, y + radius_body),
                                         (x - radius_body - 3 * radius_body * np.cos(angle / 180 * np.pi),
                                          y + radius_body - 3 * radius_body * np.sin(angle / 180 * np.pi)),
                                         (x - radius_body - 3 * radius_body * np.cos(angle / 180 * np.pi)
                                          - radius_body / 7 * np.cos((angle + 90) / 180 * np.pi),
                                          y + radius_body - 3 * radius_body * np.sin(angle / 180 * np.pi)
                                          - radius_body / 7 * np.sin((angle + 90) / 180 * np.pi)),
                                         (x - radius_body - radius_body / 7 * np.cos((angle + 90) / 180 * np.pi),
                                          y + radius_body - radius_body / 7 * np.sin((angle + 90) / 180 * np.pi))])
    dr.polygon(screen, (0, 0, 0), [(x - radius_body, y + radius_body),
                                   (x - radius_body - 3 * radius_body * np.cos(angle / 180 * np.pi),
                                    y + radius_body - 3 * radius_body * np.sin(angle / 180 * np.pi)),
                                   (x - radius_body - 3 * radius_body * np.cos(angle / 180 * np.pi)
                                    - radius_body / 7 * np.cos((angle + 90) / 180 * np.pi),
                                    y + radius_body - 3 * radius_body * np.sin(angle / 180 * np.pi)
                                    - radius_body / 7 * np.sin((angle + 90) / 180 * np.pi)),
                                   (x - radius_body - radius_body / 7 * np.cos((angle + 90) / 180 * np.pi),
                                    y + radius_body - radius_body / 7 * np.sin((angle + 90) / 180 * np.pi))],
               int(radius_body / 100))
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

    x = x + radius_body * 0.8
    y = y + radius_body * 1.5
    angle = 20
    body_side = radius_body / 2
    dr.polygon(screen, (240, 147, 26), [(x, y), (x + np.cos(angle / 180 * np.pi) * body_side,
                                                 y - np.sin(angle / 180 * np.pi) * body_side),
                                        (x + np.cos((angle + 180 / 5) / 180 * np.pi) * body_side * (np.sqrt(5) + 1) / 2,
                                         y - np.sin((angle + 180 / 5) / 180 * np.pi) * body_side * (
                                                 np.sqrt(5) + 1) / 2),
                                        (x + np.cos((angle + 180 * 2 / 5) / 180 * np.pi) * body_side * (
                                                np.sqrt(5) + 1) / 2,
                                         y - np.sin((angle + 180 * 2 / 5) / 180 * np.pi) * body_side * (
                                                 np.sqrt(5) + 1) / 2),
                                        (x + np.cos((angle + 180 * 3 / 5) / 180 * np.pi) * body_side,
                                         y - np.sin((angle + 180 * 3 / 5) / 180 * np.pi) * body_side)
                                        ])
    dr.polygon(screen, (0, 0, 0), [(x, y), (x + np.cos(angle / 180 * np.pi) * body_side,
                                            y - np.sin(angle / 180 * np.pi) * body_side),
                                   (x + np.cos((angle + 180 / 5) / 180 * np.pi) * body_side * (np.sqrt(5) + 1) / 2,
                                    y - np.sin((angle + 180 / 5) / 180 * np.pi) * body_side * (
                                            np.sqrt(5) + 1) / 2),
                                   (x + np.cos((angle + 180 * 2 / 5) / 180 * np.pi) * body_side * (
                                           np.sqrt(5) + 1) / 2,
                                    y - np.sin((angle + 180 * 2 / 5) / 180 * np.pi) * body_side * (
                                            np.sqrt(5) + 1) / 2),
                                   (x + np.cos((angle + 180 * 3 / 5) / 180 * np.pi) * body_side,
                                    y - np.sin((angle + 180 * 3 / 5) / 180 * np.pi) * body_side)
                                   ], int(body_side / 30))
    x = x - radius_body * 0.8 * 2
    angle = 20
    body_side = radius_body / 2
    dr.polygon(screen, (240, 147, 26), [(x, y), (x - np.cos(angle / 180 * np.pi) * body_side,
                                                 y - np.sin(angle / 180 * np.pi) * body_side),
                                        (x - np.cos((angle + 180 / 5) / 180 * np.pi) * body_side * (np.sqrt(5) + 1) / 2,
                                         y - np.sin((angle + 180 / 5) / 180 * np.pi) * body_side * (
                                                 np.sqrt(5) + 1) / 2),
                                        (x - np.cos((angle + 180 * 2 / 5) / 180 * np.pi) * body_side * (
                                                np.sqrt(5) + 1) / 2,
                                         y - np.sin((angle + 180 * 2 / 5) / 180 * np.pi) * body_side * (
                                                 np.sqrt(5) + 1) / 2),
                                        (x - np.cos((angle + 180 * 3 / 5) / 180 * np.pi) * body_side,
                                         y - np.sin((angle + 180 * 3 / 5) / 180 * np.pi) * body_side)
                                        ])
    dr.polygon(screen, (0, 0, 0), [(x, y), (x - np.cos(angle / 180 * np.pi) * body_side,
                                            y - np.sin(angle / 180 * np.pi) * body_side),
                                   (x - np.cos((angle + 180 / 5) / 180 * np.pi) * body_side * (np.sqrt(5) + 1) / 2,
                                    y - np.sin((angle + 180 / 5) / 180 * np.pi) * body_side * (
                                            np.sqrt(5) + 1) / 2),
                                   (x - np.cos((angle + 180 * 2 / 5) / 180 * np.pi) * body_side * (
                                           np.sqrt(5) + 1) / 2,
                                    y - np.sin((angle + 180 * 2 / 5) / 180 * np.pi) * body_side * (
                                            np.sqrt(5) + 1) / 2),
                                   (x - np.cos((angle + 180 * 3 / 5) / 180 * np.pi) * body_side,
                                    y - np.sin((angle + 180 * 3 / 5) / 180 * np.pi) * body_side)
                                   ], int(body_side / 30))


def hair(x, y, radius_hair):
    number_hair = 10
    angle_hair = -120 / number_hair
    for i in range(number_hair + 1):
        for j in range(i // 2, 0, -1):
            triangle(x - radius_hair * np.sin(angle_hair * (j - 0.5) / 180 * np.pi),
                     y - radius_hair * np.cos(angle_hair * (j - 0.5) / 180 * np.pi),
                     radius_hair / number_hair * 4, angle_hair * j)
        for j in range(i - i // 2):
            triangle(x - radius_hair * np.sin(-angle_hair * (j + 0.5) / 180 * np.pi),
                     y - radius_hair * np.cos(-angle_hair * (j + 0.5) / 180 * np.pi),
                     radius_hair / number_hair * 4, -angle_hair * j)


pygame.init()

FPS = 30
k = 1.5
screen = pygame.display.set_mode((int(400 * k), int(400 * k)))

dr.rect(screen, (212, 205, 205), (0, 0, int(400 * k), int(400 * k)))
body(200 * k, 220 * k, 100 * k)
head(200 * k, 220 * k, 100 * k)
body2(200 * k, 220 * k, 100 * k)
dr.rect(screen, (151, 245, 100), (0, 0, int(400 * k), int(60 * k)))
dr.rect(screen, (0, 0, 0), (0, 0, int(400 * k), int(60 * k)), int(2 * k))

# PYTHON is AMAZING
font = pygame.font.Font(None, 72)
text = font.render(
    "PYTHON is AMAZING", True, (0, 0, 0))
place = text.get_rect(
    center=(200 * k, 30 * k))
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
