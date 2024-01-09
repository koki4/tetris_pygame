from random import randint
from math import sqrt
from copy import deepcopy
import sys
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_DOWN, K_LEFT, K_RIGHT, K_SPACE

BLOCK_DATA = (
    (
        (0, 0, 1, \
         1, 1, 1, \
         0, 0, 0),
        (0, 1, 0, \
         0, 1, 0, \
         0, 1, 1),
        (0, 0, 0, \
         1, 1, 1, \
         1, 0, 0),
        (1, 1, 0, \
         0, 1, 0, \
         0, 1, 0),
    ), (
        (2, 0, 0, \
         2, 2, 2, \
         0, 0, 0),
        (0, 2, 2, \
         0, 2, 0, \
         0, 2, 0),
        (0, 0, 0, \
         2, 2, 2, \
         0, 0, 2),
        (0, 2, 0, \
         0, 2, 0, \
         2, 2, 0)
    ), (
        (0, 3, 0, \
         3, 3, 3, \
         0, 0, 0),
        (0, 3, 0, \
         0, 3, 3, \
         0, 3, 0),
        (0, 0, 0, \
         3, 3, 3, \
         0, 3, 0),
        (0, 3, 0, \
         3, 3, 0, \
         0, 3, 0)
    ), (
        (4, 4, 0, \
         0, 4, 4, \
         0, 0, 0),
        (0, 0, 4, \
         0, 4, 4, \
         0, 4, 0),
        (0, 0, 0, \
         4, 4, 0, \
         0, 4, 4),
        (0, 4, 0, \
         4, 4, 0, \
         4, 0, 0)
    ), (
        (0, 5, 5, \
         5, 5, 0, \
         0, 0, 0),
        (0, 5, 0, \
         0, 5, 5, \
         0, 0, 5),
        (0, 0, 0, \
         0, 5, 5, \
         5, 5, 0),
        (5, 0, 0, \
         5, 5, 0, \
         0, 5, 0)
    ), (
        (6, 6, 6, 6),
        (6, 6, 6, 6),
        (6, 6, 6, 6),
        (6, 6, 6, 6)
    ), (
        (0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0),
        (0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0, \
         0, 0, 0, 0),
        (0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0),
        (0, 0, 0, 0, \
         0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0)
    )
)

COL_DATA = ((200, 0, 0), (0, 200, 0), (0, 0, 200),
   (200, 200, 0), (0, 200, 200), (200, 0, 200), (200, 200, 200))

class Block:
    def __init__(self):
        self.x = 2
        self.y = 2
        self.landed = False
        self.block_type = randint(0, 6)
        self.orientation = randint(0, 3)
        self.col = COL_DATA[self.block_type]
        self.whole_size = len(BLOCK_DATA[self.block_type][self.orientation])
        self.side_length = int(sqrt(self.whole_size))
    def prepare_draw(self):
        for index in range(self.whole_size):
            if BLOCK_DATA[self.block_type][self.orientation][index]:
                pygame.draw.rect(Surface, self.col,
                  Rect(350 + self.x * SIZE + index % self.side_length * SIZE,
                   50 + self.y * SIZE + index // self.side_length * SIZE, SIZE, SIZE))
    def draw(self):
        for index in range(self.whole_size):
            if BLOCK_DATA[self.block_type][self.orientation][index]:
                pygame.draw.rect(Surface, self.col,
                  Rect(25 + self.x * SIZE + index % self.side_length * SIZE,
                  -100 + 25 + self.y * SIZE + index // self.side_length * SIZE, SIZE, SIZE))
    def update(self, count):
        global game_over
        if self.landed:
            for index in range(self.whole_size):
                if BLOCK_DATA[self.block_type][self.orientation][index]:
                    FIELD[self.x + index % self.side_length][self.y + index // self.side_length] = 1
                    FIELD_COL[self.x + index % self.side_length][self.y + index // self.side_length] = self.col
            from_current_to_next()
            return
        next_x, next_y = self.x, self.y
        if count % 10 == 0:
            next_y += 1
        flag = True
        under_nothing = True
        """for index in range(self.whole_size * (self.side_length - 1) // self.side_length, self.whole_size * (self.side_length - 0) // self.side_length):
            if BLOCK_DATA[self.block_type][self.orientation][index]:
                under_nothing = False
                if FIELD[int(next_x + index % self.side_length)][int(next_y + index // self.side_length)]:
                    flag = False
        if under_nothing:
            print("second")
            for index in range(self.whole_size * (self.side_length - 2) // self.side_length, self.whole_size * (self.side_length - 1) // self.side_length):
                if BLOCK_DATA[self.block_type][self.orientation][index]:
                    under_nothing = False
                    if FIELD[int(next_x + index % self.side_length)][int(next_y + index // self.side_length)]:
                        flag = False
        if under_nothing:
            print("third")
            for index in range(self.whole_size * (self.side_length - 3) // self.side_length, self.whole_size * (self.side_length - 2) // self.side_length):
                if BLOCK_DATA[self.block_type][self.orientation][index]:
                    under_nothing = False
                    if FIELD[int(next_x + index % self.side_length)][int(next_y + index // self.side_length)]:
                        flag = False"""
        num_from_buttom = 0
        while under_nothing:
            for index in range(self.whole_size * (self.side_length - num_from_buttom - 1) // self.side_length, self.whole_size * (self.side_length - num_from_buttom) // self.side_length):
                if BLOCK_DATA[self.block_type][self.orientation][index]:
                    under_nothing = False
                    if FIELD[int(next_x + index % self.side_length)][int(next_y + index // self.side_length)]:
                        flag = False
            num_from_buttom += 1
        if flag:
            self.x, self.y = next_x, next_y
        else:
            self.landed = True
        if self.landed:
            for index in range(self.whole_size):
                if BLOCK_DATA[self.block_type][self.orientation][index]:
                    if -100 + 25 + self.y * SIZE + index // self.side_length * SIZE < 75 :
                        game_over = True

    def rotation(self):
        if self.landed:
            return
        next_orientation = (self.orientation + 1) % 4
        flag = True
        for index in range(self.whole_size):
            if BLOCK_DATA[self.block_type][next_orientation][index]:
                if FIELD[int(self.x + index % self.side_length)][int(self.y + index // self.side_length)]:
                    flag = False
        if flag:
            self.orientation = next_orientation
    def move(self, key):
        if self.landed:
            return
        next_x, next_y = self.x, self.y
        if key == K_DOWN:
            next_y += 1
        elif key == K_LEFT:
            next_x -= 1
        elif key == K_RIGHT:
            next_x += 1
        flag = True
        for index in range(self.whole_size):
            if BLOCK_DATA[self.block_type][self.orientation][index]:
                if FIELD[int(next_x + index % self.side_length)][int(next_y + index // self.side_length)]:
                    flag = False
        if flag:
            self.x = next_x
            self.y = next_y

def from_current_to_next():
    global current_block
    global next_block
    current_block = next_block
    next_block = Block()

def line_clear(row):
    for xpos in range(1, 10 + 1):
        for ypos in range(row, 0 - 1 + 1, -1):
            FIELD[xpos][ypos] = FIELD[xpos][ypos - 1]
            FIELD_COL[xpos][ypos] = FIELD_COL[xpos][ypos - 1]

def line_check():
    row = []
    for ypos in range(0, 24 + 1):
        line_exist = True
        for xpos in range(1, 10 + 1):
            if FIELD[xpos][ypos] == 0:
                line_exist = False
        if line_exist:
            row.append(ypos)
    for index in row:
        line_clear(index)

pygame.init()
Surface = pygame.display.set_mode((600, 600))
Fpslock = pygame.time.Clock()
pygame.key.set_repeat(30, 30)

SIZE = 25
WIDTH = 12
HEIGHT = 22
game_over = False
FIELD = [[0 for _ in range(HEIGHT+4)] for _ in range(WIDTH)]
FIELD_COL = [[(0, 0, 0) for _ in range(HEIGHT+4)] for _ in range(WIDTH)]

current_block = Block()
next_block = Block()

def main():
    count = 0
    sysfont = pygame.font.SysFont(None, 72)
    over_mess = sysfont.render("Game Over!!!", True, (255, 100, 100))
    mess_rect = over_mess.get_rect()
    mess_rect.center = (300, 300)
    #フィールド背景の画面
    for ypos in range(3, HEIGHT+4):
        FIELD[0][ypos] = 1
        FIELD_COL[0][ypos] = (100, 100, 100)
    for xpos in range(WIDTH):
        FIELD[xpos][HEIGHT - 1 + 4] = 1
        FIELD_COL[xpos][HEIGHT - 1 + 4] = (100, 100, 100)
    for ypos in range(3, HEIGHT+4):
        FIELD[WIDTH - 1][ypos] = 1
        FIELD_COL[WIDTH - 1][ypos] = (100, 100, 100)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    current_block.rotation()
                else:
                    current_block.move(event.key)
        
        #描画
        Surface.fill((0, 0, 0))
        current_block.draw()
        next_block.prepare_draw()

        #フィールドの描画
        for ypos in range(HEIGHT+4):
            for xpos in range(WIDTH):
                if FIELD[xpos][ypos]:
                    pygame.draw.rect(Surface, FIELD_COL[xpos][ypos],
                      Rect(25 + xpos * SIZE, -100 + 25 + ypos * SIZE, SIZE, SIZE))

        #マスの描画
        for ypos in range(0, 600, SIZE):
            pygame.draw.line(Surface, (0, 0, 0), (0, ypos), (600, ypos))
        for xpos in range(0, 600, SIZE):
            pygame.draw.line(Surface, (0, 0, 0), (xpos, 0), (xpos, 600))
        pygame.draw.line(Surface, (255, 0, 0), (50, 75), (300, 75))
        
        #文字の描画
        if game_over:
            Surface.blit(over_mess, mess_rect)

        if not game_over:
            #処理
            count += 1
            current_block.update(count)
            line_check()

        pygame.display.update()
        Fpslock.tick(15)

if __name__ == "__main__":
    main()