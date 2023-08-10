import pygame
pygame.init()  # to initialize

WIDTH = 700
HEIGHT = 700
FPS = 60

COLS = 10  # for paddles
ROWS = 6

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (80, 175, 90)
BLUE = (60, 160, 200)

win = pygame.display.set_mode((WIDTH, HEIGHT))  # give wid,hei as tuple
pygame.display.set_caption("Breakout Game")
clock = pygame.time.Clock()

# Paddle class


class Paddle():
    def __init__(self):  # alwys first define dimension and position in object
        self.width = int(WIDTH/COLS)
        self.height = 20
        self.x = int(WIDTH/2)-int(self.width/2)
        self.y = HEIGHT-40
        self.speed = 10
        # to define an object as rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_paddle(self):
        pygame.draw.rect(win, WHITE, self.rect)

    def move_paddle(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if key[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# ball class


class Ball():
    def __init__(self, x, y):
        self.radius = 10
        self.x = x
        self.y = y
        # width of sq=radius*2
        self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)
        self.dx = 3
        self.dy = -3  # in pygame y cor is increaing in downward so we decrease
        self.game_st = 0

    def draw_ball(self):
        pygame.draw.circle(win, BLUE, (self.rect.x, self.rect.y), self.radius)

    def move_ball(self):
        # wall collision
        if self.rect.right > WIDTH or self.rect.left < 0:  # for left and right only x sign will change
            self.dx *= -1
        if self.rect.top < 0:
            self.dy *= -1
        if self.rect.bottom > HEIGHT:
            self.game_st = -1
        # paddle collision
        # if the ball is in the paddle during next loop the direction will change continuously it feels like struck
        if self.rect.colliderect(paddle) and self.dy > 0:
            # when ball in downward movement dy is positive
            self.dy *= -1
        self.rect.x += self.dx
        self.rect.y += self.dy

        return self.game_st


paddle = Paddle()
ball = Ball(paddle.x+int(paddle.width/2), paddle.y-10)
run = True
'''everything is declared as rectange for comfortable movement and simple code'''
while run:

    clock.tick(FPS)
    # every time it made everything black otherwise the previous draw trace will show
    win.fill(BLACK)
    paddle.draw_paddle()
    paddle.move_paddle()
    ball.draw_ball()
    status = ball.move_ball()
    if status == -1:
        win.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Game Over", True, BLUE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        win.blit(text, text_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
