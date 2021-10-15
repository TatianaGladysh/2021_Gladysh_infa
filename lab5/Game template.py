import pygame
import pygame.draw as dr
from random import randint

pygame.init()

FPS = 5
SCREEN_SIZE = (1200, 800)
screen = pygame.display.set_mode(SCREEN_SIZE)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

BALLS = []
for i in range(12):
    BALLS.append([0] * 4)
global score
score = 0


def new_ball():
    """
    рисует новый шарик случайного размера, цвета и положения
    """
    x = randint(100, SCREEN_SIZE[0] - 100)
    y = randint(100, SCREEN_SIZE[1] - 100)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    dr.circle(screen, color, (x, y), r)
    BALLS[BALLS[10][0]] = [x, y, r, color]
    BALLS[10][0] = (BALLS[10][0] + 1) % 10


def draw_all_balls():
    new_ball()
    for ball_parameters in BALLS:
        draw_ball(ball_parameters)


def draw_ball(parameters):
    dr.circle(screen, parameters[3], (parameters[0], parameters[1]), parameters[2])


def score_window():
    dr.rect(screen, (0, 0, 0), (0, 0, int(SCREEN_SIZE[0] / 2), int(SCREEN_SIZE[1] / 10)))
    font = pygame.font.Font(None, 72)
    text = font.render("Your score: " + str(score), True, (255, 255, 255))
    place = text.get_rect(center=(SCREEN_SIZE[0] / 4, SCREEN_SIZE[1] / 20))
    screen.blit(text, place)


def window_update():
    screen.fill(BLACK)
    draw_all_balls()
    score_window()


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
                        event.pos[1] - ball[1]) < ball[2]*ball[2]:
                    score = score + 1
                    print(event.pos[0], ball[0], event.pos[1], ball[1], ball[2])
                    ball[2] = 0
                print(event.pos[0], ball[0], event.pos[1], ball[1], ball[2], score)
    pygame.display.update()
    window_update()

    # screen.fill(BLACK)

pygame.quit()
