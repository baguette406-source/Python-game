import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super meat boy copy")

clock = pygame.time.Clock()

background = pygame.image.load("backdropSamurai.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

BODY_COLOR = (0, 200, 255)
HAND_COLOR = (100, 100, 255)

# Player settings
body_size = 35
ground_y = HEIGHT - 80
facing_right = False
square_x = WIDTH // 5
square_y = ground_y - body_size

# Horizontal movement
speed = 0
max_speed = 12
acceleration = 0.9
friction = 0.6

# Gravity & jumping
y_velocity = 0
gravity = 0.6
jump_strength = -8
on_ground = False
jump_held = False
jump_hold_frames = 0
max_jump_frames = 12
hold_jump_force = 0.8

# Punch variables
punching = False
hand_offset = 0
hand_speed = 8
max_reach = 35
hand_width = 20
hand_height = 10

font = pygame.font.SysFont("monospace", 24)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP) and on_ground:
                y_velocity = jump_strength
                on_ground = False
                jump_held = True
                jump_hold_frames = 0
            if event.key == pygame.K_SPACE and not punching:
                punching = True

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_UP):
                jump_held = False

    # Variable jump height — outside event loop
    if jump_held:
        if jump_hold_frames < max_jump_frames and not on_ground:
            y_velocity -= hold_jump_force
            jump_hold_frames += 1
        else:
            jump_held = False

    # Horizontal movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        speed -= acceleration
        facing_right = False
        if speed < -max_speed:
            speed = -max_speed
    elif keys[pygame.K_d]:
        speed += acceleration
        facing_right = True
        if speed > max_speed:
            speed = max_speed
    else:
        speed *= friction
        if abs(speed) < 0.1:
            speed = 0

    square_x += speed

    y_velocity += gravity
    square_y += y_velocity

    if square_y + body_size >= ground_y:
        square_y = ground_y - body_size
        y_velocity = 0
        on_ground = True

    if punching:
        hand_offset += hand_speed
        if hand_offset >= max_reach:
            hand_speed = -hand_speed
        if hand_offset <= 0:
            hand_offset = 0
            hand_speed = abs(hand_speed)
            punching = False

    square_x = max(0, min(WIDTH - body_size, square_x))

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (80, 50, 30), (0, ground_y, WIDTH, HEIGHT - ground_y))
    pygame.draw.rect(screen, BODY_COLOR, (square_x, square_y, body_size, body_size))

    if facing_right:
        hand_x = square_x + body_size + hand_offset
    else:
        hand_x = square_x - hand_width - hand_offset
    hand_y = square_y + body_size // 2 - hand_height // 2
    pygame.draw.rect(screen, HAND_COLOR, (hand_x, hand_y, hand_width, hand_height))

    speed_text = font.render(f"Speed: {speed:.2f}", True, (255, 255, 255))
    screen.blit(speed_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)