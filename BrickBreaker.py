import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Paddle settings
paddle_width, paddle_height = 100, 10
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 30, paddle_width, paddle_height)
paddle_speed = 7

# Ball settings
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 10, 10)
ball_speed_x, ball_speed_y = 4, -4
nitrous = False  # Speed boost flag

# Brick settings
brick_rows, brick_cols = 6, 12
brick_width, brick_height = 50, 20
brick_padding = 5
brick_offset_top = 50
brick_offset_left = (WIDTH - (brick_cols * (brick_width + brick_padding))) // 2
colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

# Create bricks
bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = brick_offset_left + col * (brick_width + brick_padding)
        brick_y = brick_offset_top + row * (brick_height + brick_padding)
        bricks.append((pygame.Rect(brick_x, brick_y, brick_width, brick_height), colors[row]))

# Fireworks function
def draw_fireworks():
    for _ in range(30):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT // 2)
        pygame.draw.circle(screen, random.choice(colors), (x, y), random.randint(2, 6))

# Game loop
running = True
win = False
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed
    
    # Speed boost (Nitrous)
    if keys[pygame.K_SPACE]:
        nitrous = True
    else:
        nitrous = False
    
    # Ball movement
    speed_multiplier = 1.5 if nitrous else 1
    ball.x += int(ball_speed_x * speed_multiplier)
    ball.y += int(ball_speed_y * speed_multiplier)
    
    # Ball collisions
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y
    if ball.colliderect(paddle):
        ball_speed_y = -ball_speed_y
    
    # Check for brick collisions
    for brick in bricks[:]:
        if ball.colliderect(brick[0]):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y
            pygame.draw.rect(screen, CYAN, brick[0])  # Smash effect
            break
    
    # Check for game over
    if ball.bottom >= HEIGHT:
        running = False
    
    # Check for win
    if not bricks:
        win = True
        running = False
    
    # Draw elements
    pygame.draw.rect(screen, BLACK, paddle)
    pygame.draw.ellipse(screen, CYAN if nitrous else BLACK, ball)  # Nitrous effect
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)
    
    pygame.display.flip()
    pygame.time.delay(16)

# End screen
screen.fill(BLACK)
if win:
    font = pygame.font.Font(None, 74)
    text = font.render("YOU WIN!", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    for _ in range(50):
        draw_fireworks()
else:
    font = pygame.font.Font(None, 74)
    text = font.render("YOU LOSE!", True, RED)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

pygame.display.flip()
pygame.time.delay(3000)
pygame.quit()