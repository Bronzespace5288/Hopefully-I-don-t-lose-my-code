import pygame
import random

pygame.init()

# Game dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Screen size calculation
screen_width = GRID_WIDTH * BLOCK_SIZE + 200  # Extra space for next piece and score
screen_height = GRID_HEIGHT * BLOCK_SIZE
SCREEN_SIZE = (screen_width, screen_height)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SHAPE_COLORS = {
    'L': (255, 0, 255),  # Magenta
    'J': (255, 165, 0),  # Orange
    'Z': (255, 255, 0),  # Yellow
    'S': (176, 38, 255),  # neon purple
    'T': (255, 0, 0),    # Bright Red
    'I': (0, 255, 0),    # Neon Green
    'O': (0, 0, 255)     # Blue
}

# Shapes
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'L': [[1, 0], [1, 0], [1, 1]],
    'J': [[0, 1], [0, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}

# Display
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Tetris")

# Game variables
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_shape = None
current_pos = [0, 0]
current_shape_type = None
next_shape_type = None
score = 0
high_score = 0

# Movement delay variables
MOVE_DELAY = 85  # milliseconds
move_time = 0

# Speed progression variables
BASE_FALL_SPEED = 0.5  # Initial fall speed in seconds
SPEED_INCREMENT = 0.05  # Speed increase per level
MAX_SPEED = 0.1  # Maximum speed (minimum time between falls)

def calculate_fall_speed(score):
    level = score // 1000 + 1  # Increase level every 1000 points
    return max(BASE_FALL_SPEED - (level - 1) * SPEED_INCREMENT, MAX_SPEED)

def rotate_shape(shape):
    return list(zip(*shape[::-1]))

def create_shape():
    global current_shape, current_pos, current_shape_type, next_shape_type
    if next_shape_type is None:
        next_shape_type = random.choice(list(SHAPES.keys()))
    current_shape_type = next_shape_type
    current_shape = SHAPES[current_shape_type]
    next_shape_type = random.choice(list(SHAPES.keys()))
    
    # Randomly rotate the shape 0-3 times
    for _ in range(random.randint(0, 3)):
        current_shape = rotate_shape(current_shape)
    
    # Adjust spawn position based on shape width
    current_pos = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
    
    # Adjust spawn position if it's out of bounds
    while current_pos[0] < 0:
        current_pos[0] += 1
    while current_pos[0] + len(current_shape[0]) > GRID_WIDTH:
        current_pos[0] -= 1
    
    return current_shape_type

def draw_shape(shape, pos, color):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color,
                                 ((pos[0] + x) * BLOCK_SIZE, (pos[1] + y) * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE))

def draw_grid():
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, SHAPE_COLORS[cell],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            # Draw grid lines
            pygame.draw.rect(screen, (50, 50, 50),
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def check_collision(shape, pos):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if (pos[1] + y >= GRID_HEIGHT or
                    pos[0] + x < 0 or pos[0] + x >= GRID_WIDTH or
                    grid[pos[1] + y][pos[0] + x]):
                    return True
    return False

def merge_shape():
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell:
                grid[current_pos[1] + y][current_pos[0] + x] = current_shape_type

def remove_full_rows():
    global grid, score
    full_rows = [i for i, row in enumerate(grid) if all(row)]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    score += len(full_rows) * 100  # 100 points per row cleared

def adjust_rotation(shape, pos):
    new_pos = list(pos)
    while check_collision(shape, new_pos):
        if new_pos[0] < GRID_WIDTH // 2:
            new_pos[0] += 1
        else:
            new_pos[0] -= 1
    return new_pos

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_next_shape():
    next_shape = SHAPES[next_shape_type]
    shape_width = len(next_shape[0]) * BLOCK_SIZE
    shape_height = len(next_shape) * BLOCK_SIZE
    start_x = screen_width - 150 + (100 - shape_width) // 2
    start_y = 100 + (100 - shape_height) // 2
    
    for y, row in enumerate(next_shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, SHAPE_COLORS[next_shape_type],
                                 (start_x + x * BLOCK_SIZE, start_y + y * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE))

def show_game_over_screen():
    global high_score
    screen.fill(BLACK)
    if score > high_score:
        high_score = score
        draw_text("NEW HIGH SCORE!", 48, WHITE, screen_width // 2, screen_height // 2 - 50)
    draw_text(f"Game Over", 64, WHITE, screen_width // 2, screen_height // 2)
    draw_text(f"Score: {score}", 32, WHITE, screen_width // 2, screen_height // 2 + 50)
    draw_text(f"High Score: {high_score}", 32, WHITE, screen_width // 2, screen_height // 2 + 100)
    draw_text("Press any key to play again", 24, WHITE, screen_width // 2, screen_height - 50)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYUP:
                waiting = False
    return True

def game_loop():
    global current_shape, current_pos, current_shape_type, grid, score, move_time
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = BASE_FALL_SPEED  # Start with base fall speed
    shape_type = create_shape()
    running = True

    while running:
        fall_time += clock.get_rawtime()
        move_time += clock.get_rawtime()
        clock.tick()

        # Update fall speed based on score
        fall_speed = calculate_fall_speed(score)

        # Handle continuous movement
        keys = pygame.key.get_pressed()
        if move_time > MOVE_DELAY:
            if keys[pygame.K_LEFT]:
                new_pos = [current_pos[0] - 1, current_pos[1]]
                if not check_collision(current_shape, new_pos):
                    current_pos = new_pos
                move_time = 0
            elif keys[pygame.K_RIGHT]:
                new_pos = [current_pos[0] + 1, current_pos[1]]
                if not check_collision(current_shape, new_pos):
                    current_pos = new_pos
                move_time = 0
            elif keys[pygame.K_DOWN]:
                for i in range(2):
                    new_pos = [current_pos[0], current_pos[1] + 1]
                    if not check_collision(current_shape, new_pos):
                        current_pos = new_pos
                move_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotated_shape = rotate_shape(current_shape)
                    new_pos = adjust_rotation(rotated_shape, current_pos)
                    if not check_collision(rotated_shape, new_pos):
                        current_shape = rotated_shape
                        current_pos = new_pos

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            new_pos = [current_pos[0], current_pos[1] + 1]
            if check_collision(current_shape, new_pos):
                merge_shape()
                remove_full_rows()
                shape_type = create_shape()
                if check_collision(current_shape, current_pos):
                    running = False
            else:
                current_pos = new_pos

        screen.fill(BLACK)
        draw_grid()
        draw_shape(current_shape, current_pos, SHAPE_COLORS[shape_type])
        draw_text(f"Score: {score}", 24, WHITE, screen_width - 100, 20)
        draw_text(f"Level: {score // 1000 + 1}", 24, WHITE, screen_width - 100, 50)
        draw_text("Next:", 24, WHITE, screen_width - 100, 80)
        draw_next_shape()
        pygame.display.flip()

    return True

# Main game
while True:
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    score = 0
    next_shape_type = None
    if game_loop():
        if not show_game_over_screen():
            break
    else:
        break

pygame.quit()