import pygame
import sys
import random
import time

WIDTH, HEIGHT = 1080,720
CELL_SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN1 = (170, 215, 81)
GREEN2 = (162, 209, 73)
SNAKE_HEAD = (60, 60, 60)
SNAKE_BODY = (120, 120, 120)
APPLE_RED = (220, 0, 0)
APPLE_STEM = (34, 139, 34)

DIFFICULTIES = [
    {"name": "Easy", "fps": 10, "food_time": 30},
    {"name": "Hard", "fps": 20, "food_time": 20},
    {"name": "Nightmare", "fps": 40, "food_time": 10}
]

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game (Grass Design)")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)

def draw_text_center(text, y, font, color=WHITE):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, rect)

def random_food(snake):
    while True:
        pos = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
               random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        if pos not in snake:
            return pos

def draw_button(text, rect, selected):
    color = WHITE if selected else (100, 100, 100)
    pygame.draw.rect(screen, color, rect, 2)
    draw_text_center(text, rect.centery, small_font, color)

def game_over_screen(score):
    selected = 0
    buttons = ["Restart", "Quit"]
    rects = [pygame.Rect(WIDTH//2-80, HEIGHT//2+40+i*50, 160, 40) for i in range(2)]
    while True:
        screen.fill(BLACK)
        draw_text_center("Game Over", HEIGHT//2-60, font)
        draw_text_center(f"Score: {score}", HEIGHT//2-20, small_font)
        for i, rect in enumerate(rects):
            draw_button(buttons[i], rect, i == selected)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected = (selected - 1) % 2
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected = (selected + 1) % 2
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if selected == 0:
                        return True
                    else:
                        pygame.quit()
                        sys.exit()

def pause_screen():
    selected = 0
    buttons = ["Restart", "Resume", "Quit"]
    rects = [pygame.Rect(WIDTH//2-80, HEIGHT//2-20+i*50, 160, 40) for i in range(3)]
    while True:
        screen.fill(BLACK)
        draw_text_center("Paused", HEIGHT//2-60, font)
        for i, rect in enumerate(rects):
            draw_button(buttons[i], rect, i == selected)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected = (selected - 1) % 3
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected = (selected + 1) % 3
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if selected == 0:
                        return "restart"
                    elif selected == 1:
                        return "resume"
                    else:
                        pygame.quit()
                        sys.exit()

def draw_grass_background():
    for y in range(0, HEIGHT, CELL_SIZE):
        for x in range(0, WIDTH, CELL_SIZE):
            color = GREEN1 if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0 else GREEN2
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

def draw_snake(snake):
    for i, segment in enumerate(snake):
        x, y = segment
        if i == 0:
            pygame.draw.circle(screen, SNAKE_HEAD, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2)
            eye_offset = 4
            if len(snake) > 1:
                dx = snake[0][0] - snake[1][0]
                dy = snake[0][1] - snake[1][1]
            else:
                dx, dy = 1, 0
            if dx > 0:
                eye1 = (x + CELL_SIZE - eye_offset, y + eye_offset)
                eye2 = (x + CELL_SIZE - eye_offset, y + CELL_SIZE - eye_offset)
            elif dx < 0: 
                eye1 = (x + eye_offset, y + eye_offset)
                eye2 = (x + eye_offset, y + CELL_SIZE - eye_offset)
            elif dy > 0: 
                eye1 = (x + eye_offset, y + CELL_SIZE - eye_offset)
                eye2 = (x + CELL_SIZE - eye_offset, y + CELL_SIZE - eye_offset)
            else: 
                eye1 = (x + eye_offset, y + eye_offset)
                eye2 = (x + CELL_SIZE - eye_offset, y + eye_offset)
            pygame.draw.circle(screen, WHITE, eye1, 3)
            pygame.draw.circle(screen, WHITE, eye2, 3)
        else:
            pygame.draw.rect(screen, SNAKE_BODY, (x+2, y+2, CELL_SIZE-4, CELL_SIZE-4), border_radius=6)

def draw_food(food):
    x, y = food
    pygame.draw.rect(screen, APPLE_RED, (x+4, y+4, CELL_SIZE-8, CELL_SIZE-8), border_radius=8)
    pygame.draw.rect(screen, APPLE_STEM, (x + CELL_SIZE // 2 - 2, y + 2, 4, 7), border_radius=2)

def difficulty_screen():
    selected = 0
    rects = [pygame.Rect(WIDTH//2-80, HEIGHT//2-40+i*60, 160, 50) for i in range(3)]
    while True:
        screen.fill(BLACK)
        draw_text_center("Select Difficulty", HEIGHT//2-100, font)
        for i, rect in enumerate(rects):
            draw_button(DIFFICULTIES[i]["name"], rect, i == selected)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected = (selected - 1) % 3
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected = (selected + 1) % 3
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    return DIFFICULTIES[selected]

def main():
    while True:
        difficulty = difficulty_screen()
        FPS = difficulty["fps"]
        food_time_limit = difficulty["food_time"]
        snake = [(WIDTH//2, HEIGHT//2)]
        direction = RIGHT
        food = random_food(snake)
        score = 0
        food_spawn_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w] and direction != DOWN:
                        direction = UP
                    elif event.key in [pygame.K_DOWN, pygame.K_s] and direction != UP:
                        direction = DOWN
                    elif event.key in [pygame.K_LEFT, pygame.K_a] and direction != RIGHT:
                        direction = LEFT
                    elif event.key in [pygame.K_RIGHT, pygame.K_d] and direction != LEFT:
                        direction = RIGHT
                    elif event.key == pygame.K_ESCAPE:
                        action = pause_screen()
                        if action == "restart":
                            break
                        elif action == "resume":
                            continue
            else:
                head_x, head_y = snake[0]
                dx, dy = direction
                new_head = ((head_x + dx * CELL_SIZE) % WIDTH,
                            (head_y + dy * CELL_SIZE) % HEIGHT)
                if new_head in snake:
                    if game_over_screen(score):
                        break
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food(snake)
                    food_spawn_time = time.time()
                else:
                    snake.pop()
                if time.time() - food_spawn_time > food_time_limit:
                    food = random_food(snake)
                    food_spawn_time = time.time()
                draw_grass_background()
                draw_snake(snake)
                draw_food(food)
                draw_text_center(f"Score: {score}", 20, small_font)
                pygame.display.flip()
                clock.tick(FPS)
                continue
            break

if __name__ == "__main__":
    main()