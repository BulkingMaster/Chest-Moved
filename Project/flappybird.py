import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 32)

# Bird settings
bird_radius = 20
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipe settings
pipe_width = 60
pipe_gap = 150
pipe_velocity = 3
pipes = []

def create_pipe():
    height = random.randint(100, 400)
    top = height - pipe_gap
    bottom = height
    return {'x': WIDTH, 'top': top, 'bottom': bottom}

def draw_bird(y):
    pygame.draw.circle(screen, WHITE, (bird_x, int(y)), bird_radius)

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe['x'], 0, pipe_width, pipe['top']))
        pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['bottom'], pipe_width, HEIGHT))

def check_collision(pipes, y):
    for pipe in pipes:
        if pipe['x'] < bird_x + bird_radius < pipe['x'] + pipe_width:
            if y - bird_radius < pipe['top'] or y + bird_radius > pipe['bottom']:
                return True
    if y - bird_radius <= 0 or y + bird_radius >= HEIGHT:
        return True
    return False

def display_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# Game variables
score = 0
pipe_timer = 0
game_active = True

# Game loop
while True:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = jump_strength
        else:
            if event.type == pygame.KEYDOWN:
                # Reset game
                bird_y = HEIGHT // 2
                bird_velocity = 0
                pipes.clear()
                score = 0
                game_active = True

    if game_active:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe management
        pipe_timer += 1
        if pipe_timer >= 90:
            pipes.append(create_pipe())
            pipe_timer = 0

        for pipe in pipes:
            pipe['x'] -= pipe_velocity

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe['x'] + pipe_width > 0]

        # Scoring
        for pipe in pipes:
            if pipe['x'] + pipe_width == bird_x:
                score += 1

        # Collision detection
        if check_collision(pipes, bird_y):
            game_active = False

        # Drawing
        draw_bird(bird_y)
        draw_pipes(pipes)
        display_score(score)
    else:
        game_over_text = font.render("Game Over! Press any key", True, WHITE)
        screen.blit(game_over_text, (50, HEIGHT // 2 - 20))

    pygame.display.update()
    clock.tick(FPS)
