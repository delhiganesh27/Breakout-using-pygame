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

# brick class


class Brick():
    def __init__(self):  # alwys first define dimension and position in object
        self.width = int(WIDTH/COLS)
        self.height = 30

    def create_bricks(self):
        self.bricks = []
        for row in range(ROWS):
            bricks_row = []
            for col in range(COLS):
                brick_x = col*self.width
                brick_y = row*self.height
                br = pygame.Rect(brick_x, brick_y, self.width, self.height)
                bricks_row.append(br)
            self.bricks.append(bricks_row)

    def draw_bricks(self):
        for row in self.bricks:
            for br in row:
                pygame.draw.rect(win, GREEN, br)
                pygame.draw.rect(win, BLACK, br, 2)  # for outline

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
        if self.rect.right > WIDTH or self.rect.left < 10:  # for left and right only x sign will change
            self.dx *= -1
        if self.rect.top < 10:
            self.dy *= -1
        if self.rect.bottom > HEIGHT:
            self.game_st = -1
        # paddle collision
        # if the ball is in the paddle during next loop the direction will change continuously it feels like struck
        if self.rect.colliderect(paddle) and self.dy > 0:

            # when ball in downward movement dy is positive
            self.dy *= -1
            sound = pygame.mixer.Sound("bounce.wav")
            sound.play()
        # brick collision
        all_done = True
        row_num = 0
        for row in brick_wall.bricks:
            col_num = 0
            for br in row:
                if self.rect.colliderect(br):
                    hit_sound = pygame.mixer.Sound("hit.wav")
                    hit_sound.play()
                    # if abs(self.rect.bottom-br.top) < 5 and self.dy > 0:
                    #     self.dy *= -1
                    # if abs(self.rect.top-br.bottom) < 5 and self.dy < 0:
                    #     self.dy *= -1
                    # if abs(self.rect.left-br.right) < 5 and self.dx < 0:
                    #     self.dx *= -1
                    # if abs(self.rect.right-br.left) < 5 and self.dx > 0:
                    #     self.dx *= -1
                    brick_wall.bricks[row_num][col_num] = (0, 0, 0, 0)
                if brick_wall.bricks[row_num][col_num] != (0, 0, 0, 0):
                    all_done = False
                col_num += 1
            row_num += 1
        if all_done:
            self.game_st = 1
        self.rect.x += self.dx
        self.rect.y += self.dy

        return self.game_st


paddle = Paddle()
ball = Ball(paddle.x+int(paddle.width/2), paddle.y-10)
brick_wall = Brick()
brick_wall.create_bricks()
run = True
'''everything is declared as rectange for comfortable movement and simple code'''
while run:

    clock.tick(FPS)
    # every time it made everything black otherwise the previous draw trace will show
    win.fill(BLACK)
    paddle.draw_paddle()
    paddle.move_paddle()
    ball.draw_ball()
    brick_wall.draw_bricks()
    status = ball.move_ball()
    if status == -1:
        win.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Game Over", True, BLUE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        win.blit(text, text_rect)
    if status == 1:
        win.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render("You Win", True, BLUE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        win.blit(text, text_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
