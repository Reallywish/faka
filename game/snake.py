import pygame
import random

# 游戏界面的尺寸
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# 贪吃蛇方格的大小
GRID_SIZE = 20

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 初始化 Pygame
pygame.init()

# 设置游戏界面尺寸和标题
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")


# 定义贪吃蛇类
class Snake:
    def __init__(self):
        self.body = [(4, 3), (3, 3), (2, 3)]
        self.direction = "right"

    def move(self):
        if self.direction == "up":
            new_head = (self.body[0][0], self.body[0][1] - 1)
        elif self.direction == "down":
            new_head = (self.body[0][0], self.body[0][1] + 1)
        elif self.direction == "left":
            new_head = (self.body[0][0] - 1, self.body[0][1])
        else:
            new_head = (self.body[0][0] + 1, self.body[0][1])

        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def change_direction(self, direction):
        if direction == "up" and self.direction != "down":
            self.direction = "up"
        elif direction == "down" and self.direction != "up":
            self.direction = "down"
        elif direction == "left" and self.direction != "right":
            self.direction = "left"
        elif direction == "right" and self.direction != "left":
            self.direction = "right"

    def get_head(self):
        return self.body[0]

    def get_body(self):
        return self.body


# 定义食物类
class Food:
    def __init__(self):
        self.position = (0, 0)

    def generate(self):
        x = random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1)
        y = random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)
        self.position = (x, y)

    def get_position(self):
        return self.position


# 初始化贪吃蛇和食物
snake = Snake()
food = Food()
food.generate()

# 游戏主循环
clock = pygame.time.Clock()
while True:
    clock.tick(10)

    # 处理游戏事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("up")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("down")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("left")

