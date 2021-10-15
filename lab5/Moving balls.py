import pygame
import pygame.draw as dr
from random import randint

pygame.init()

FPS = 100

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# game settings
number_of_balls = 10
speed_level = 1
score = 0
screen_size = (1200, 800)
score_window_size = int(screen_size[0]), int(screen_size[1] / 12)


def new_ball():
    """
    Generate new ball with random color, position and speed instead of ball in position new_position.
    Then add new ball to balls list.

    :return: new parameters of ball to write them to balls_list
    """
    x = randint(100 + score_window_size[1], screen_size[0] - 100)
    y = randint(100 + score_window_size[1], screen_size[1] - 100)
    radius = randint(20, 100)
    color = COLORS[randint(0, len(COLORS) - 1)]
    speed_x = randint(1, 50) / (21 - speed_level)
    speed_y = randint(1, 50) / (21 - speed_level)
    return [x, y, radius, color, speed_x, speed_y]


def draw_all_balls():
    """
    Draw all balls in balls_list
    """
    for number in range(number_of_balls + 1):
        balls_list[number] = draw_ball(*balls_list[number])


def draw_ball(x, y, radius, color, speed_x, speed_y):
    """
    Draw ball with given parameters and move it to the next position after small time

    :param x: coordinate x
    :param y: coordinate y
    :param radius: radius of ball
    :param color: color of ball
    :param speed_x: OX speed of ball
    :param speed_y: OY speed of ball
    :return: new position
    """
    dr.circle(screen, color, (x + speed_x, y + speed_y), radius)
    x = x + speed_x
    y = y + speed_y
    if x - radius < 0 or x + radius > screen_size[0]:
        speed_x = -speed_x
    elif y - radius < score_window_size[1] or y + radius > screen_size[1]:
        speed_y = -speed_y
    return [x, y, radius, color, speed_x, speed_y]


def score_window():
    """
    Draw score window
    """
    dr.rect(screen, (0, 0, 0), (0, 0, score_window_size[0], score_window_size[1]))
    font = pygame.font.Font(None, 60)
    if 3 <= score < 20:
        text = font.render("GOOD! YOUR SCORE: " + str(score), True, (255, 255, 255))
    elif 20 <= score < 50:
        text = font.render("GREAT! YOUR SCORE: " + str(score), True, (255, 255, 255))
    elif 50 <= score:
        text = font.render("BRILLIANT! YOUR SCORE: " + str(score), True, (255, 255, 255))
    else:
        text = font.render("YOUR SCORE: " + str(score), True, (255, 255, 255))
    place = text.get_rect(center=(screen_size[0] / 2, screen_size[1] / 20))
    screen.blit(text, place)


def window_update():
    """
    Redraw picture after small time to simulate moving
    """
    screen.fill(BLACK)
    draw_all_balls()
    score_window()


def make_brand_new_balls():
    """
    Build list of new balls
    """
    for number in range(number_of_balls):
        balls_list[number] = new_ball()


def count_score(radius, speed_x, speed_y):
    """
    Count ball score as you want

    :param radius: ball radius
    :param speed_x: ball speed on the OX
    :param speed_y: ball speed on the OY
    """
    return max(int(1000 * speed_x * speed_x * speed_y * speed_y / (radius * radius)), 1)


def catch_checking(click_place_x, click_place_y):
    """
    Check did player catch ball?
    :param click_place_x: coordinate x of place, where player wants to catch
    :param click_place_y: coordinate x of place, where player wants to catch
    :return: points user got after this click
    """
    add_score = 0
    for ball_number in range(number_of_balls):
        ball_x, ball_y, ball_radius, ball_color, ball_speed_x, ball_speed_y = balls_list[ball_number]
        if (click_place_x - ball_x) * (click_place_x - ball_x) + (click_place_y - ball_y) * (
                click_place_y - ball_y) < ball_radius * ball_radius:
            add_score = count_score(ball_radius, ball_speed_x, ball_speed_y)
            balls_list[ball_number] = new_ball()
    return add_score


screen = pygame.display.set_mode(screen_size)
pygame.display.update()
clock = pygame.time.Clock()
finished = False
window_update()

# list of all balls, includes all ball parameters: x and y coordinate, radius, color, OX and OY speed
balls_list = [new_ball() for i in range(number_of_balls + 1)]
make_brand_new_balls()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            score = score + catch_checking(*event.pos)
    pygame.display.update()
    window_update()

pygame.quit()
