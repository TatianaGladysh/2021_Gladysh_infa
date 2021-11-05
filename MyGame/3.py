import math
from random import randint, choice
import pygame
import numpy as np

FPS = 30

RED = 0xFF0000
POWDER_BLUE = (176, 224, 230)
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
SKY = HEIGHT / 20
GROUND = HEIGHT * 2 / 3
WATER = GROUND + WIDTH / 20

# gun parameters
# x0 = WIDTH / 10
y0 = HEIGHT * 9 / 10
start_gun_power = 50

left_gun_x = WIDTH / 10
left_gun_y = GROUND
right_gun_x = WIDTH - left_gun_x
right_gun_y = left_gun_y

# target parameters
max_target_radius = 30

# ball parameters
attenuation_factor = 0.8
speed_coefficient = 1 * WIDTH * HEIGHT / 800 / 600
g = 1 * speed_coefficient
water_g = g / 3

score_window_size = [WIDTH / 10, HEIGHT / 10]


def score_window():
    """
    Draw score window

    """
    pygame.draw.rect(game_screen, left_player.color, (0, 0, int(WIDTH / 2), int(SKY)))
    pygame.draw.rect(game_screen, right_player.color, (int(WIDTH / 2), 0, int(WIDTH), int(SKY)))
    font = pygame.font.Font(None, 60)
    text = font.render(str(int(left_player.score)), True, BLACK)
    place = text.get_rect(center=(int(WIDTH / 4), int(SKY / 2)))
    game_screen.blit(text, place)
    font = pygame.font.Font(None, 60)
    text = font.render(str(int(right_player.score)), True, BLACK)
    place = text.get_rect(center=(int(WIDTH * 3 / 4), int(SKY / 2)))
    game_screen.blit(text, place)


def screen_update():
    """
    Draw gun, balls, score window
    """
    left_player.check_hits()
    right_player.check_hits()
    game_screen.fill(WHITE)
    pygame.draw.rect(game_screen, WHITE, (0, int(SKY), int(WIDTH), int(GROUND)))
    pygame.draw.rect(game_screen, POWDER_BLUE, (0, int(GROUND), int(WIDTH), int(HEIGHT)))
    score_window()
    left_player.gun.draw(game_screen)
    right_player.gun.draw(game_screen)
    for screen_ball in right_player.balls:
        screen_ball.move()
        if screen_ball.live == 1:
            screen_ball.draw()
            left_player.score += left_player.gun.hit_test(screen_ball)
    for screen_ball in left_player.balls:
        screen_ball.move()
        if screen_ball.live == 1:
            screen_ball.draw()
            right_player.score += right_player.gun.hit_test(screen_ball)
    for i in range(len(targets)):
        targets[i].move()
        if targets[i].live == 1:
            targets[i].draw()
        else:
            # if targets[i].life_time != 0:
            #     targets[i].color = RED
            #     targets[i].draw()
            if isinstance(targets[i], Fish):
                if targets[i].live == 0 and targets[i].life_time != 0:
                    a = randint(3, 7)
                    for i in range(a):
                        targets.append(Feather(i, a, targets[i].x, targets[i].y))
                targets[i] = Fish()
            elif isinstance(targets[i], Bird):
                targets[i] = Bird()
    pygame.display.update()


class Player:
    def __init__(self, player_number, start_x, start_y, game_screen_left_border, game_screen_right_border, color=CYAN):
        self.number = player_number
        self.score = 0
        self.color = color
        self.position_x = start_x
        self.position_y = start_y
        self.gun = Gun(self.number, game_screen, self.position_x, self.position_y, self.color, game_screen_left_border,
                       game_screen_right_border)
        self.balls = []

    def process_event(self, one_event):
        game_end = False
        if one_event.type == pygame.QUIT:
            game_end = True
        if self.number == 1:
            if event.type == pygame.KEYDOWN:
                if event.mod != pygame.KMOD_LSHIFT and event.key == pygame.K_a:
                    self.gun.targeting('left')
                elif event.mod != pygame.KMOD_LSHIFT and event.key == pygame.K_d:
                    self.gun.targeting('right')
                elif event.mod == pygame.KMOD_LSHIFT and event.key == pygame.K_a:
                    self.gun.moving('left')
                elif event.mod == pygame.KMOD_LSHIFT and event.key == pygame.K_d:
                    self.gun.moving('right')
                elif event.mod != pygame.KMOD_LSHIFT and event.key == pygame.K_w:
                    self.balls.append(self.gun.fire())
                elif event.mod == pygame.KMOD_LSHIFT and event.key == pygame.K_w:
                    if self.gun.fire_power >= start_gun_power * 2:
                        self.balls.append(self.gun.power_up())
                    else:
                        self.gun.power_up()
                elif event.mod == pygame.KMOD_LSHIFT and event.key == pygame.K_s:
                    pass
        else:
            if event.type == pygame.KEYDOWN:
                if event.mod != pygame.KMOD_RSHIFT and event.key == pygame.K_LEFT:
                    self.gun.targeting('left')
                elif event.mod != pygame.KMOD_RSHIFT and event.key == pygame.K_RIGHT:
                    self.gun.targeting('right')
                elif event.mod == pygame.KMOD_RSHIFT and event.key == pygame.K_LEFT:
                    self.gun.moving('left')
                elif event.mod == pygame.KMOD_RSHIFT and event.key == pygame.K_RIGHT:
                    self.gun.moving('right')
                elif event.mod != pygame.KMOD_RSHIFT and event.key == pygame.K_UP:
                    self.balls.append(self.gun.fire())
                elif event.mod == pygame.KMOD_RSHIFT and event.key == pygame.K_UP:
                    if self.gun.fire_power >= start_gun_power * 2:
                        self.balls.append(self.gun.power_up())
                    else:
                        self.gun.power_up()
                elif event.mod == pygame.KMOD_RSHIFT and event.key == pygame.K_DOWN:
                    pass

        return game_end

    def check_hits(self):
        """
        Check all hits

        :return: number of hit targets
        """
        check_number_of_hit_targets = 0
        for check_ball in self.balls:
            check_ball.move()
            if check_ball.live:
                for i in range(len(targets)):
                    if targets[i].live:
                        self.score += targets[i].hit_test(check_ball)


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
        self.radius = 4
        self.speed_x = speed_coefficient * power * math.cos(start_angle)
        self.speed_y = -speed_coefficient * power * math.sin(start_angle)
        self.color = choice(GAME_COLORS)
        self.live = 1

    def move(self):
        """
        Move ball and get new ball parameters after small time
        """
        if self.x < 0 or self.x > WIDTH or self.y > GROUND:
            self.live = 0
        else:
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


class Hook:
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
        self.radius = 4
        self.speed_x = speed_coefficient * power * math.cos(start_angle)
        self.speed_y = -speed_coefficient * power * math.sin(start_angle)
        self.color = choice(GAME_COLORS)
        self.live = 1

    def move(self):
        """
        Move ball and get new ball parameters after small time
        """
        if self.x < 0 or self.x > WIDTH or self.y < GROUND or self.y > HEIGHT:
            self.live = 0
        else:
            self.x += self.speed_x
            self.y = self.y + self.speed_y
            self.speed_y -= water_g
            if self.speed_x > 0:
                self.speed_x -= water_g
            else:
                self.speed_x += water_g
            self.x += self.speed_x
            self.y = self.y + self.speed_y

    def draw(self):
        """
        Draw ball with given parameters
        """
        pygame.draw.rect(self.screen, BLACK,
                         (self.x - self.radius / 2, self.y - self.radius / 2, self.radius, self.radius))
        # pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.radius + 1)
        # pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)


class Gun:
    def __init__(self, number, screen, x, y, head_color, left_border, right_border):
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
        self.right_border = right_border
        self.left_border = left_border
        self.head_color = head_color
        self.radius = self.length / 6
        # self.head = Head(self.length / 6, head_color, screen, self.x, self.y)

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
        if 0 < self.angle < np.pi:
            self.color = GREY
            new_ball = Ball(self.screen, self.angle, self.fire_power / 5,
                            int(self.x + self.length * math.cos(self.angle)),
                            int(self.y - self.length * math.sin(self.angle)))
            self.fire_power = start_gun_power
            return new_ball
        else:
            self.color = GREY
            new_hook = Hook(self.screen, self.angle, self.fire_power / 5,
                            int(self.x + self.length * math.cos(self.angle)),
                            int(self.y - self.length * math.sin(self.angle)))
            self.fire_power = start_gun_power
            return new_hook

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
        if direction == 'right' and self.x < self.right_border:
            self.x = self.x + self._moving_speed
        elif direction == 'left' and self.x > self.left_border:
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
        pygame.draw.circle(self.screen, self.head_color, (self.x, self.y), self.radius)

    def hit_test(self, object):
        if (self.radius + object.radius) * (self.radius + object.radius) > (object.x - self.x) * (object.x - self.x) + (
                object.y - self.y) * (object.y - self.y):
            self.live = 0
            return -400
        else:
            return 0


class Target:
    def __init__(self):
        self.live = 1

    def move(self):
        pass

    def draw(self):
        pass

    def hit_test(self, object):
        pass


class Feather(Target):
    def __init__(self, number, all_number, x, y):
        super().__init__()
        self.x = x + (randint(1, 5) + 5) * np.cos(number * np.pi * 2 / all_number)
        self.y = y + (randint(1, 5) + 5) * np.sin(number * np.pi * 2 / all_number)
        # self.speed_x = randint(1, 15)*np.cos(number*np.pi*2/all_number)
        # self.speed_y = -randint(1, 15)*np.sin(number*np.pi*2/all_number)
        self.radius = randint(3, max_target_radius / 3)
        self.color = YELLOW
        self.screen = game_screen
        self.life_time = 50

    def draw(self):
        """
        Draw target with given parameters
        """
        self.life_time -= 1
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        if self.life_time <= 0:
            self.live = 0

    def hit_test(self, obj):
        if (self.radius + obj.radius) * (self.radius + obj.radius) > (obj.x - self.x) * (obj.x - self.x) + (
                obj.y - self.y) * (obj.y - self.y):
            self.live = 0
            return 300
        else:
            return 0


class Bird(Target):
    def __init__(self):
        super().__init__()

        self.speed_x = randint(1, 15) * choice([1, -1])
        self.speed_y = 0
        self.x = (0 - max_target_radius / 2) * int(bool(self.speed_x > 0)) + (WIDTH - max_target_radius) * int(
            bool(self.speed_x < 0))
        self.y = randint(int(max_target_radius + SKY), int((GROUND - max_target_radius) / 2))
        self.radius = randint(30, max_target_radius)
        self.color = choice(GAME_COLORS)
        self.screen = game_screen
        self.life_time = 1
        self.live = 1

    def draw(self):
        """
        Draw target with given parameters
        """
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.radius + 1)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):

        self.x += self.speed_x
        if self.x + self.radius < 0:
            self.live = 0
        elif self.x - self.radius > WIDTH:
            self.live = 0

    def hit_test(self, obj):
        if (self.radius + obj.radius) * (self.radius + obj.radius) > (obj.x - self.x) * (obj.x - self.x) + (
                obj.y - self.y) * (obj.y - self.y):
            self.live = 0
            return 200 / self.y * 300 / abs(self.speed_x)
        else:
            return 0


class Fish(Target):
    def __init__(self):
        """
        New target initialisation
        """
        super().__init__()
        self.x = randint(int(0 + max_target_radius), int(WIDTH - max_target_radius))
        self.y = randint(int(WATER + max_target_radius), int(HEIGHT - max_target_radius))
        self.speed_x = randint(1, 5)
        self.speed_y = randint(1, 5)
        self.radius = randint(15, max_target_radius)
        self.color = GREY
        self.screen = game_screen
        self.life_time = randint(500, 1000)
        self.live = 1

    def draw(self):
        """
        Draw target with given parameters
        """
        self.life_time = self.life_time - 1
        if self.life_time <= 0:
            self.live = 0
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.life_time -= 1
        if self.life_time <= 0:
            self.live = 0
        self.x += self.speed_x
        self.y = self.y + self.speed_y
        # self.speed_y += g
        if self.x - self.radius < 0:
            self.speed_x = -attenuation_factor * self.speed_x
            self.x = self.radius
        elif self.x + self.radius > WIDTH:
            self.speed_x = -attenuation_factor * self.speed_x
            self.x = WIDTH - self.radius
        if self.y - self.radius < WATER:
            self.speed_y = -attenuation_factor * self.speed_y
            self.y = self.radius + WATER
        elif self.y + self.radius > HEIGHT:
            self.speed_y = -attenuation_factor * self.speed_y
            self.y = HEIGHT - self.radius
        self.x += self.speed_x
        self.y = self.y + self.speed_y

    def hit_test(self, obj):
        if (self.radius + obj.radius) * (self.radius + obj.radius) > (obj.x - self.x) * (obj.x - self.x) + (
                obj.y - self.y) * (obj.y - self.y):
            self.live = 0
            return 100 * (30 - self.radius)
        else:
            return 0


pygame.init()
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# points = 0

# lists of all balls and all targets
targets = []

# new objects
left_player = Player(1, left_gun_x, left_gun_y, 0, WIDTH / 2, RED)
right_player = Player(2, right_gun_x, right_gun_y, WIDTH / 2, WIDTH, GREEN)

for i in range(8):
    targets.append(Fish())
    targets.append(Bird())

finished = False

while not finished:
    screen_update()
    clock.tick(FPS)
    for event in pygame.event.get():
        finished = left_player.process_event(event)
        finished = right_player.process_event(event)
pygame.quit()