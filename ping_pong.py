import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
paddle_speed = 5

BALL_SIZE = 20
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))

paddle1 = pygame.Rect(10, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(WIDTH - 20, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)

running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # get keys for paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= paddle_speed
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += paddle_speed

    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
        paddle2.y += paddle_speed

    # ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # collision with paddle
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x *= -1

    # scoring
    if ball.left <= 0:
        score2 += 1
        ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))

    if ball.right >= WIDTH:
        score1 += 1
        ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))

    # drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2,0), (WIDTH // 2, HEIGHT))

    # display scores
    text1 = font.render(f"{score1}", True, WHITE)
    screen.blit(text1,(WIDTH // 2 - 100, 10))
    text2 = font.render(f"{score2}", True, WHITE)
    screen.blit(text2, (WIDTH // 2 + 60, 10))

    # refresh screen
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# quit pygame
pygame.quit()
sys.exit()


