import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super cube game")
clock = pygame.time.Clock()

# Colors
WHITE     = (240, 240, 240)
BLUE      = (0, 150, 255)
GREEN     = (0, 255, 100)
DARK      = (30, 30, 30)
BOX_COLOR = (255, 80, 80)

# Player — one Rect does everything: movement, drawing, and collision
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 90, 40, 40)
speed  = 7

# Gravity / jumping
y_velocity    = 0
gravity       = 0.6
jump_strength = -12
on_ground     = False

# Ground
ground_y = HEIGHT - 50

# Target box
box  = pygame.Rect(350, 700, 40, 40)
font = pygame.font.SysFont(None, 32)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                y_velocity = jump_strength
                on_ground  = False

    # Left / right movement — update player.x directly
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: player.x -= speed
    if keys[pygame.K_d]: player.x += speed

    # Keep player inside the screen
    player.x = max(0, min(WIDTH - player.width, player.x))

    # Apply gravity — update player.y directly
    y_velocity += gravity
    player.y   += int(y_velocity)

    # Land on the ground
    if player.bottom >= ground_y:
        player.bottom = ground_y
        y_velocity    = 0
        on_ground     = True

    # Collision check — works now because player actually moves
    colliding = player.colliderect(box)

    # Draw
    screen.fill(DARK)
    pygame.draw.rect(screen, WHITE, (0, ground_y, WIDTH, HEIGHT - ground_y))
    pygame.draw.rect(screen, BOX_COLOR, box)
    pygame.draw.rect(screen, GREEN if colliding else BLUE, player)  # player changes color on hit

    label = font.render("Touching!" if colliding else "Move to the red box", True, WHITE)
    screen.blit(label, (20, 20))

    pygame.display.flip()
    clock.tick(60)