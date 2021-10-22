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
WHITE = (255, 255, 255)
BALL_COLORS = [GREEN, MAGENTA, CYAN, YELLOW]
BUG_COLORS = [RED, BLUE]

# game settings
time = 0
number_of_balls = 20
number_of_bugs = 5
speed_level = 1
score = 0
screen_size = (1200, 800)
score_window_size = int(screen_size[0]), int(screen_size[1] / 12)
bug_rest_time = 75
score_scale = [10, 100, 500, 1000]


# functions for balls
def draw_ball(color, x, y, radius):
    """
    Draw ball

    :param color: color of ball
    :param x: ball center coordinate x
    :param y: ball center coordinate y
    :param radius: ball radius
    """
    dr.circle(screen, BALL_COLORS[(color + 1) % len(BALL_COLORS)], (x, y), radius + 3)
    dr.circle(screen, BALL_COLORS[color], (x, y), radius)


def new_ball():
    """
    Generate new ball with random color, position and speed instead of ball in position new_position.
    Then add new ball to balls list.

    :return: new parameters of ball to write them to balls_list
    """
    x = randint(100 + score_window_size[1], screen_size[0] - 100)
    y = randint(100 + score_window_size[1], screen_size[1] - 100)
    radius = randint(20, 100)
    color = randint(0, len(BALL_COLORS) - 1)
    speed_x = randint(1, 50) / (21 - speed_level)
    speed_y = randint(1, 50) / (21 - speed_level)
    return [x, y, radius, color, speed_x, speed_y]


def draw_all_balls():
    """
    Draw all balls in balls_list
    """
    for number in range(number_of_balls):
        balls_list[number] = move_ball(*balls_list[number])


def move_ball(x, y, radius, color, speed_x, speed_y):
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
    draw_ball(color, x, y, radius)
    x = x + speed_x
    y = y + speed_y
    if x - radius < 0 or x + radius > screen_size[0]:
        speed_x = -speed_x
    elif y - radius < score_window_size[1] or y + radius > screen_size[1]:
        speed_y = -speed_y
    return [x, y, radius, color, speed_x, speed_y]


def make_brand_new_balls():
    """
    Build list of new balls
    """
    for number in range(number_of_balls):
        balls_list[number] = new_ball()


def count_ball_score(radius, speed_x, speed_y):
    """
    Count ball score as you want

    :param radius: ball radius
    :param speed_x: ball speed on the OX
    :param speed_y: ball speed on the OY
    """
    return max(int(1000 * speed_x * speed_x * speed_y * speed_y / (radius * radius)), 1)


# functions for bugs
def draw_bug(color, x, y, radius, speed, direction):
    """
        Draw bug

        :param color: color of bug
        :param x: bug center coordinate x
        :param y: bug center coordinate y
        :param radius: bug radius
        :param speed: bug speed
        :param direction: direction of moving: OX - 0, OY - 1
        """
    dr.circle(screen, BLACK, (x, y), radius + 1)
    dr.circle(screen, color, (x, y), radius)
    dr.circle(screen, BLACK, (x + radius * 7 / 9 * (1 - direction) * (int(speed > 0) - int(speed < 0)),
                              y + radius * 7 / 9 * direction * (int(speed > 0) - int(speed < 0))), radius * 3 / 5)


def new_bug():
    """
        Generate new bug with random color from BUG_COLORS, position and speed instead of bug in position new_position.
        Then add new bug to bugs list.

        :return: new parameters of bug to write them to bugs_list
        """
    x = randint(100 + score_window_size[1], screen_size[0] - 100)
    y = randint(100 + score_window_size[1], screen_size[1] - 100)
    radius = randint(15, 50)
    color = BUG_COLORS[randint(0, len(BUG_COLORS) - 1)]
    speed = randint(1, 50) / (21 - speed_level) * 150
    direction = randint(0, 1)
    return [x, y, radius, color, speed, direction]


def draw_all_bugs():
    """
        Draw all bugs in bugs_list
        """
    for number in range(number_of_bugs):
        bugs_list[number] = move_bug(*bugs_list[number])


def move_bug(x, y, radius, color, speed, direction):
    """
        Draw bug with given parameters and move it to the next position after small time

        :param x: coordinate x
        :param y: coordinate y
        :param radius: radius of bug
        :param color: color of bug
        :param speed: speed of bug
        :param direction: direction of bug: [OX, OY]
        :return: new position
        """
    if time % bug_rest_time == 0:
        x = x + speed * (1 - direction)
        y = y + speed * direction
        draw_bug(color, x, y, radius, speed, direction)
        if x - radius < 0 or x + radius > screen_size[0] or y - radius < score_window_size[1] or y + radius > \
                screen_size[
                    1]:
            speed = -speed
        if randint(1, 4) == 4:
            direction = 1 - direction
        return [x, y, radius, color, speed, direction]
    else:
        draw_bug(color, x, y, radius, speed, direction)
        return [x, y, radius, color, speed, direction]


def make_brand_new_bugs():
    """
       Build list of new bugs
       """
    for number in range(number_of_bugs):
        bugs_list[number] = new_bug()


def count_bug_score(radius, speed, direction):
    """
    Count bug score as you want

    :param radius: bug radius
    :param speed: bug speed on the OX
    :param direction: bug speed on the OY
    """
    return max(int(8 * speed * speed / (radius * radius)), 5) + randint(0, 50) * direction


# window functions
def score_window():
    """
    Draw score window
    """
    dr.rect(screen, WHITE, (0, 0, score_window_size[0], score_window_size[1]))
    font = pygame.font.Font(None, 60)
    if score_scale[0] <= score < score_scale[1]:
        text = font.render("GOOD! YOUR SCORE: " + str(score), True, BLACK)
    elif score_scale[1] <= score < score_scale[2]:
        text = font.render("WOW! YOUR SCORE: " + str(score), True, BLACK)
    elif score_scale[2] <= score < score_scale[3]:
        text = font.render("GREAT! YOUR SCORE: " + str(score), True, BLACK)
    elif score_scale[3] <= score:
        text = font.render("BRILLIANT! YOUR SCORE: " + str(score), True, BLACK)
    else:
        text = font.render("YOUR SCORE: " + str(score), True, BLACK)
    place = text.get_rect(center=(screen_size[0] / 2, screen_size[1] / 20))
    screen.blit(text, place)


def window_update():
    """
    Redraw picture after small time to simulate moving
    """
    screen.fill(WHITE)
    draw_all_balls()
    draw_all_bugs()
    score_window()


def catch_checking(click_place_x, click_place_y):
    """
    Check did player catch ball or bug?

    :param click_place_x: coordinate x of place, where player wants to catch
    :param click_place_y: coordinate x of place, where player wants to catch
    :return: points user got after this click
    """
    add_score = 0
    for ball_number in range(number_of_balls):
        ball_x, ball_y, ball_radius, ball_color, ball_speed_x, ball_speed_y = balls_list[ball_number]
        if (click_place_x - ball_x) * (click_place_x - ball_x) + (click_place_y - ball_y) * (
                click_place_y - ball_y) < ball_radius * ball_radius:
            add_score = count_ball_score(ball_radius, ball_speed_x, ball_speed_y)
            balls_list[ball_number] = new_ball()
    for bug_number in range(number_of_bugs):
        bug_x, bug_y, bug_radius, bug_color, bug_speed, bug_direction = bugs_list[bug_number]
        if (click_place_x - bug_x) * (click_place_x - bug_x) + (click_place_y - bug_y) * (
                click_place_y - bug_y) < bug_radius * bug_radius:
            add_score = count_bug_score(bug_radius, bug_speed, bug_direction)
            bugs_list[bug_number] = new_bug()
    return add_score


# communicate module
def meet_user():
    """
    Greet and get acquainted with player

    :return: player's name
    """
    print("Balls&Bugs")
    print("Hi!")
    print("Enter you name, we want to save your progress")
    name = input()
    print("Thank you! Open the game and enjoy playing!")
    print(
        "You can catch ball and bugs. You will get different points for different size. " +
        "If you catch a bug you get random number of points")
    print("When you will close the game, progress save automatically")
    return name


player_name = meet_user()
screen = pygame.display.set_mode(screen_size)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

# list of all balls, includes all ball parameters: x and y coordinate, radius, color, OX and OY speed
balls_list = [new_ball() for _ in range(number_of_balls)]
make_brand_new_balls()
# list of all bugs, includes all bug parameters: x and y coordinate, radius, color, speed and direction
bugs_list = [new_bug() for _ in range(number_of_bugs)]
make_brand_new_bugs()

window_update()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # update_rating()
            with open("results.txt", "a") as results:
                results.write(str(str(player_name) + ' ' + str(score)))
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            screen_size = (1200, 800)
            score_window_size = int(screen_size[0]), int(screen_size[1] / 12)
            if (
                    score_window_size[0] < event.pos[0] < screen_size[0],
                    score_window_size[1] < event.pos[1] < screen_size[1]):
                score = score + catch_checking(*event.pos)
        # score_window_event(*event.pos)
    pygame.display.update()
    window_update()
    time = time + 1

pygame.quit()
