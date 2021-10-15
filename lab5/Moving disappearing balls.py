import pygame
import pygame.draw as dr
from random import randint

pygame.init()

FPS = 100
screen_size = (1200, 800)
screen = pygame.display.set_mode(screen_size)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

number_of_balls = 20

# координаты, радиус, цвет  и 2 проекции скорости
BALLS = []
for i in range(number_of_balls + 2):
    BALLS.append([0] * 6)
score = 0
time = 0


def new_ball():
    """
    рисует новый шарик случайного размера, цвета и положения
    """
    x = randint(100, screen_size[0] - 100)
    y = randint(100, screen_size[1] - 100)
    r = randint(10, 100)
    speed_x = randint(1, 10)
    speed_y = randint(1, 10)
    color = COLORS[randint(0, 5)]
    dr.circle(screen, color, (x, y), r)
    BALLS[BALLS[number_of_balls][0]] = [x, y, r, color, speed_x, speed_y]
    BALLS[number_of_balls][0] = (BALLS[number_of_balls][0] + 1) % number_of_balls


def draw_all_balls():
    """
    рисует все шарики, которые сейчас должны быть на листе
    """
    if time < number_of_balls or time % 10 == 0:
        new_ball()
    for j in range(number_of_balls):
        BALLS[j] = draw_ball(*BALLS[j])


def draw_ball(x, y, radius, color, speed_x, speed_y):
    """
    рисует шарик с заданными характеристиками

    :param x: координата по оси X
    :param y: координата по оси Y
    :param radius: радиус шарика
    :param color: цвет шарика
    :param speed_x: скорость по оси OX
    :param speed_y: скорость по оси OY
    :return: пересчитанные характеристики
    """
    dr.circle(screen, color, (x + speed_x, y + speed_y), radius)
    x = x + speed_x
    y = y + speed_y
    if x - radius < 0 or x + radius > screen_size[0]:
        speed_x = -speed_x
    elif y - radius < 0 or y + radius > screen_size[1]:
        speed_y = -speed_y
    return [x, y, radius, color, speed_x, speed_y]


def score_window():
    dr.rect(screen, (0, 0, 0), (0, 0, int(screen_size[0] / 3), int(screen_size[1] / 10)))
    font = pygame.font.Font(None, 72)
    text = font.render("Your score: " + str(score), True, (255, 255, 255))
    place = text.get_rect(center=(screen_size[0] / 6, screen_size[1] / 20))
    screen.blit(text, place)


def window_update():
    screen.fill(BLACK)
    draw_all_balls()
    score_window()


def raise_score():
    return score


pygame.display.update()
clock = pygame.time.Clock()
finished = False
window_update()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in BALLS:
                if (event.pos[0] - ball[0]) * (event.pos[0] - ball[0]) + (event.pos[1] - ball[1]) * (
                        event.pos[1] - ball[1]) < ball[2] * ball[2]:
                    score = score + 1
                    # print(event.pos[0], ball[0], event.pos[1], ball[1], ball[2])
                    ball[2] = 0
                # print(event.pos[0], ball[0], event.pos[1], ball[1], ball[2], score)
    pygame.display.update()
    window_update()
    time += 1

    # screen.fill(BLACK)

pygame.quit()
