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
WIDTH = 1200
HEIGHT = 800

# target parameters
max_target_radius = 50

# ball parameters
attenuation_factor = 0.8
speed_coefficient = 0.5 * WIDTH * HEIGHT / 800 / 600
g = 1 * speed_coefficient

# gun parameters
x0 = WIDTH / 10
y0 = HEIGHT * 9 / 10


class ScoreWindow:
    def __init__(self):
        self.score = 0
        self.size = [WIDTH/10, HEIGHT/10]

    def draw(self):
        """
        Draw score window
        """
        pygame.draw.rect(game_screen, WHITE, (0, 0, int(self.size[0]), int(self.size[1])))
        font = pygame.font.Font(None, 60)
        text = font.render(str(self.score), True, BLACK)
        place = text.get_rect(center=(self.size[0] / 2, self.size[1] / 2))
        game_screen.blit(text, place)


def screen_update():
    """
    Draw gun, balls, score window
    """
    game_screen.fill(WHITE)
    score_window.score += number_of_hit_targets
    score_window.draw()
    gun1.power_up()
    gun1.draw(game_screen)
    for screen_target in targets:
        screen_target.move()
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
        self.speed_x = speed_coefficient * power * math.cos(start_angle)
        self.speed_y = -speed_coefficient * power * math.sin(start_angle)
        self.color = choice(GAME_COLORS)
        self.life = 5
        self.life_time = 30

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
                obj.y - self.y) * (obj.y - self.y)


class Gun:
    def __init__(self, screen, x0, y0):
        """
        Initialisation of gun

        :param screen: game screen
        :param x0: place of man head
        :param y0: place of man head
        """
        self.screen = screen
        self.fire_power = 100
        self.targeting_on = 0
        self.angle = 1
        self.color = GREY
        self.width = 10
        self.x0 = x0
        self.y0 = y0

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

        :return: new ball
        """
        self.targeting_on = 0
        self.fire_power = 100
        self.color = GREY
        return Ball(self.screen, self.angle, self.fire_power / 5, int(x0 + self.fire_power * math.cos(self.angle)),
                    int(y0 - self.fire_power * math.sin(self.angle)))

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
        x0 = self.x0
        y0 = self.y0
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
        self.x = randint(int(WIDTH / 2), WIDTH - max_target_radius)
        self.y = randint(max_target_radius, HEIGHT - max_target_radius)
        self.speed_x = 0
        self.speed_y = randint(1, 15)
        self.radius = randint(30, max_target_radius)
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

    def move(self):
        # self.x += self.speed_x
        self.y = self.y + self.speed_y
        # self.speed_y += g
        # if self.x - self.radius < 0:
        #     self.speed_x = -attenuation_factor * self.speed_x
        #     self.x = self.radius
        # elif self.x + self.radius > WIDTH:
        #     self.speed_x = -attenuation_factor * self.speed_x
        #     self.x = WIDTH - self.radius
        if self.y - self.radius < 0:
            self.speed_y = -attenuation_factor * self.speed_y
            self.y = self.radius
        elif self.y + self.radius > HEIGHT:
            self.speed_y = -attenuation_factor * self.speed_y
            self.y = HEIGHT - self.radius
        # self.x += self.speed_x
        self.y = self.y + self.speed_y


pygame.init()
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

number_of_hit_targets = 0
# points = 0

# lists of all balls and all targets
balls = []
targets = []

# new objects
gun1 = Gun(game_screen, WIDTH / 4, HEIGHT * 3 / 2)
gun2 = Gun(game_screen, WIDTH * 3 / 4, HEIGHT * 3 / 2)
targets.append(Target())
targets.append(Target())
score_window = ScoreWindow()
finished = False

while not finished:
    screen_update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.K_z:
            gun1.fire_power += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            balls.append(gun1.end_fire())
        elif event.type == pygame.MOUSEMOTION:
            gun1.targeting(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun1.start_fire()
        elif event.type == pygame.MOUSEBUTTONUP:
            balls.append(gun1.end_fire())
        elif event.type == pygame.MOUSEMOTION:
            gun1.targeting(event)
    number_of_hit_targets += check_hits()

pygame.quit()
