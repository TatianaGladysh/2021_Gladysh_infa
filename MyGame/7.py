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
DARK_GREEN = (0, 100, 0)
FOREST_GREEN = (34, 139, 34)
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
start_gun_power = 50

# target parameters
max_target_radius = 30

# ball parameters
attenuation_factor = 0.8
speed_coefficient = 1 * WIDTH * HEIGHT / 800 / 600
g = 1 * speed_coefficient
water_g = g / 3


def draw_text_line(text_line1, text_line2, text_line3, height1, height2):
    """
    Draw 3 text lines for first screen. One live above two others

    :param text_line1: main line
    :param text_line2: line for left player
    :param text_line3: line for right player
    :param height1: center coordinate y of text_line1 line
    :param height2: center coordinate y of text_line2 and text_line3 line
    """
    font = pygame.font.Font(None, 40)
    text = font.render(text_line1, True, BLACK)
    place = text.get_rect(center=(int(WIDTH / 2), int(height1)))
    game_screen.blit(text, place)
    font = pygame.font.Font(None, 30)
    text = font.render(text_line2, True, RED)
    place = text.get_rect(center=(int(WIDTH * 2 / 5), int(height2)))
    game_screen.blit(text, place)
    font = pygame.font.Font(None, 30)
    text = font.render(text_line3, True, RED)
    place = text.get_rect(center=(int(WIDTH * 3 / 5), int(height2)))
    game_screen.blit(text, place)


def first_screen():
    """
    Draw greetings screen with game rules and key functions
    """
    block_height = HEIGHT / 23
    game_screen.fill(FOREST_GREEN)
    font = pygame.font.Font(None, 200)
    title = font.render('HUNTERS', True, BLACK)
    game_screen.blit(title, title.get_rect(center=(int(WIDTH / 2), int(block_height * 3))))
    line_number = 6
    draw_text_line('to rotate gun clockwise', 'd', 'right', block_height * line_number,
                   block_height * (line_number + 1))
    line_number += 3
    draw_text_line('to rotate gun counterclockwise', 'a', 'left', block_height * line_number,
                   block_height * (line_number + 1))
    line_number += 3
    draw_text_line('to move hunter to the right', 'left shift + d', 'right shift + right', block_height * line_number,
                   block_height * (line_number + 1))
    line_number += 3
    draw_text_line('to move hunter to the left', 'left shift + a', 'right shift + left', block_height * line_number,
                   block_height * (line_number + 1))
    line_number += 3
    draw_text_line('to increase shot power', 'left shift + w', 'right shift + up', block_height * line_number,
                   block_height * (line_number + 1))
    line_number += 3
    draw_text_line('to shoot', 'w', 'up', block_height * line_number, block_height * (line_number + 1))
    pygame.display.update()


def score_window():
    """
    Draw score window for two players
    """
    for player in players:
        pygame.draw.rect(game_screen, player.color, (player.left_border, 0, int(player.right_border), int(SKY)))
        font = pygame.font.Font(None, 60)
        text = font.render(str(int(player.score)), True, BLACK)
        place = text.get_rect(center=(int((player.right_border + player.left_border) / 2), int(SKY / 2)))
        game_screen.blit(text, place)


def random_color():
    """
    Generate random new color

    :return: random new color
    """
    color_number_1 = randint(0, 255)
    color_number_2 = randint(0, 255)
    color_number_3 = randint(0, 255)
    return [color_number_1, color_number_2, color_number_3]


def screen_update():
    """
    Update scores
    Move balls, hooks, hunters, targets
    Draw new screen
    """
    for player in players:
        player.check_hits()
    game_screen.fill(WHITE)
    pygame.draw.rect(game_screen, WHITE, (0, int(SKY), int(WIDTH), int(GROUND - SKY)))
    pygame.draw.rect(game_screen, POWDER_BLUE, (0, int(GROUND), int(WIDTH), int(HEIGHT - GROUND)))
    pygame.draw.rect(game_screen, FOREST_GREEN, (0, int(GROUND), int(WIDTH), int((WATER - GROUND) / 2)))
    score_window()
    for player in players:
        player.gun.draw()
        for screen_ball in player.balls:
            screen_ball.move()
            if screen_ball.live == 1:
                screen_ball.draw()
    for j in range(len(targets)):
        targets[j].move()
        if targets[j].live == 1:
            targets[j].draw()
        else:
            if isinstance(targets[j], Fish):
                if targets[j].live == 0 and targets[j].life_time > 0:
                    number_of_all_feathers = randint(3, 7)
                    for number_of_feather in range(number_of_all_feathers):
                        targets.append(Feather(number_of_feather, number_of_all_feathers, targets[j].x, targets[j].y))
                targets[j] = Bird()
            elif isinstance(targets[j], Bird):
                targets[j] = Fish()
    pygame.display.update()


class Player:
    def __init__(self, player_number, game_screen_left_border, game_screen_right_border):
        """
        Get new player

        :param player_number: 0(left) or 1(right)
        :param game_screen_left_border: left border of player's moving place
        :param game_screen_right_border: right border of player's moving place
        """
        self.number = player_number
        self.left_border = game_screen_left_border
        self.right_border = game_screen_right_border
        self.position_x = (self.left_border + self.right_border) / 2
        self.position_y = GROUND
        self.score = 0
        self.color = random_color()
        self.gun = Gun(self.number, game_screen, self.position_x, self.position_y, self.color, self.left_border,
                       self.right_border)
        self.balls = []

    def process_event(self, one_event):
        """
        Process event

        :param one_event: event to process
        :return: True if game is over else False
        """
        game_end = False
        if one_event.type == pygame.QUIT:
            game_end = True
        if self.number == 0:
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
        Check all balls hits with all targets and other player
        """
        for check_ball in self.balls:
            check_ball.move()
            if check_ball.live:
                players[1- self.number].score += players[1- self.number].gun.hit_test(check_ball)
                for number_of_target in range(len(targets)):
                    if targets[number_of_target].live:
                        self.score += targets[number_of_target].hit_test(check_ball)


class Ball:
    def __init__(self, screen, start_angle, power, x, y):
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
        :param start_angle: angle of hook moving
        :param power: factor of velocity
        :param x: gun end coordinate x
        :param y: gun end coordinate y
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = 10
        self.speed_x = speed_coefficient * power * math.cos(start_angle)
        self.speed_y = -speed_coefficient * power * math.sin(start_angle)
        self.color = BLACK
        self.live = 1

    def move(self):
        """
        Move hook and get new hook parameters after small time
        Count hook life time and check if it is over
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
        Draw hooks with given parameters
        """
        pygame.draw.rect(self.screen, BLACK,
                         (self.x - self.radius / 2, self.y - self.radius / 2, self.radius, self.radius))


class Gun:
    def __init__(self, number, screen, x, y, head_color, left_border, right_border):
        """
        Initialisation of gun

        :param number: player's number
        :param screen: screen of gun
        :param x: start gun coordinate x
        :param y: start gun coordinate y
        :param head_color: player's color
        :param left_border: left border to move
        :param right_border: right border to move
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
        self.live = 1
        # self.head = Head(self.length / 6, head_color, screen, self.x, self.y)

    def power_up(self):
        """
        Power up start speed of shot
        After start_gun_power*2 powering ends and gun shoots itself and get initial power of shooting
        Near maximum power it becomes red

        :return: new ball if gun shoots
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
        Ball shot with given parameters

        :return: new ball after shot
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
        Clockwise or counterclockwise, depends on direction

        :param direction: direction of rotation, left or right
        """
        if direction == 'right':
            self.angle = self.angle - self._rotation_speed
        else:
            self.angle = self.angle + self._rotation_speed

    def moving(self, direction):
        """
        Horizontal moving of player

        :param direction: direction of moving
        """
        if direction == 'right' and self.x < self.right_border:
            self.x = self.x + self._moving_speed
        elif direction == 'left' and self.x > self.left_border:
            self.x = self.x - self._moving_speed

    def draw(self):
        """
        Draw gun
        Its length and width shows power of possible shot
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
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.radius, width=1)

    def hit_test(self, test_object):
        """
        Test if object hits playes

        :param test_object: object to test
        :return: result win score
        """
        hit_radius = test_object.radius * 1.2
        if (self.radius + hit_radius) * (self.radius + hit_radius) > (test_object.x - self.x) * (
                test_object.x - self.x) + (test_object.y - self.y) * (test_object.y - self.y):
            self.live = 0
            return -400
        else:
            return 0


class Target:
    def __init__(self):
        """
        Initialisation
        """
        self.live = 1

    def move(self):
        """
        Moving after small time
        """
        pass

    def draw(self):
        """
        Draw target
        """
        pass

    def hit_test(self, object):
        """
        Test if object hits target

        :param object: object to test hitting with
        """
        pass


class Feather(Target):
    def __init__(self, number, all_number, x, y):
        """
        Make new feather after ded fish
        All feathers go in different sides around place of ded

        :param number: number of this feather
        :param all_number: all number of feathers from one ded fish
        :param x: place of ded
        :param y: place of ded
        """
        super().__init__()
        self.x = x + (randint(1, 5) + 10) * np.cos(number * np.pi * 2 / all_number)
        self.y = y + (randint(1, 5) + 10) * np.sin(number * np.pi * 2 / all_number)
        self.speed_y = randint(1, 15)
        self.radius = randint(5, int(max_target_radius / 3))
        self.color = YELLOW
        self.screen = game_screen
        self.life_time = 50

    def draw(self):
        """
        Draw feather with given parameters
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        """
        Calculate feather speed and coordinate after small time
        """
        self.life_time -= 1
        if self.life_time <= 0:
            self.live = 0
        self.y += self.speed_y
        self.speed_y -= water_g

    def hit_test(self, obj):
        """
        Test if object hits feather

        :param obj: object to test hitting
        :return: win score or 0
        """
        if (self.radius + obj.radius) * (self.radius + obj.radius) > (obj.x - self.x) * (obj.x - self.x) + (
                obj.y - self.y) * (obj.y - self.y):
            self.live = 0
            return 300
        else:
            return 0


class Bird(Target):
    def __init__(self):
        """
        Initialisation
        """
        super().__init__()
        self.speed_x = randint(1, 15) * choice([1, -1])
        self.speed_y = 0
        self.x = (0 - max_target_radius / 2) * int(bool(self.speed_x > 0)) + (WIDTH - max_target_radius) * int(
            bool(self.speed_x < 0))
        self.y = randint(int(max_target_radius + SKY), int((GROUND - max_target_radius) / 2))
        self.radius = randint(30, max_target_radius)
        self.color = GREY
        self.screen = game_screen
        self.life_time = 1
        self.live = 1

    def draw(self):
        """
        Draw target with given parameters
        """
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.radius + 1)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        if self.speed_x > 0:
            pygame.draw.polygon(self.screen, self.color, (
                (self.x - self.radius, self.y), (self.x - self.radius * 2, self.y + self.radius / 2),
                (self.x - self.radius * 2, self.y - self.radius / 2)))
            pygame.draw.polygon(self.screen, BLACK, (
                (self.x - self.radius, self.y), (self.x - self.radius * 2, self.y + self.radius / 2),
                (self.x - self.radius * 2, self.y - self.radius / 2)), width=1)
            wing_length = self.radius * randint(1, 100) / 50
            pygame.draw.polygon(self.screen, self.color, (
                (self.x - wing_length, self.y - self.radius), (self.x, self.y + self.radius),
                (self.x, self.y - self.radius)))
            pygame.draw.polygon(self.screen, BLACK, (
                (self.x - wing_length, self.y - self.radius), (self.x, self.y + self.radius),
                (self.x, self.y - self.radius)), width=1)
            pygame.draw.polygon(self.screen, YELLOW, (
                (self.x + self.radius * 1.2, self.y), (self.x + self.radius * 0.9, self.y + self.radius * 0.4),
                (self.x + self.radius * 0.9, self.y - self.radius * 0.4)))
            pygame.draw.polygon(self.screen, BLACK, (
                (self.x + self.radius * 1.2, self.y), (self.x + self.radius * 0.9, self.y + self.radius * 0.4),
                (self.x + self.radius * 0.9, self.y - self.radius * 0.4)), width=1)
        else:
            pygame.draw.polygon(self.screen, self.color, (
                (self.x + self.radius, self.y), (self.x + self.radius * 2, self.y + self.radius / 2),
                (self.x + self.radius * 2, self.y - self.radius / 2)))
            pygame.draw.polygon(self.screen, BLACK, (
                (self.x + self.radius, self.y), (self.x + self.radius * 2, self.y + self.radius / 2),
                (self.x + self.radius * 2, self.y - self.radius / 2)), width=1)
            wing_length = self.radius * randint(1, 100) / 50
            pygame.draw.polygon(self.screen, self.color, (
                (self.x + wing_length, self.y - self.radius), (self.x, self.y + self.radius),
                (self.x, self.y - self.radius)))
            pygame.draw.polygon(self.screen, BLACK, (
                (self.x + wing_length, self.y - self.radius), (self.x, self.y + self.radius),
                (self.x, self.y - self.radius)), width=1)
            pygame.draw.polygon(self.screen, YELLOW, (
                (self.x - self.radius * 1.2, self.y), (self.x - self.radius * 0.9, self.y + self.radius * 0.4),
                (self.x - self.radius * 0.9, self.y - self.radius * 0.4)))
            pygame.draw.polygon(self.screen, BLACK, (
                (self.x - self.radius * 1.2, self.y), (self.x - self.radius * 0.9, self.y + self.radius * 0.4),
                (self.x - self.radius * 0.9, self.y - self.radius * 0.4)), width=1)

    def move(self):
        """
        Calculate bird speed and coordinate after small time
        """
        self.x += self.speed_x
        if self.x + self.radius < 0:
            self.live = 0
        elif self.x - self.radius > WIDTH:
            self.live = 0

    def hit_test(self, obj):
        """
        Test hitting

        :param obj: object to test
        :return: win score or 0
        """
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
        self.color = random_color()
        # self.color = choice(GAME_COLORS)
        self.screen = game_screen
        self.life_time = randint(500, 1000)
        self.live = 1

    def draw(self):
        """
        Draw target with given parameters
        """
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.radius + 1)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        if self.speed_x > 0:
            pygame.draw.polygon(self.screen, self.color, (
                (self.x - self.radius, self.y), (self.x - self.radius * 2, self.y + self.radius),
                (self.x - self.radius * 2, self.y - self.radius)))
            pygame.draw.polygon(self.screen, BLACK, (
                (self.x - self.radius, self.y), (self.x - self.radius * 2, self.y + self.radius),
                (self.x - self.radius * 2, self.y - self.radius)), width=1)
        else:
            pygame.draw.polygon(self.screen, self.color, (
                (self.x + self.radius, self.y), (self.x + self.radius * 2, self.y + self.radius),
                (self.x + self.radius * 2, self.y - self.radius)))
            pygame.draw.polygon(self.screen, BLACK, (
                (self.x + self.radius, self.y), (self.x + self.radius * 2, self.y + self.radius),
                (self.x + self.radius * 2, self.y - self.radius)), width=1)

    def move(self):
        """
        Move target
        """
        self.life_time -= 1
        if self.life_time <= 0:
            self.live = 0
            self.life_time = 0
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
        """
        Test hitting
        :param obj: object to test
        :return: win score or 0
        """
        if (self.radius + obj.radius) * (self.radius + obj.radius) > (obj.x - self.x) * (obj.x - self.x) + (
                obj.y - self.y) * (obj.y - self.y):
            self.live = 0
            return 100 * (30 - self.radius)
        else:
            return 0


pygame.init()
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False

left_player = Player(0, 0, WIDTH / 2)
right_player = Player(1, WIDTH / 2, WIDTH)
players = [left_player, right_player]
targets = []
for i in range(8):
    targets.append(Fish())
    targets.append(Bird())

first_screen()
pygame.time.delay(10000)

while not finished:
    screen_update()
    clock.tick(FPS)
    for event in pygame.event.get():
        finished = players[0].process_event(event) or players[1].process_event(event)
pygame.quit()
