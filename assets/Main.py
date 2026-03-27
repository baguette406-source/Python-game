import pygame
import sys

pygame.init()

# --- Window & World Setup ---
WORLD_WIDTH, WORLD_HEIGHT = 7500, 800   # how big the whole level is
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800 # how big the window is

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Game")
clock = pygame.time.Clock()

# --- Physics & Movement ---
gravity = 1
jump_force = 20
player_speed = 8

vertical_velocity = 0   # how fast the player is moving up/down (can be negative = falling)
is_on_ground = True
is_facing_left = False

# --- Camera ---
camera_x = 0   # how far the camera has scrolled to the right

# --- Animation ---
current_frame = 0       # which walk frame we're on (0-3)
frame_timer = 0         # counts up, then resets to advance the frame
frames_per_step = 3     # how many game ticks before switching to the next walk frame

# --- Tile / Level Settings ---
tile_size = 48
ground_y = 660          # y position of the ground floor


# --- Helper: load and scale an image ---
def load_image(path, width, height):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (width, height))


# --- Load Player Sprites ---
sprite_width, sprite_height = 48, 64

sprite_stand  = load_image("mario_standing.png", sprite_width, sprite_height)
sprite_jump   = load_image("mario_jumping.png",  sprite_width, sprite_height)
walk_frames   = [load_image(f"walk{i}.gif", sprite_width, sprite_height) for i in range(1, 5)]

# Flipped (left-facing) versions of every sprite
sprite_stand_left = pygame.transform.flip(sprite_stand, True, False)
sprite_jump_left  = pygame.transform.flip(sprite_jump,  True, False)
walk_frames_left  = [pygame.transform.flip(frame, True, False) for frame in walk_frames]

# --- Load Background ---
background = pygame.transform.scale(
    pygame.image.load("background_long.png").convert(),
    (WORLD_WIDTH, WORLD_HEIGHT)
)

# --- Load Block Sprite ---
block_image = load_image("brick_block.png", tile_size, tile_size)

# --- Load Level from File ---
# level.txt has one block per line: "x y"
# Lines starting with # are comments and are ignored
blocks = []
with open("level.txt", "r", encoding="utf-8-sig") as level_file:
    for line in level_file:
        line = line.strip()
        if line and not line.startswith("#"):
            parts = line.split()
            if len(parts) == 2:
                block_x = int(parts[0])
                block_y = int(parts[1])
                blocks.append(pygame.Rect(block_x, block_y, tile_size, tile_size))

# --- Create Player Rectangle ---
player = sprite_stand.get_rect(midbottom=(400, ground_y))

# Start camera centered on the player
camera_x = max(0, min(player.x - SCREEN_WIDTH // 2, WORLD_WIDTH - SCREEN_WIDTH))


# ===================== GAME LOOP =====================
while True:

    # --- Handle Events (closing the window, etc.) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # --- Horizontal Movement ---
    move_x = 0  # how many pixels to move this frame (negative = left, positive = right)

    if keys[pygame.K_a]:
        move_x = -player_speed
        is_facing_left = True
    if keys[pygame.K_d]:
        move_x = player_speed
        is_facing_left = False

    is_moving = move_x != 0

    # --- Jumping ---
    if keys[pygame.K_SPACE] and is_on_ground:
        vertical_velocity = jump_force
        is_on_ground = False

    # --- Apply Gravity (pulls the player down each frame) ---
    vertical_velocity -= gravity

    # --- Move Player Horizontally & Check Block Collisions ---
    player.x += move_x
    for block in blocks:
        if player.colliderect(block):
            if move_x > 0:                  # moving right → pushed back from right side
                player.right = block.left
            else:                           # moving left → pushed back from left side
                player.left = block.right

    # --- Move Player Vertically & Check Block Collisions ---
    player.y -= vertical_velocity          # subtract because pygame's y-axis is flipped
    is_on_ground = False                   # assume in the air until we land on something

    for block in blocks:
        if player.colliderect(block):
            if vertical_velocity < 0:       # player is falling downward
                player.bottom = block.top
                is_on_ground = True
            else:                           # player hit the ceiling
                player.top = block.bottom
            vertical_velocity = 0           # stop vertical movement after hitting something

    # --- Ground Floor (so the player doesn't fall forever) ---
    if player.centery >= ground_y:
        player.centery = ground_y
        vertical_velocity = 0
        is_on_ground = True

    # --- Animation ---
    if is_moving and is_on_ground:
        frame_timer += 1
        if frame_timer >= frames_per_step:
            frame_timer = 0
            current_frame = (current_frame + 1) % len(walk_frames)  # loop through walk frames
    else:
        current_frame = 0   # reset to first frame when standing still or in the air
        frame_timer = 0

    # --- Smooth Camera Follow ---
    target_camera_x = player.centerx - SCREEN_WIDTH // 2           # where we want the camera
    camera_x += (target_camera_x - camera_x) * 0.1                 # slowly move toward target
    camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))    # don't go past the edges

    # --- Drawing ---

    # Draw the background (only the visible slice)
    screen.blit(background, (0, 0), (camera_x, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Draw blocks (only the ones currently on screen)
    for block in blocks:
        screen_x = block.x - camera_x
        if -tile_size < screen_x < SCREEN_WIDTH:   # skip blocks that are off-screen
            screen.blit(block_image, (screen_x, block.y))

    # Pick the right player sprite based on state
    if not is_on_ground:
        player_sprite = sprite_jump_left if is_facing_left else sprite_jump
    elif is_moving:
        player_sprite = walk_frames_left[current_frame] if is_facing_left else walk_frames[current_frame]
    else:
        player_sprite = sprite_stand_left if is_facing_left else sprite_stand

    screen.blit(player_sprite, (player.x - camera_x, player.y))

    # --- Update Display ---
    pygame.display.update()
    clock.tick(60)  # cap the game at 60 frames per second