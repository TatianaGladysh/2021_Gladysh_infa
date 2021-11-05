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
GROUND = HEIGHT / 2

# gun parameters
# x0 = WIDTH / 10
y0 = HEIGHT * 9 / 10
start_gun_power = 50

left_gun_x = WIDTH / 10
left_gun_y = GROUND
right_gun_x = WIDTH - left_gun_x
right_gun_y = left_gun_y

# target parameters
max_target_radius = 50

# ball parameters
attenuation_factor = 0.8
speed_coefficient = 1 * WIDTH * HEIGHT / 800 / 600
g = 1 * speed_coefficient

score_window_size = [WIDTH / 10, HEIGHT / 10]


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
    left_player.gun.draw(game_screen)
    right_player.gun.draw(game_screen)
    right_player.gun.draw(game_screen)
    for screen_target in targets:
        screen_target.move()
        screen_target.draw()
    for screen_ball in balls:
        if screen_ball.life == 1:
            screen_ball.move()
            screen_ball.draw()
        if screen_ball.x < 0 or screen_ball.x > WIDTH or screen_ball.y > GROUND:
            screen_ball.life = 0
    pygame.display.update()


def check_hits():
    """
    Check all hits

    :return: number of hit targets
    """
    check_number_of_hit_targets = 0
    for check_ball in balls:
        if check_ball.life > 0:
            check_ball.move()
            for i in range(len(targets)):
                if check_ball.hit_test(targets[i]) and targets[i].live:
                    targets[i].live = 0
                    targets[i].hit()
                    targets[i] = Target()
                    check_number_of_hit_targets += 1
    return check_number_of_hit_targets


class Player:
    def __init__(self, player_number, start_x, start_y, game_screen_left_border, game_screen_right_border, color=CYAN):
        self.number = player_number
        self.score = 0
        self.color = color
        self.position_x = start_x
        self.position_y = start_y
        self.gun = Gun(self.number, game_screen, self.position_x, self.position_y, self.color, game_screen_left_border,
                       game_screen_right_border)

    def process_event(self, one_event):
        game_end = False
        if self.number == 1:
            if one_event.type == pygame.QUIT:
                game_end = True
            elif event.type == pygame.KEYDOWN:
                if event.mod == pygame.KMOD_NONE and event.key == pygame.K_a:
                    self.gun.targeting('left')
                elif event.mod == pygame.KMOD_NONE and event.key == pygame.K_d:
                    self.gun.targeting('right')
                elif event.mod == pygame.KMOD_LSHIFT and event.key == pygame.K_a:
                    self.gun.moving('left')
                elif event.mod == pygame.KMOD_LSHIFT and event.key == pygame.K_d:
                    self.gun.moving('right')
                elif event.mod == pygame.KMOD_NONE and event.key == pygame.K_w:
                    balls.append(self.gun.fire())
                    print(7)
                elif event.mod == pygame.KMOD_LSHIFT and event.key == pygame.K_w:
                    if self.gun.fire_power >= start_gun_power * 2:
                        balls.append(self.gun.power_up())
                    else:
                        self.gun.power_up()
                elif event.mod == pygame.KMOD_LSHIFT and event.key == pygame.K_s:
                    pass
        else:
            if one_event.type == pygame.QUIT:
                game_end = True
            elif event.type == pygame.KEYDOWN:
                if event.mod == pygame.KMOD_NONE and event.key == pygame.K_LEFT:
                    self.gun.targeting('left')
                elif event.mod == pygame.KMOD_NONE and event.key == pygame.K_RIGHT:
                    self.gun.targeting('right')
                elif event.mod == pygame.KMOD_RSHIFT and event.key == pygame.K_LEFT:
                    self.gun.moving('left')
                elif event.mod == pygame.KMOD_RSHIFT and event.key == pygame.K_RIGHT:
                    self.gun.moving('right')
                elif event.mod == pygame.KMOD_NONE and event.key == pygame.K_UP:
                    balls.append(self.gun.fire())
                    print(7)
                elif event.mod == pygame.KMOD_RSHIFT and event.key == pygame.K_UP:
                    if self.gun.fire_power >= start_gun_power * 2:
                        balls.append(self.gun.power_up())
                    else:
                        self.gun.power_up()
                elif event.mod == pygame.KMOD_RSHIFT and event.key == pygame.K_DOWN:
                    pass

        return game_end


class Ball:
    def __init__(self, screen: pygame.Surface, start_angle, power, x, y, number):
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
        self.radius = 4
        self.speed_x = speed_coefficient * power * math.cos(start_angle)
        self.speed_y = -speed_coefficient * power * math.sin(start_angle)
        self.color = choice(GAME_COLORS)
        self.life = 5
        self.life = 1
        self.player = number

    def move(self):
        """
        Move ball and get new ball parameters after small time
        """
        self.x += self.speed_x
        self.y = self.y + self.speed_y
        self.speed_y += g
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
    def __init__(self, number, screen, x, y, head_color, left_bowder, right_bowder):
        """
        Initialisation of gun

        :param screen: game screen
        """
        self.number = number
        self.screen = screen
        self.fire_power = start_gun_power
        # self.targeting_on = 0
        self.angle = np.pi / 2
        self.color = GREY
        self.width = 10
        self.x = x
        self.y = y
        self._rotation_speed = 0.1
        self._moving_speed = 10
        self._powering_speed = 5
        self.length = 2 * start_gun_power
        self.head_size = self.length / 6
        self.head_color = head_color
        self.right_bowder = right_bowder
        self.left_bowder = left_bowder

    def power_up(self):
        """
        Calculate the initial velocity coefficient for targeting, fire_power
        """
        if self.fire_power > start_gun_power * 18 / 10:
            self.color = RED
        if self.fire_power < start_gun_power * 2:
            self.fire_power += self._powering_speed
        else:
            new_ball = self.fire()
            self.fire_power = start_gun_power
            self.color = GREY
            return new_ball

    def fire(self):
        """
        Ball shot with given parametersW

        :return: new ball
        """
        self.color = GREY
        new_ball = Ball(self.screen, self.angle, self.fire_power / 5,
                        int(self.x + self.length * math.cos(self.angle)),
                        int(self.y - self.length * math.sin(self.angle)), self.number)
        self.fire_power = start_gun_power
        return new_ball

    def targeting(self, direction):
        """
        Calculate gun new angle

        :param direction: direction of rotation, left or right
        """
        if direction == 'right':
            self.angle = self.angle - self._rotation_speed
        else:
            self.angle = self.angle + self._rotation_speed

    def moving(self, direction):
        if direction == 'right' and self.x < self.right_bowder:
            self.x = self.x + self._moving_speed
        elif direction == 'left' and self.x > self.left_bowder:
            self.x = self.x - self._moving_speed

    def draw(self, screen):
        """
        Draw gun on given game screen

        :param screen: game screen
        """
        self.length = start_gun_power * 3 - self.fire_power
        self.width = start_gun_power * start_gun_power / 5 / self.length
        pygame.draw.polygon(self.screen, self.color, (
            (self.x + self.width / 2 * math.sin(self.angle), self.y + self.width / 2 * math.cos(self.angle)),
            (self.x + self.length * math.cos(self.angle) + self.width / 2 * math.sin(self.angle),
             self.y - self.length * math.sin(self.angle) + self.width / 2 * math.cos(self.angle)),
            (
                self.x - self.width * math.sin(self.angle) + self.length * math.cos(
                    self.angle) + self.width / 2 * math.sin(
                    self.angle),
                self.y - self.width * math.cos(self.angle) - self.length * math.sin(
                    self.angle) + self.width / 2 * math.cos(
                    self.angle)),
            (self.x - self.width * math.sin(self.angle) + self.width / 2 * math.sin(self.angle),
             self.y - self.width * math.cos(self.angle) + self.width / 2 * math.cos(self.angle))))
        pygame.draw.circle(self.screen, self.head_color, (self.x, self.y), self.head_size)


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
left_player = Player(1, left_gun_x, left_gun_y, 0, WIDTH / 2, CYAN)
right_player = Player(2, right_gun_x, right_gun_y, WIDTH / 2, WIDTH, GREEN)

# left_gun = Gun(game_screen, left_player.position_x, left_player.position_y, left_player.color, 0, WIDTH/2)
# right_gun = Gun(game_screen, right_player.position_x, right_player.position_y, right_player.color, WIDTH/2, WIDTH)

targets.append(Target())
targets.append(Target())

finished = False

while not finished:
    screen_update()
    clock.tick(FPS)
    for event in pygame.event.get():
        finished = left_player.process_event(event)
        finished = right_player.process_event(event)
    number_of_hit_targets += check_hits()
pygame.quit()
