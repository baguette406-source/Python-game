import pygame
import sys
import math
import time

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Samurai Game")

# Clock
clock = pygame.time.Clock()
background = pygame.image.load("backdropSamurai.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Colors
BODY_COLOR = (0, 200, 255)
SWORD_COLOR = (200, 200, 200)

# Square/Body settings
body_size = 50
square_x = WIDTH // 5
square_y = HEIGHT // 1.22
speed = 7

# Sword variables
swinging = False
sword_angle = -65  # Start up (-65 degrees)
swing_speed = 20
sword_length = 60
sword_width = 8



# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and not swinging:
                swinging = True
                sword_angle = -95
                time.sleep(0.2)
                sword_angle = -75  # Reset sword up

    # Key presses for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        square_x -= speed
    if keys[pygame.K_d]:
        square_x += speed

    # Swing animation (rotate the sword)
    if swinging:

        sword_angle += swing_speed  # Rotate down
        if sword_angle >= 55:  # Reached bottom (45 degrees down)
            swing_speed = -swing_speed  # Reverse direction
        if sword_angle <= -75:  # Back to top
            sword_angle = -75

            swing_speed = abs(swing_speed)  # Reset to positive
            swinging = False

    # Keep square on screen
    square_x = max(0, min(WIDTH - body_size, square_x))
    square_y = max(0, min(HEIGHT - body_size, square_y))

    # Drawing
    screen.blit(background, (0, 0))

    # Draw body
    pygame.draw.rect(
        screen,
        BODY_COLOR,
        (square_x, square_y, body_size, body_size)
    )

    # Draw sword (rotating)
    # Pivot point is on the right side of the body
    pivot_x = square_x + body_size
    pivot_y = square_y + body_size // 2

    # Calculate where the sword tip is based on angle
    angle_radians = math.radians(sword_angle)
    sword_tip_x = pivot_x + sword_length * math.cos(angle_radians)
    sword_tip_y = pivot_y + sword_length * math.sin(angle_radians)

    # Draw the sword as a line from pivot to tip
    pygame.draw.line(
        screen,
        SWORD_COLOR,
        (pivot_x, pivot_y),
        (sword_tip_x, sword_tip_y),
        sword_width
    )

    pygame.display.flip()
    clock.tick(60)