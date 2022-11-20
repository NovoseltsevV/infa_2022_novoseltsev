from random import choice
from random import randint
import pygame
import math
pygame.init()
pygame.font.init()
f = pygame.font.Font(None, 24)
FPS = 30
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
BLACK = (0, 0, 0)
PURPLE = (156, 0, 195)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
WIDTH = 1100
HEIGHT = 800
bullet = 0
bullets = []
v = 10
v_special = 30
"""скорости объектов"""

class Bullet:
    def __init__(self, screen: pygame.Surface, x=90, y=750):
        """Конструктор класса bullet
        x - начальное положение снаряда по горизонтали
        y - начальное положение снаряда по вертикали
        r - радиус мяча
        color - цвет мяча
        vx - начальная скорость снаряда по горизонтали
        vy - начальная скорость снаряда по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(COLORS)

    def move(self):
        """Перемещение снаряда за единицу времени."""
        self.vy -= 1
        self.x += self.vx * dt
        self.y -= self.vy * dt

        if self.y + self.r >= HEIGHT:
            self.vx = self.vx / 1.2
            self.vy = -self.vy / 1.5
        if self.y - self.r <= 0:
            self.vy = -self.vy
        if self.x - self.r <= 0 or self.x + self.r >= WIDTH:
            self.vx = -self.vx

    def draw(self):
        """рисует снаряд"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


    def hit(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью,
        описываемой в обьекте obj.
        Аргументы:
            obj: Обьект, с которым проверяется столкновение.
        Возвращает True в случае столкновения мяча и цели.
        В противном случае возвращает False.
        """
        x = self.x - obj.x
        y = self.y - obj.y
        if (x ** 2 + y ** 2) ** 0.5 <= self.r + obj.r:
            return True
        return False


class Gun:
    def __init__(self, screen):
        """Конструктор класса gun
        Args:
        x - начальное положение снаряда по горизонтали
        y - начальное положение снаряда по вертикали
        f_power - сила выстрела
        """
        self.x = 70
        self.y = 750
        self.screen = screen
        self.f_power = 10
        self.f_on = False
        self.an = 0
        self.color = BLACK

    def fire_start(self):
        self.f_on = True

    def fire_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy
        зависят от положения мыши.
        """
        global bullets, bullet
        bullet += 1
        new_ball = Bullet(self.screen)
        new_ball.r += 5
        pos_x = event.pos[0] - new_ball.x
        pos_y = event.pos[1] - new_ball.y
        self.an = math.atan2(pos_y, pos_x)
        new_ball.vx = self.f_power * math.cos(self.an)
        new_ball.vy = - self.f_power * math.sin(self.an)
        bullets.append(new_ball)
        self.f_on = 0
        self.f_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1] - 750) / (event.pos[0] - 70))
        if self.f_on:
            self.color = PURPLE
        else:
            self.color = BLACK

    def draw(self):
        """Рисует пушку"""
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y),
            (self.x + max(self.f_power, 20) * math.cos(self.an),
             self.y + max(self.f_power, 20) * math.sin(self.an)),
            8
        )

    def power_up(self):
        """Увеличивает силу выстрела, до крит значения"""
        if self.f_on:
            if self.f_power < 100:
                self.f_power += 1
            self.color = PURPLE
        else:
            self.color = BLACK


class Target:
    def __init__(self, screen):
        """Конструктор класса target
        Args:
        live - количество жизней у цели
        """
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """Инициализация новой цели"""
        self.r = randint(2, 50)
        self.x = randint(0, WIDTH - self.r)
        self.y = randint(0, HEIGHT - self.r)
        self.vx = randint(-v, v)
        self.vy = randint(-v, v)
        self.live = 1
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель"""
        self.points += points

    def draw(self):
        """Рисует цель"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        """Метод описывает перемещение цели за один кадр перерисовки."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.y + self.r >= HEIGHT:
            self.vx = self.vx
            self.vy = -self.vy
        if self.y - self.r <= 0:
            self.vy = -self.vy
        if self.x - self.r <= 0 or self.x + self.r >= WIDTH:
            self.vx = -self.vx


class SpecialTarget(Target):
    def move(self):
        """Метод описывает перемещение специальной цели за один кадр перерисовки."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx = randint(-v_special, v_special)
        self.vy = randint(-v_special, v_special)
        if self.y + self.r * 2 >= HEIGHT:
            self.new_target()
        if self.y - self.r <= 0:
            self.new_target()
        if self.x - self.r <= 0 or self.x + self.r >= WIDTH:
            self.new_target()

    def draw(self):
        """Рисует специальный шарик"""
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, YELLOW, (self.x, self.y), self.r/2)

    def hit(self, points=5):
        """Попадание шарика в цель"""
        self.points += points


screen = pygame.display.set_mode((WIDTH, HEIGHT))
target = Target(screen)
clock = pygame.time.Clock()
gun = Gun(screen)
special_target = SpecialTarget(screen)
finished = False
elements = [target, special_target]


while not finished:
    dt = clock.tick(FPS) / FPS
    screen.fill(WHITE)
    for elem in elements:
        elem.draw()
        elem.move()
    gun.draw()
    for b in bullets:
        b.draw()
    text1 = str(target.points + special_target.points) + ' ' + str(bullet)
    text = f.render(text1, True, BLACK)
    screen.blit(text, (10, 10))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in bullets:
        b.move()
        for elem in elements:
            if b.hit(elem) and elem.live:
                elem.hit()
                elem.new_target()
    gun.power_up()

pygame.quit()