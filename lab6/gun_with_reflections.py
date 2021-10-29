import math
from random import randint, choice
import pygame
import numpy as np

FPS = 30

RED = 0xFF0000
ORANGE = (255, 165, 0)
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [ORANGE, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# game screen parameters
WIDTH = 800
HEIGHT = 600

# Gun parameters
x0 = WIDTH / 10
y0 = HEIGHT * 9 / 10

score_window_size = [x0, HEIGHT - y0]

# ball parameters
attenuation_factor = 0.8
speed_k = 0.5
g = 1 * speed_k


def score_window(score):
    """
    Draw score window

    :param score: game score
    """
    pygame.draw.rect(game_screen, WHITE, (0, 0, int(score_window_size[0]), int(score_window_size[1])))
    font = pygame.font.Font(None, 60)
    text = font.render(str(score), True, BLACK)
    place = text.get_rect(center=(score_window_size[0] / 2, score_window_size[1] / 2))
    game_screen.blit(text, place)


def screen_update():
    """
    Draw gun, balls, score window
    """
    game_screen.fill(WHITE)
    score_window(number_of_hit_targets)
    gun.power_up()
    gun.draw(game_screen)
    for screen_target in targets:
        screen_target.draw()
    for screen_ball in balls:
        if screen_ball.life_time > 0:
            screen_ball.life_time -= 1
            screen_ball.move()
            screen_ball.draw()
    pygame.display.update()


def check_hits():
    """
    Check all hits

    :return: number of hit targets
    """
    check_number_of_hit_targets = 0
    for check_ball in balls:
        if check_ball.life_time > 0:
            check_ball.move()
            for i in range(len(targets)):
                if check_ball.hit_test(targets[i]) and targets[i].live:
                    targets[i].live = 0
                    targets[i].hit()
                    targets[i] = Target()
                    check_number_of_hit_targets += 1
    return check_number_of_hit_targets


class Ball:
    def __init__(self, screen: pygame.Surface, start_angle, power, x, y):
        """
        Class constructor

        :param screen: game display
        :param start_angle: angle of ball moving
        :param power: factor of velocity
        :param x: gun end coordinate x
        :param y: gun end coordinate y
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = 20
        self.speed_x = speed_k * power * math.cos(start_angle)
        self.speed_y = -speed_k * power * math.sin(start_angle)
        self.color = choice(GAME_COLORS)
        self.live = 5
        self.life_time = 50

    def move(self):
        """
        Move ball and get new ball parameters after small time
        """
        self.x += self.speed_x
        self.y = self.y + self.speed_y
        self.speed_y += g
        if self.x - self.radius < 0:
            self.speed_x = -attenuation_factor * self.speed_x
            self.x = self.radius
        elif self.x + self.radius > WIDTH:
            self.speed_x = -attenuation_factor * self.speed_x
            self.x = WIDTH - self.radius
        if self.y - self.radius < 0:
            self.speed_y = -attenuation_factor * self.speed_y
            self.y = self.radius
        elif self.y + self.radius > HEIGHT:
            self.speed_y = -attenuation_factor * self.speed_y
            self.y = HEIGHT - self.radius
        self.x += self.speed_x
        self.y = self.y + self.speed_y

    def draw(self):
        """
        Draw ball with given parameters
        """
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.radius + 1)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def hit_test(self, obj):
        """
        Check if this object hits this target

        :param obj: ball
        :return: True is object hits target or False
        """
        return (self.radius + obj.radius) * (self.radius + obj.radius) > (obj.x - self.x) * (obj.x - self.x) + (
                obj.y - self.y) * (
                       obj.y - self.y)


class Gun:
    def __init__(self, screen):
        """
        Initialisation of gun

        :param screen: game screen
        """
        self.screen = screen
        self.fire_power = 100
        self.targeting_on = 0
        self.angle = 1
        self.color = GREY
        self.width = 10

    def power_up(self):
        """
        Calculate the initial velocity coefficient for targeting, fire_power
        """
        if self.targeting_on:
            if self.fire_power < 200:
                self.fire_power += 1
            self.color = RED
        else:
            self.color = GREY
            self.fire_power = 100

    def start_fire(self):
        """
        Tick start of targeting
        """
        self.targeting_on = 1

    def end_fire(self):
        """
        Ball shot with given parameters
        """
        global balls, bullet
        bullet += 1
        balls.append(
            Ball(self.screen, self.angle, self.fire_power / 5, int(x0 + self.fire_power * math.cos(self.angle)),
                 int(y0 - self.fire_power * math.sin(self.angle))))
        self.targeting_on = 0
        self.fire_power = 100
        self.color = GREY

    def targeting(self, mouse_position):
        """
        Calculate gun angle
        Depends on mouse position on game screen

        :param mouse_position: mouse position now
        """""
        if mouse_position:
            if mouse_position.pos[0] - x0 != 0 and x0 < mouse_position.pos[0]:
                self.angle = math.atan((y0 - mouse_position.pos[1]) / (mouse_position.pos[0] - x0))
            elif mouse_position.pos[0] - x0 != 0 and x0 > mouse_position.pos[0]:
                self.angle = math.atan((y0 - mouse_position.pos[1]) / (mouse_position.pos[0] - x0)) + np.pi
            else:
                self.angle = np.pi / 2

    def draw(self, screen):
        """
        Draw gun on given game screen

        :param screen: game screen
        """
        pygame.draw.polygon(screen, self.color, (
            (x0, y0), (x0 + self.fire_power * math.cos(self.angle), y0 - self.fire_power * math.sin(self.angle)),
            (x0 - self.width * math.sin(self.angle) + self.fire_power * math.cos(self.angle),
             y0 - self.width * math.cos(self.angle) - self.fire_power * math.sin(self.angle)),
            (x0 - self.width * math.sin(self.angle), y0 - self.width * math.cos(self.angle))))


class Target:
    def __init__(self):
        """
        New target initialisation
        """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.radius = randint(2, 50)
        self.color = RED
        # self.points = 10000 / (self.r) ** 2
        self.live = 1
        self.screen = game_screen

    def hit(self):
        """
        Tick if hit the target
        """
        # self.points += 1
        self.live = 0

    def draw(self):
        """
        Draw target with given parameters
        """
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.radius + 1)
        pygame.draw.circle(self.screen, RED, (self.x, self.y), self.radius)


pygame.init()
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
number_of_hit_targets = 0
# points = 0
bullet = 0
balls = []
targets = []

clock = pygame.time.Clock()
gun = Gun(game_screen)
targets.append(Target())
targets.append(Target())

finished = False

while not finished:
    screen_update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.start_fire()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.end_fire()
        elif event.type == pygame.MOUSEMOTION:
            gun.targeting(event)
    number_of_hit_targets += check_hits()
pygame.quit()
