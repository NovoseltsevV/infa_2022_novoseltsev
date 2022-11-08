import pygame
from pygame.draw import *
from random import randint
pygame.init()
f1 = pygame.font.Font(None, 36)
FPS = 30
screen = pygame.display.set_mode((1100, 800))
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
Scores = 0
Balls = []
"""Массив, в котором хранятся данные о всех шариках"""
Number = 3
Width = 1100
Height = 800


def special():
    """Вероятность создания специальной цели"""
    return randint(0, 100) <= 10


def new_ball():
    """рисует новый шарик и определяет его начальные характеристики """
    x = randint(100, 1000)
    y = randint(100, 700)
    r = randint(10, 100)
    vx = randint(-15, 15)
    vy = randint(-15, 15)
    color = COLORS[randint(0, 5)]
    ball = [x, y, r, vx, vy, color, special()]
    """Массив чисел, который характеризует каждый шарик"""
    if ball[6]:
        circle(screen, (230, 218, 57), (ball[0], ball[1]), 30)
        circle(screen, (219, 20, 20), (ball[0] + 14, ball[1] - 14), 8)
        circle(screen, (219, 20, 20), (ball[0] - 14, ball[1] - 14), 8)
        circle(screen, (0, 0, 0), (ball[0] + 14, ball[1] - 14), 4)
        circle(screen, (0, 0, 0), (ball[0] - 14, ball[1] - 14), 4)
        rect(screen, (0, 0, 0), (ball[0] - 9, ball[1] + 9, 18, 6))
    else:
        circle(screen, ball[5], (ball[0], ball[1]), ball[2])
    Balls.append(ball)


def click(event):
    """определяет попадание мыши в шарик"""
    if event.button == 1:
        return (event.pos[0]-ball[0])**2 + (event.pos[1]-ball[1])**2 <= ball[2]**2


def update_position():
    """Функция определяет премещение шариков каждого типа за один кадр и отражение от стен"""
    screen.fill(BLACK)
    for ball in Balls:
        if ball[6]:
            ball[0] += ball[3]
            ball[1] += ball[4]
            if ball[0] >= Width - 30 or ball[0] <= 30:
                ball[3] = -ball[3]
            elif ball[1] >= Height - 30 or ball[1] <= 30:
                ball[4] = -ball[4]
            circle(screen, (230, 218, 57), (ball[0], ball[1]), 30)
            circle(screen, (219, 20, 20), (ball[0] + 14, ball[1] - 14), 8)
            circle(screen, (219, 20, 20), (ball[0] - 14, ball[1] - 14), 8)
            circle(screen, (0, 0, 0), (ball[0] + 14, ball[1] - 14), 4)
            circle(screen, (0, 0, 0), (ball[0] - 14, ball[1] - 14), 4)
            rect(screen, (0, 0, 0), (ball[0] - 9, ball[1] + 9, 18, 6))
        else:
            ball[0] += ball[3]
            ball[1] += ball[4]
            if ball[0] >= Width - ball[2] or ball[0] <= ball[2]:
                ball[3] = -ball[3]
            elif ball[1] >= Height - ball[2] or ball[1] <= ball[2]:
                ball[4] = -ball[4]
            circle(screen, ball[5], (ball[0], ball[1]), ball[2])


def score():
    """Функция определяет число набранных очков для каждого типа целей"""
    global Scores
    if ball[6]:
        Scores += 5*round(((ball[3])**2 + (ball[4])**2)/30)
    else:
        Scores += round(((ball[3]) ** 2 + (ball[4]) ** 2)/ball[2])


for i in range(Number):
    """Создание нужного числа шариков в начальный момент"""
    new_ball()


clock = pygame.time.Clock()
pygame.display.update()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in Balls:
                if click(event):
                    score()
                    new_ball()
                    Balls.remove(ball)
    update_position()
    text = f1.render(str(Scores), 1, (255, 255, 255))
    screen.blit(text, (10, 10))
    """текст со счётом игрока и его вывод на экран"""
    pygame.display.update()
pygame.quit()