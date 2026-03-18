import pygame
import sys

pygame.init()

# --- Setup ---
WORLD_WIDTH, WORLD_HEIGHT = 7500, 800
WIDTH, HEIGHT = 800, 800
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("jumping")

X_POSITION, Y_POSITION = 400, 660

# Game variables
on_ground = True
jumping = False
Y_GRAVITY = 1
JUMP_HEIGHT = 18
Y_VELOCITY = 0
VELOCITY = 8
FACING_LEFT = False

# Camera settings
cam_x = 0
cam_y = 0

# Animation variables
anim_frame = 0
anim_timer = 0
ANIM_SPEED = 6

# --- Load assets (ONLY ONCE) ---
STANDING_SURFACE = pygame.transform.scale(
    pygame.image.load("mario_standing.png").convert_alpha(), (48, 64)
)

JUMPING_SURFACE = pygame.transform.scale(
    pygame.image.load("mario_jumping.png").convert_alpha(), (48, 64)
)

WALK_FRAMES = [
    pygame.transform.scale(pygame.image.load(f"walk{i}.gif").convert_alpha(), (48, 64))
    for i in range (1, 5)
]

BACKGROUND = pygame.transform.scale(
    pygame.image.load("background_long.png").convert(), (7500, 800)
)

BLOCK_IMAGE = pygame.transform.scale(
    pygame.image.load("brick_block.png").convert_alpha(),(48, 48)
)
def get(c):
    print("Test")
    print(c)

BLOCK_SIZE = 48

# Load block placements
blocks = []
with open("level.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line:

            x = map(get, (line.split()) )
            #blocks.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))

# --- Rect ---
mario_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))

GROUND_Y = 660

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    X_VELOCITY = 0
    MOVING = False

    # Jump when space is pressed
    if keys[pygame.K_SPACE] and not jumping:
        jumping = True
        Y_VELOCITY = JUMP_HEIGHT

    # Apply physics while jumping is true
    if jumping:
        Y_POSITION -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY

        if Y_POSITION >= GROUND_Y:
            Y_POSITION = GROUND_Y
            jumping = False
            Y_VELOCITY = 0

    # Move left
    if keys[pygame.K_a]:
        X_VELOCITY = -VELOCITY
        MOVING = True
        FACING_LEFT = True

    # Move right
    if keys[pygame.K_d]:
        X_VELOCITY = VELOCITY
        MOVING = True
        FACING_LEFT = False

    # Exit
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if MOVING and not jumping:
        anim_timer += 1
        if anim_timer >= ANIM_SPEED:
            anim_timer = 0
            anim_frame = (anim_frame + 1) % len(WALK_FRAMES)

    else:
        anim_frame = 0
        anim_timer = 0

    # Update position
    X_POSITION += X_VELOCITY
    mario_rect.center = (X_POSITION, Y_POSITION)

    for block in blocks:
        if mario.rect.colliderect(block):
            if X_VELOCITY > 0:
                mario_rect.right = block.left
            elif X_VELOCITY < 0:
                mario_rect.left = block.right
            X_POSITION = mario_rect.centerx

    mario_rect.centery = int(Y_POSITION)

    on_ground = False
    for block in blocks:
        if mario_rect.colliderect(block):
            if Y_VELOCITY < 0:
                mario_rect.top = block.bottom
                Y_POSITION = mario_rect.centery
                Y_VELOCITY = 0
            elif Y_VELOCITY >= 0:
                mario_rect.bottom = block.top
                on_ground = True
                jumping = False
                Y_VELOCITY = 0

    if Y_POSITION >= GROUND_Y:
        Y_POSITION = GROUND_Y
        mario_rect.centery = int(Y_POSITION)
        jumping = False
        Y_VELOCITY = 0
        on_ground = True


    # Update camera
    target_cam_x = X_POSITION - WIDTH // 2
    target_cam_y = Y_POSITION - HEIGHT // 2

    cam_x += (target_cam_x - cam_x) * 0.1
    cam_y += (target_cam_y - cam_y) * 0.1

    # Clamp camera to world bounds
    cam_x = max(0, min(cam_x, WORLD_WIDTH - WIDTH))
    cam_y = max(0, min(cam_y, WORLD_HEIGHT - HEIGHT))

    # Drawing
    SCREEN.blit(BACKGROUND, (-cam_x, -cam_y))

    draw_x = mario_rect.x - cam_x
    draw_y = mario_rect.y - cam_y

    if jumping:
        current_surface = JUMPING_SURFACE
    elif MOVING:
        current_surface = WALK_FRAMES[anim_frame]
    else:
        current_surface = STANDING_SURFACE

    if FACING_LEFT:
        current_surface = pygame.transform.flip(current_surface, True, False)

    SCREEN.blit(current_surface, (draw_x, draw_y))

    pygame.display.update()
    CLOCK.tick(60)