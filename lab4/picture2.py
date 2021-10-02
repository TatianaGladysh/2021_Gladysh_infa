import pygame
import pygame.draw as dr
import numpy as np

pygame.init()

BACKGROUND_COLOR = (212, 205, 205)
BLACK = (0, 0, 0)
MOUTH_COLOR = (235, 16, 53)
SKIN_COLOR = (245, 211, 211)
NOSE_COLOR = (117, 97, 101)
FIRST_HAIR_COLOR = (245, 233, 100)
SECOND_HAIR_COLOR = (175, 19, 207)
FIRST_EYE_COLOR = (150, 137, 137)
SECOND_EYE_COLOR = (23, 160, 191)
GREEN = (13, 74, 13)
ORANGE = (240, 147, 26)
BOX_COLOR = (151, 245, 100)

FIRST_PERSON_POSITION = [200, 220]
SECOND_PERSON_POSITION = [500, 220]
SCALE = 150


def triangle_patch_of_hair(xy, triangle_side, angle, color_triangle):
    """
    :param xy: (list) starting point of drawing a triangle
    :param triangle_side: length of triangle side
    :param angle: how tilted is this triangle
    :param color_triangle: color of triangle

    draws one hair polygon
    """
    dr.polygon(screen, color_triangle, [(xy[0], xy[1]), (
        xy[0] + np.cos(angle / 180 * np.pi) * triangle_side, xy[1] - np.sin(angle / 180 * np.pi) * triangle_side),
                                        (xy[0] + np.cos((angle + 60) / 180 * np.pi) * triangle_side,
                                         xy[1] - np.sin((angle + 60) / 180 * np.pi) * triangle_side)])
    dr.polygon(screen, BLACK, [(xy[0], xy[1]), (
        xy[0] + np.cos(angle / 180 * np.pi) * triangle_side, xy[1] - np.sin(angle / 180 * np.pi) * triangle_side),
                               (xy[0] + np.cos((angle + 60) / 180 * np.pi) * triangle_side,
                                xy[1] - np.sin((angle + 60) / 180 * np.pi) * triangle_side)], int(triangle_side / 30))


def face(xy, radius_face):
    """
    :param xy: (list) center of the face
    :param radius_face: radius of circle-face

    draws faceplate
    """
    dr.circle(screen, BLACK, (xy[0], xy[1]), radius_face + 2)
    dr.circle(screen, SKIN_COLOR, (xy[0], xy[1]), radius_face)


def mouth(xy, radius_mouth):
    """
    :param xy: (list) sets position of a mouth
    :param radius_mouth: radius of mouth curvature

    draws mouth
    """
    dr.polygon(screen, MOUTH_COLOR,
               [(xy[0], xy[1] + radius_mouth * 2 / 3), (xy[0] + radius_mouth / 2, xy[1] + radius_mouth / 3),
                (xy[0] - radius_mouth / 2, xy[1] + radius_mouth / 3)])
    dr.polygon(screen, BLACK,
               [(xy[0], xy[1] + radius_mouth * 2 / 3), (xy[0] + radius_mouth / 2, xy[1] + radius_mouth / 3),
                (xy[0] - radius_mouth / 2, xy[1] + radius_mouth / 3)], int(radius_mouth / 50))


def eyes(xy, radius_eyes, color_eyes):
    """
    :param xy: (list) decides position of eyes
    :param radius_eyes: size of eyes
    :param color_eyes: eye color

    draws 2 eyes for one face
    """
    dr.ellipse(screen, color_eyes,
               (xy[0] + radius_eyes * 0.8 / 4 - 0.01 * radius_eyes, xy[1] - radius_eyes / 4 - 0.01 * radius_eyes,
                radius_eyes / 3.5 + 0.02 * radius_eyes, radius_eyes / 4 + 0.02 * radius_eyes), int(radius_eyes / 2))
    dr.ellipse(screen, BLACK,
               (xy[0] + radius_eyes * 0.8 / 4 - 0.01 * radius_eyes, xy[1] - radius_eyes / 4 - 0.01 * radius_eyes,
                radius_eyes / 3.5 + 0.02 * radius_eyes, radius_eyes / 4 + 0.02 * radius_eyes),
               int(radius_eyes / 100 * 3))
    dr.ellipse(screen, BLACK,
               (xy[0] + radius_eyes / 3.5, xy[1] - radius_eyes * 0.6 / 4, radius_eyes / 10, radius_eyes / 11))
    dr.ellipse(screen, color_eyes,
               (xy[0] + radius_eyes * 0.8 / 4 - 2 * (radius_eyes / 3.5 + 0.02 * radius_eyes), xy[1] - radius_eyes / 4,
                radius_eyes / 3.5, radius_eyes / 4), int(radius_eyes / 2))
    dr.ellipse(screen, BLACK,
               (xy[0] + radius_eyes * 0.8 / 4 - 0.01 * radius_eyes - 2 * (radius_eyes / 3.5 + 0.02 * radius_eyes),
                xy[1] - radius_eyes / 4 - 0.01 * radius_eyes,
                radius_eyes / 3.5 + 0.02 * radius_eyes, radius_eyes / 4 + 0.02 * radius_eyes),
               int(radius_eyes / 100 * 3))
    dr.ellipse(screen, BLACK,
               (xy[0] + radius_eyes / 3.5 - 2 * (radius_eyes / 3.5 + 0.02 * radius_eyes), xy[1] - radius_eyes * 0.6 / 4,
                radius_eyes / 10, radius_eyes / 11))


def nose(xy, radius_nose):
    """
    :param xy: (list) nose position
    :param radius_nose: nose size

    draws a nose
    """
    dr.polygon(screen, NOSE_COLOR, [(xy[0], xy[1] + radius_nose / 8), (xy[0] + radius_nose / 40, xy[1]),
                                    (xy[0] - radius_nose / 40, xy[1])])
    dr.polygon(screen, BLACK, [(xy[0], xy[1] + radius_nose / 8), (xy[0] + radius_nose / 40, xy[1]),
                               (xy[0] - radius_nose / 40, xy[1])], int(radius_nose / 50))


def hair(xy, radius_hair, color_hair=FIRST_HAIR_COLOR):
    """
    :param xy: (list) defines hair position space
    :param radius_hair: matches hair patches to the size of the head
    :param color_hair: hair color

    draws hair for one head
    """
    number_hair = 10
    angle_hair = -120 / number_hair
    for i in range(number_hair + 1):
        for j in range(i // 2, 0, -1):
            triangle_patch_of_hair([xy[0] - radius_hair * np.sin(angle_hair * (j - 0.5) / 180 * np.pi),
                                    xy[1] - radius_hair * np.cos(angle_hair * (j - 0.5) / 180 * np.pi)],
                                   radius_hair / number_hair * 4, angle_hair * j, color_hair)
        for j in range(i - i // 2):
            triangle_patch_of_hair([xy[0] - radius_hair * np.sin(-angle_hair * (j + 0.5) / 180 * np.pi),
                                    xy[1] - radius_hair * np.cos(-angle_hair * (j + 0.5) / 180 * np.pi)],
                                   radius_hair / number_hair * 4, -angle_hair * j, color_hair)


def head(oxy, radius_head, color_head_hair, color_head_eyes):
    """
    :param oxy: (list) position of center of the head in space
    :param radius_head: head size
    :param color_head_hair: hair color
    :param color_head_eyes: eye color

    draws head with all collected pieces of face
    """
    face(oxy, radius_head)
    mouth(oxy, radius_head)
    eyes(oxy, radius_head, color_head_eyes)
    nose(oxy, radius_head)
    hair(oxy, radius_head, color_head_hair)


def body(xy, radius_body, body_color):
    """
    :param xy: (list) sets the position of body polygon
    :param radius_body: body size
    :param body_color: body color

    draws human body
    """
    dr.ellipse(screen, body_color,
               (xy[0] - radius_body * 1.2, xy[1] + 0.8 * radius_body, radius_body * 2.4, 2.5 * radius_body))
    dr.ellipse(screen, BLACK,
               (xy[0] - radius_body * 1.2, xy[1] + 0.8 * radius_body, radius_body * 2.4, 2.5 * radius_body),
               int(radius_body / 100 * 3))


def shoulders(xy, radius_shoulders):
    """
    :param xy: (list) defines position of shoulder polygons
    :param radius_shoulders: shoulder size

    draws two shoulder polygons
    """
    angle = 75
    dr.polygon(screen, SKIN_COLOR, [(xy[0] + radius_shoulders, xy[1] + radius_shoulders),
                                    (xy[0] + radius_shoulders + 3 * radius_shoulders * np.cos(angle / 180 * np.pi),
                                     xy[1] + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)),
                                    (xy[0] + radius_shoulders + 3 * radius_shoulders * np.cos(angle / 180 * np.pi)
                                     + radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                     xy[1] + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)
                                     - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi)),
                                    (xy[0] + radius_shoulders + radius_shoulders / 7 * np.cos(
                                        (angle + 90) / 180 * np.pi),
                                     xy[1] + radius_shoulders - radius_shoulders / 7 * np.sin(
                                         (angle + 90) / 180 * np.pi))])
    dr.polygon(screen, BLACK, [(xy[0] + radius_shoulders, xy[1] + radius_shoulders),
                               (xy[0] + radius_shoulders + 3 * radius_shoulders * np.cos(angle / 180 * np.pi),
                                xy[1] + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)),
                               (xy[0] + radius_shoulders + 3 * radius_shoulders * np.cos(angle / 180 * np.pi)
                                + radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                xy[1] + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)
                                - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi)),
                               (xy[0] + radius_shoulders + radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                xy[1] + radius_shoulders - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi))],
               int(radius_shoulders / 100))
    dr.polygon(screen, SKIN_COLOR, [(xy[0] - radius_shoulders, xy[1] + radius_shoulders),
                                    (xy[0] - radius_shoulders - 3 * radius_shoulders * np.cos(angle / 180 * np.pi),
                                     xy[1] + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)),
                                    (xy[0] - radius_shoulders - 3 * radius_shoulders * np.cos(angle / 180 * np.pi)
                                     - radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                     xy[1] + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)
                                     - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi)),
                                    (xy[0] - radius_shoulders - radius_shoulders / 7 * np.cos(
                                        (angle + 90) / 180 * np.pi),
                                     xy[1] + radius_shoulders - radius_shoulders / 7 * np.sin(
                                         (angle + 90) / 180 * np.pi))])
    dr.polygon(screen, BLACK, [(xy[0] - radius_shoulders, xy[1] + radius_shoulders),
                               (xy[0] - radius_shoulders - 3 * radius_shoulders * np.cos(angle / 180 * np.pi),
                                xy[1] + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)),
                               (xy[0] - radius_shoulders - 3 * radius_shoulders * np.cos(angle / 180 * np.pi)
                                - radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                xy[1] + radius_shoulders - 3 * radius_shoulders * np.sin(angle / 180 * np.pi)
                                - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi)),
                               (xy[0] - radius_shoulders - radius_shoulders / 7 * np.cos((angle + 90) / 180 * np.pi),
                                xy[1] + radius_shoulders - radius_shoulders / 7 * np.sin((angle + 90) / 180 * np.pi))],
               int(radius_shoulders / 100))


def sleeves(xy, radius_sleeves, sleeves_color, angle, n):
    """
    :param xy: (list) sets starting point for sleeve drawing
    :param radius_sleeves: sleeve size
    :param sleeves_color: sleeve color
    :param angle: rotates sleeve polygon around starting point
    :param n: mirrors the sleeve (for symmetry purposes)

    draws one sleeve polygon
    """
    dr.polygon(screen, sleeves_color, [(xy[0], xy[1]), (xy[0] + n * np.cos(angle / 180 * np.pi) * radius_sleeves,
                                                        xy[1] - np.sin(angle / 180 * np.pi) * radius_sleeves),
                                       (xy[0] + n * np.cos((angle + 180 / 5) / 180 * np.pi) * radius_sleeves * (
                                               np.sqrt(5) + 1) / 2,
                                        xy[1] - np.sin((angle + 180 / 5) / 180 * np.pi) * radius_sleeves * (
                                                np.sqrt(5) + 1) / 2),
                                       (xy[0] + n * np.cos((angle + 180 * 2 / 5) / 180 * np.pi) * radius_sleeves * (
                                               np.sqrt(5) + 1) / 2,
                                        xy[1] - np.sin((angle + 180 * 2 / 5) / 180 * np.pi) * radius_sleeves * (
                                                np.sqrt(5) + 1) / 2),
                                       (xy[0] + n * np.cos((angle + 180 * 3 / 5) / 180 * np.pi) * radius_sleeves,
                                        xy[1] - np.sin((angle + 180 * 3 / 5) / 180 * np.pi) * radius_sleeves)
                                       ])
    dr.polygon(screen, BLACK, [(xy[0], xy[1]), (xy[0] + n * np.cos(angle / 180 * np.pi) * radius_sleeves,
                                                xy[1] - np.sin(angle / 180 * np.pi) * radius_sleeves),
                               (xy[0] + n * np.cos((angle + 180 / 5) / 180 * np.pi) * radius_sleeves * (
                                       np.sqrt(5) + 1) / 2,
                                xy[1] - np.sin((angle + 180 / 5) / 180 * np.pi) * radius_sleeves * (
                                        np.sqrt(5) + 1) / 2),
                               (xy[0] + n * np.cos((angle + 180 * 2 / 5) / 180 * np.pi) * radius_sleeves * (
                                       np.sqrt(5) + 1) / 2,
                                xy[1] - np.sin((angle + 180 * 2 / 5) / 180 * np.pi) * radius_sleeves * (
                                        np.sqrt(5) + 1) / 2),
                               (xy[0] + n * np.cos((angle + 180 * 3 / 5) / 180 * np.pi) * radius_sleeves,
                                xy[1] - np.sin((angle + 180 * 3 / 5) / 180 * np.pi) * radius_sleeves)
                               ], int(radius_sleeves / 30))


def hands(xy, radius_body, body_color):
    """
    :param xy: (list) position of hands
    :param radius_body: size of hands
    :param body_color: skin color of person's hands

    draws hands with sleeves and shoulders
    """
    shoulders(xy, radius_body)
    dr.ellipse(screen, SKIN_COLOR,
               (xy[0] + radius_body * 1.3, xy[1] - 2.2 * radius_body, radius_body / 2, radius_body))
    dr.ellipse(screen, BLACK,
               (xy[0] + radius_body * 1.3, xy[1] - 2.2 * radius_body, radius_body / 2, radius_body),
               int(radius_body / 100))
    dr.ellipse(screen, SKIN_COLOR,
               (xy[0] - radius_body * 1.8, xy[1] - 2.2 * radius_body, radius_body / 2, radius_body))
    dr.ellipse(screen, BLACK,
               (xy[0] - radius_body * 1.8, xy[1] - 2.2 * radius_body, radius_body / 2, radius_body),
               int(radius_body / 100))
    sleeves([xy[0] + radius_body * 0.8, xy[1] + radius_body * 1.5], radius_body / 2, body_color, 20, 1)
    sleeves([xy[0] - radius_body * 0.8, xy[1] + radius_body * 1.5], radius_body / 2, body_color, 20, -1)


def python_is_amazing(k):
    """
    :param k: size of a banner

    draws "PYTHON is  REALLY AMAZING!" banner in the top-left of a screen
    """
    dr.rect(screen, BOX_COLOR, (0, 0, int(7 * k), int(0.6 * k)))
    dr.rect(screen, BLACK, (0, 0, int(7 * k), int(0.6 * k)), int(0.02 * k))
    font = pygame.font.Font(None, int(0.5 * k))
    text = font.render(
        "PYTHON is  REALLY AMAZING!", True, BLACK)
    place = text.get_rect(
        center=(3.5 * k, 0.3 * k))
    screen.blit(text, place)


def person(xy, size, clothes_color, hair_color, eye_color):
    """
    :param xy: (list) persons whereabouts
    :param size: persons size
    :param clothes_color: color of persons clothes
    :param hair_color: color of persons hair
    :param eye_color: color of persons eyes

    draws a person
    """
    body([xy[0] * size / 100, xy[1] * size / 100], size, clothes_color)
    head([xy[0] * size / 100, xy[1] * size / 100], size, hair_color, eye_color)
    hands([xy[0] * size / 100, xy[1] * size / 100], size, clothes_color)


pygame.init()

FPS = 30
screen = pygame.display.set_mode((int(7 * SCALE), int(4 * SCALE)))

dr.rect(screen, BACKGROUND_COLOR, (0, 0, int(7 * SCALE), int(4 * SCALE)))
person(FIRST_PERSON_POSITION, SCALE, GREEN, FIRST_HAIR_COLOR, FIRST_EYE_COLOR)
person(SECOND_PERSON_POSITION, SCALE, ORANGE, SECOND_HAIR_COLOR, SECOND_EYE_COLOR)
python_is_amazing(SCALE)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
