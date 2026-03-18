import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super meat boy copy")

clock = pygame.time.Clock()

background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

BODY_COLOR    = (0, 200, 255)
HAND_COLOR    = (100, 100, 255)
PLATFORM_COLOR = (120, 80, 40)
GROUND_COLOR  = (80, 50, 30)

# --- World settings ---
WORLD_WIDTH  = 4800
WORLD_HEIGHT = 2000
ground_y     = WORLD_HEIGHT - 80

# --- Platforms (x, y, width, height) in world coordinates ---
platforms = [
    pygame.Rect(300,  ground_y - 150, 200, 20),
    pygame.Rect(600,  ground_y - 280, 180, 20),
    pygame.Rect(900,  ground_y - 200, 220, 20),
    pygame.Rect(1200, ground_y - 350, 160, 20),
    pygame.Rect(1500, ground_y - 180, 200, 20),
    pygame.Rect(1800, ground_y - 300, 250, 20),
    pygame.Rect(2100, ground_y - 420, 180, 20),
    pygame.Rect(2400, ground_y - 250, 200, 20),
    pygame.Rect(2700, ground_y - 380, 170, 20),
    pygame.Rect(3000, ground_y - 200, 220, 20),
    pygame.Rect(3300, ground_y - 320, 190, 20),
    pygame.Rect(3600, ground_y - 150, 200, 20),
    pygame.Rect(3900, ground_y - 400, 160, 20),
    pygame.Rect(4200, ground_y - 260, 210, 20),
]

# --- Player settings ---
body_size    = 35
square_x     = 100.0
square_y     = float(ground_y - body_size)
facing_right = True

# Horizontal movement
speed        = 0.0
max_speed    = 12
acceleration = 0.9
friction     = 0.7

# Gravity & jumping
y_velocity      = 0.0
gravity         = 0.6
jump_strength   = -8
on_ground       = False
jump_held       = False
jump_hold_frames = 0
max_jump_frames = 12
hold_jump_force = 0.8

# Punch
punching    = False
hand_offset = 0
hand_speed  = 8
max_reach   = 35
hand_width  = 20
hand_height = 10

font = pygame.font.SysFont("monospace", 24)

# --- Camera ---
cam_x = 0.0
cam_y = 0.0

while True:
    # ---- EVENTS ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP) and on_ground:
                y_velocity       = jump_strength
                on_ground        = False
                jump_held        = True
                jump_hold_frames = 0
            if event.key == pygame.K_SPACE and not punching:
                punching = True

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_UP):
                jump_held = False

    # ---- JUMP HOLD ----
    if jump_held:
        if jump_hold_frames < max_jump_frames and not on_ground:
            y_velocity       -= hold_jump_force
            jump_hold_frames += 1
        else:
            jump_held = False

    # ---- HORIZONTAL MOVEMENT ----
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
    square_x  = max(0, min(WORLD_WIDTH - body_size, square_x))

    # ---- GRAVITY ----
    y_velocity += gravity
    square_y   += y_velocity
    on_ground   = False

    # ---- COLLISION: ground ----
    if square_y + body_size >= ground_y:
        square_y   = ground_y - body_size
        y_velocity = 0
        on_ground  = True

    # ---- COLLISION: platforms ----
    player_rect = pygame.Rect(square_x, square_y, body_size, body_size)
    for plat in platforms:
        if player_rect.colliderect(plat):
            # Only land on top (falling down onto it)
            if y_velocity >= 0 and player_rect.bottom - y_velocity <= plat.top + 5:
                square_y   = plat.top - body_size
                y_velocity = 0
                on_ground  = True

    # ---- PUNCH ANIMATION ----
    if punching:
        hand_offset += hand_speed
        if hand_offset >= max_reach:
            hand_speed = -hand_speed
        if hand_offset <= 0:
            hand_offset = 0
            hand_speed  = abs(hand_speed)
            punching    = False

    # ---- CAMERA (smoothly follows player) ----
    target_cam_x = square_x - WIDTH  // 2
    target_cam_y = square_y - HEIGHT // 2
    cam_x += (target_cam_x - cam_x) * 0.1
    cam_y += (target_cam_y - cam_y) * 0.1

    # Clamp camera to world bounds
    cam_x = max(0, min(WORLD_WIDTH  - WIDTH,  cam_x))
    cam_y = max(0, min(WORLD_HEIGHT - HEIGHT, cam_y))

    # ---- DRAW ----
    screen.blit(background, (0, 0))

    # Ground (draw relative to camera)
    pygame.draw.rect(screen, GROUND_COLOR,
        (0 - cam_x, ground_y - cam_y, WORLD_WIDTH, WORLD_HEIGHT))

    # Platforms
    for plat in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR,
            (plat.x - cam_x, plat.y - cam_y, plat.width, plat.height))

    # Player body
    draw_x = square_x - cam_x
    draw_y = square_y - cam_y
    pygame.draw.rect(screen, BODY_COLOR, (draw_x, draw_y, body_size, body_size))

    # Punch hand
    if facing_right:
        hand_x = draw_x + body_size + hand_offset
    else:
        hand_x = draw_x - hand_width - hand_offset
    hand_y = draw_y + body_size // 2 - hand_height // 2
    pygame.draw.rect(screen, HAND_COLOR, (hand_x, hand_y, hand_width, hand_height))

    # HUD
    speed_text = font.render(f"Speed: {speed:.2f}", True, (255, 255, 255))
    pos_text   = font.render(f"Pos: ({int(square_x)}, {int(square_y)})", True, (255, 255, 255))
    screen.blit(speed_text, (10, 10))
    screen.blit(pos_text,   (10, 40))

    pygame.display.flip()
    clock.tick(60)