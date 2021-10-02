import pygame
import pygame.draw as dr
import numpy as np

pygame.init()

BACKGROUND_COLOR = (212, 205, 205)
BLACK = (0, 0, 0)
MOUTH_COLOR = (235, 16, 53)
FIRST_SKIN_COLOR = (219, 144, 101)
SECOND_SKIN_COLOR = (245, 211, 211)
NOSE_COLOR = (117, 97, 101)
NUMBER_OF_HAIR_TRIANGLES = 10
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
CONVERT = np.pi / 180


def triangle_patch_of_hair(xy, tri_side, angle, color_triangle):
    """
    :param xy: (list) starting point of drawing a triangle
    :param tri_side: length of triangle side
    :param angle: how tilted is this triangle
    :param color_triangle: color of triangle

    draws one hair polygon
    """
    dots = [(xy[0], xy[1])]
    for i in range(2):
        dots.append((xy[0] + np.cos((angle + i * 60) * CONVERT) * tri_side,
                     xy[1] - np.sin((angle + i * 60) * CONVERT) * tri_side))
    dr.polygon(screen, color_triangle, dots)
    dr.polygon(screen, BLACK, dots, int(tri_side / 30))


def face(xy, r_face, color_skin):
    """
    :param xy: (list) center of the face
    :param r_face: radius of circle-face
    :param color_skin: face's color

    draws faceplate
    """
    dr.circle(screen, BLACK, (xy[0], xy[1]), r_face + 2)
    dr.circle(screen, color_skin, (xy[0], xy[1]), r_face)


def mouth(xy, r_mouth):
    """
    :param xy: (list) sets position of a mouth
    :param r_mouth: mouth size (preferably "== r_face" to match with faceplate from "face" function)

    draws mouth
    """
    dots = [(xy[0], xy[1] + r_mouth * 2 / 3), (xy[0] + r_mouth / 2, xy[1] + r_mouth / 3),
            (xy[0] - r_mouth / 2, xy[1] + r_mouth / 3)]
    dr.polygon(screen, MOUTH_COLOR, dots)
    dr.polygon(screen, BLACK, dots, int(r_mouth / 50))


def eyes(xy, r_eyes, color_eyes):
    """
    :param xy: (list) decides position of eyes
    :param r_eyes: size of eyes (preferably "== r_face" to match with faceplate from "face" function)
    :param color_eyes: eye color

    draws 2 eyes for one face
    """
    dr.ellipse(screen, color_eyes, (xy[0] + r_eyes / 5, xy[1] - r_eyes / 4, r_eyes * 0.3, r_eyes / 4), int(r_eyes / 2))
    dr.ellipse(screen, BLACK, (xy[0] + r_eyes / 5, xy[1] - r_eyes / 4, r_eyes * 0.3, r_eyes / 4), int(r_eyes / 33))
    dr.ellipse(screen, BLACK, (xy[0] + r_eyes * 0.3, xy[1] - r_eyes * 0.16, r_eyes / 10, r_eyes / 11))
    dr.ellipse(screen, color_eyes, (xy[0] - r_eyes / 2, xy[1] - r_eyes / 4, r_eyes * 0.3, r_eyes / 4), int(r_eyes / 2))
    dr.ellipse(screen, BLACK, (xy[0] - r_eyes / 2, xy[1] - r_eyes / 4, r_eyes * 0.3, r_eyes / 4), int(r_eyes / 33))
    dr.ellipse(screen, BLACK, (xy[0] - r_eyes * 0.4, xy[1] - r_eyes * 0.16, r_eyes / 10, r_eyes / 11))


def nose(xy, r_nose):
    """
    :param xy: (list) nose position
    :param r_nose: nose size (preferably "== r_face" to match with faceplate from "face" function)

    draws a nose
    """
    dots = [(xy[0], xy[1] + r_nose / 8), (xy[0] + r_nose / 40, xy[1]), (xy[0] - r_nose / 40, xy[1])]
    dr.polygon(screen, NOSE_COLOR, dots)
    dr.polygon(screen, BLACK, dots, int(r_nose / 50))


def hair(xy, r_hair, color_hair=FIRST_HAIR_COLOR):
    """
    :param xy: (list) defines hair position space
    :param r_hair: size of hair patches (should be "== r_face" to match with faceplate from "face" function)
    :param color_hair: hair color

    draws hair for one head
    """
    number_hair = NUMBER_OF_HAIR_TRIANGLES
    angle_hair = -120 / number_hair
    for i in range(number_hair + 1):
        for j in range(i // 2, 0, -1):
            triangle_patch_of_hair([xy[0] - r_hair * np.sin(angle_hair * (j - 0.5) * CONVERT),
                                    xy[1] - r_hair * np.cos(angle_hair * (j - 0.5) * CONVERT)],
                                   r_hair / number_hair * 4, angle_hair * j, color_hair)
        for j in range(i - i // 2):
            triangle_patch_of_hair([xy[0] - r_hair * np.sin(-angle_hair * (j + 0.5) * CONVERT),
                                    xy[1] - r_hair * np.cos(-angle_hair * (j + 0.5) * CONVERT)],
                                   r_hair / number_hair * 4, -angle_hair * j, color_hair)


def head(oxy, r_head, color_head_hair, color_head_eyes, color_head_skin):
    """
    :param oxy: (list) position of center of the head in space
    :param r_head: head size (radius)
    :param color_head_hair: hair color
    :param color_head_eyes: eye color
    :param color_head_skin: skin color

    draws head with all collected pieces of face
    """
    face(oxy, r_head, color_head_skin)
    mouth(oxy, r_head)
    eyes(oxy, r_head, color_head_eyes)
    nose(oxy, r_head)
    hair(oxy, r_head, color_head_hair)


def body(xy, r_body, body_color):
    """
    :param xy: (list) sets the position of body polygon
    :param r_body: body size
    :param body_color: body color

    draws human body
    """
    dr.ellipse(screen, body_color,
               (xy[0] - r_body * 1.2, xy[1] + 0.8 * r_body, r_body * 2.4, 2.5 * r_body))
    dr.ellipse(screen, BLACK,
               (xy[0] - r_body * 1.2, xy[1] + 0.8 * r_body, r_body * 2.4, 2.5 * r_body),
               int(r_body / 100 * 3))


def shoulders(xy, l_shoulders, shoulder_color):
    """
    :param xy: (list) defines position of shoulder polygons
    :param l_shoulders: shoulder size
    :param shoulder_color: skin color of the owner of shoulders

    draws two shoulders
    """
    angle = 75
    shoulder_list = [(xy[0] + l_shoulders, xy[1] + l_shoulders),
                     (xy[0] + l_shoulders * (1 + 3 * np.cos(angle * CONVERT)),
                      xy[1] + l_shoulders * (1 - 3 * np.sin(angle * CONVERT))),
                     (xy[0] + l_shoulders * (1 + 3 * np.cos(angle * CONVERT) + np.cos((angle + 90) * CONVERT) / 7),
                      xy[1] + l_shoulders * (1 - 3 * np.sin(angle * CONVERT) - np.sin((angle + 90) * CONVERT) / 7)),
                     (xy[0] + l_shoulders * (1 + np.cos((angle + 90) * CONVERT) / 7),
                      xy[1] + l_shoulders * (1 - np.sin((angle + 90) * CONVERT) / 7))]
    dr.polygon(screen, shoulder_color, shoulder_list)
    dr.polygon(screen, BLACK, shoulder_list, int(l_shoulders / 100))
    dr.polygon(screen, shoulder_color, [(xy[0] - l_shoulders, xy[1] + l_shoulders),
                                        (xy[0] - l_shoulders - 3 * l_shoulders * np.cos(angle * CONVERT),
                                         xy[1] + l_shoulders - 3 * l_shoulders * np.sin(angle * CONVERT)),
                                        (xy[0] - l_shoulders - 3 * l_shoulders * np.cos(angle * CONVERT)
                                         - l_shoulders / 7 * np.cos((angle + 90) * CONVERT),
                                         xy[1] + l_shoulders - 3 * l_shoulders * np.sin(angle * CONVERT)
                                         - l_shoulders / 7 * np.sin((angle + 90) * CONVERT)),
                                        (xy[0] - l_shoulders - l_shoulders / 7 * np.cos(
                                            (angle + 90) * CONVERT),
                                         xy[1] + l_shoulders - l_shoulders / 7 * np.sin(
                                             (angle + 90) * CONVERT))])
    dr.polygon(screen, BLACK, [(xy[0] - l_shoulders, xy[1] + l_shoulders),
                               (xy[0] - l_shoulders - 3 * l_shoulders * np.cos(angle * CONVERT),
                                xy[1] + l_shoulders - 3 * l_shoulders * np.sin(angle * CONVERT)),
                               (xy[0] - l_shoulders - 3 * l_shoulders * np.cos(angle * CONVERT)
                                - l_shoulders / 7 * np.cos((angle + 90) * CONVERT),
                                xy[1] + l_shoulders - 3 * l_shoulders * np.sin(angle * CONVERT)
                                - l_shoulders / 7 * np.sin((angle + 90) * CONVERT)),
                               (xy[0] - l_shoulders - l_shoulders / 7 * np.cos((angle + 90) * CONVERT),
                                xy[1] + l_shoulders - l_shoulders / 7 * np.sin((angle + 90) * CONVERT))],
               int(l_shoulders / 100))


def sleeves(xy, l_sleeves, sleeves_color, angle, n):
    """
    :param xy: (list) sets starting point for sleeve drawing
    :param l_sleeves: sleeve size (length of polygon side)
    :param sleeves_color: sleeve color
    :param angle: rotates sleeve polygon around starting point clockwise
    :param n: number of sides in sleeve polygon (its mirrored if negative "n" is given)

    draws one sleeve polygon
    """
    dots = [[xy[0], xy[1]]]
    true_dots = [(xy[0], xy[1])]
    for i in range(abs(n)):
        dots.append([dots[i][0] + n / abs(n) * l_sleeves * np.cos((-angle + i * 360 / abs(n)) * CONVERT),
                     dots[i][1] + l_sleeves * np.sin(((-angle + i * 360 / abs(n)) * CONVERT))])
        true_dots.append((dots[i][0], dots[i][1]))
    dr.polygon(screen, sleeves_color, true_dots)
    dr.polygon(screen, BLACK, true_dots, int(l_sleeves / 30))


def hands(xy, r_body, sleeve_color, hand_color):
    """
    :param xy: (list) position of hands
    :param r_body: size of hands
    :param sleeve_color: color of person's sleeves
    :param hand_color: skin color of the owner of hands

    draws hands with sleeves and shoulders
    """
    shoulders(xy, r_body, hand_color)
    dr.ellipse(screen, hand_color, (xy[0] + 1.3 * r_body, xy[1] - 2.2 * r_body, r_body / 2, r_body))
    dr.ellipse(screen, BLACK, (xy[0] + r_body * 1.3, xy[1] - 2.2 * r_body, r_body / 2, r_body),
               int(r_body / 100))
    dr.ellipse(screen, hand_color, (xy[0] - r_body * 1.8, xy[1] - 2.2 * r_body, r_body / 2, r_body))
    dr.ellipse(screen, BLACK, (xy[0] - r_body * 1.8, xy[1] - 2.2 * r_body, r_body / 2, r_body),
               int(r_body / 100))
    sleeves([xy[0] + r_body * 0.8, xy[1] + r_body * 1.5], r_body / 2, sleeve_color, 130, 5)
    sleeves([xy[0] - r_body * 0.8, xy[1] + r_body * 1.5], r_body / 2, sleeve_color, 130, -5)


def python_is_amazing(size):
    """
    :param size: size of a banner

    draws "PYTHON is  REALLY AMAZING!" banner in the top-left of a screen
    """
    dr.rect(screen, BOX_COLOR, (0, 0, int(7 * size), int(size / 2)))
    dr.rect(screen, BLACK, (0, 0, int(7 * size), int(size / 2)), int(size / 50))
    font = pygame.font.Font(None, int(size / 2))
    text = font.render("PYTHON is  REALLY AMAZING!", True, BLACK)
    place = text.get_rect(center=(3.5 * size, size / 4))
    screen.blit(text, place)


def person(xy, size, clothes_color, hair_color, eye_color, skin_color):
    """
    :param xy: (list) person's position
    :param size: person's size
    :param clothes_color: color of person's clothes
    :param hair_color: color of person's hair
    :param eye_color: color of person's eyes
    :param skin_color: color of person's skin

    draws a person
    """
    body([xy[0] * size / 100, xy[1] * size / 100], size, clothes_color)
    head([xy[0] * size / 100, xy[1] * size / 100], size, hair_color, eye_color, skin_color)
    hands([xy[0] * size / 100, xy[1] * size / 100], size, clothes_color, skin_color)


pygame.init()

FPS = 30
screen = pygame.display.set_mode((int(7 * SCALE), int(4 * SCALE)))

dr.rect(screen, BACKGROUND_COLOR, (0, 0, int(7 * SCALE), int(4 * SCALE)))
person(FIRST_PERSON_POSITION, SCALE, GREEN, FIRST_HAIR_COLOR, FIRST_EYE_COLOR, FIRST_SKIN_COLOR)
person(SECOND_PERSON_POSITION, SCALE, ORANGE, SECOND_HAIR_COLOR, SECOND_EYE_COLOR, SECOND_SKIN_COLOR)
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
