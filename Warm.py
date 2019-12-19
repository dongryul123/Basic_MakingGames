import pygame
import sys
import time
import random

from pygame.locals import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WHITE = (255, 255, 255) # 가장 밝은 RGB값인 흰색
GREEN = (0, 50, 0)
ORANGE = (250, 150, 0)
GRAY = (100, 100, 100)

GRID_SIZE = 20 # 한 칸을 20으로.
GRID_WIDTH = WINDOW_WIDTH / GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT / GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

FPS = 10 # Frame Per Second

class Python(object):
    def __init__(self):
        self.create()
        self.color = GREEN

    def create(self):
        self.length = 2
        self.positions = [((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def control(self, xy): # 방향키 입력값 xy가 주어졌을 때
        if (xy[0] * -1, xy[1] * -1) == self.direction: #현재 방향의 반대일 경우 그냥 return (현 방향 유지))
            return
        else:
            self.direction = xy

    def move(self):
        cur = self.positions[0] # 뱀의 머리 부분
        x, y = self.direction
        new = ((cur[0] + (x * GRID_SIZE)) % WINDOW_WIDTH, (cur[1] + (y * GRID_SIZE)) % WINDOW_HEIGHT ) ### _ 새 좌표 입력?
        if new in self.positions[2:]:
            self.create() # 뱀이 자기 자신의 부분을 먹음. 다시 새로 시작
        else:
            self.positions.insert(0, new) # 0번째에 new 좌표 추가. 머리의 움직인 부분 추가
            if len(self.positions) > self.length:
                self.positions.pop() # 끝에 좌표 삭제. 꼬리 부분 삭제

    def eat(self):
        self.length += 1 # length 1 추가

    def draw(self, surface):
        for p in self.positions:
            draw_object(surface, self.color, p)

class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = BLUE
        self.create()

    def create(self):
        self.position = (random.randint(0, GRID_WIDTH - 1)* GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        draw_object(surface, self.color, self.position)

def draw_object(surface, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, color, r)

def check_eat(python, feed):
    if python.positions[0] == feed.position:
        python.eat()
        feed.create()

def show_info(length, speed, surface):
    font = pygame.font.Font(None, 34)
    text = font.render("Length: " + str(length) + "    Speed: " + str(round(speed, 2)), 1, GRAY)
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text, pos)

python = Python()
feed = Feed()

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Python Game')
surface = pygame.Surface(window.get_size())
surface = surface.convert()
surface.fill(WHITE)
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 40) #When the keyboard repeat is enabled,
                            #keys that are held down will generate multiple pygame.KEYDOWN events. The delay parameter is the number of milliseconds before the first repeated pygame.KEYDOWN event will be sent.
window.blit(surface, (0, 0)) # 비트연산을 통한 화면 구성

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                python.control(UP)
            elif event.key == K_DOWN:
                python.control(DOWN)
            elif event.key == K_LEFT:
                python.control(LEFT)
            elif event.key == K_RIGHT:
                python.control(RIGHT)

    surface.fill(WHITE)
    python.move()
    check_eat(python, feed)
    speed = (FPS + python.length) / 2
    show_info(python.length, speed, surface)
    python.draw(surface)
    feed.draw(surface)
    window.blit(surface, (0,0))
    pygame.display.flip()
    pygame.display.update()
    clock.tick(speed)
