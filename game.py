import random
import sys

import pygame

CELL = 20
COLS, ROWS = 30, 20
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
FPS = 10

BG = (20, 20, 20)
GRID = (30, 30, 30)
SNAKE_HEAD = (80, 220, 100)
SNAKE_BODY = (50, 170, 80)
FOOD = (230, 60, 60)
TEXT = (240, 240, 240)

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)


def random_food(snake):
    free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake]
    return random.choice(free) if free else None


def reset():
    snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
    return snake, RIGHT, random_food(snake), 0


def draw_cell(screen, pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2), border_radius=4)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 64)

    snake, direction, food, score = reset()
    next_direction = direction
    game_over = False

    while True:
        # --- Input ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if game_over:
                    if event.key == pygame.K_r:
                        snake, direction, food, score = reset()
                        next_direction = direction
                        game_over = False
                    continue
                if event.key in (pygame.K_UP, pygame.K_w) and direction != DOWN:
                    next_direction = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != UP:
                    next_direction = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != RIGHT:
                    next_direction = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != LEFT:
                    next_direction = RIGHT

        if not game_over:
            direction = next_direction
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            hit_wall = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
            hit_self = new_head in snake[:-1]

            if hit_wall or hit_self:
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food(snake)
                    if food is None:
                        game_over = True
                else:
                    snake.pop()

        screen.fill(BG)
        for x in range(COLS):
            for y in range(ROWS):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(screen, GRID, (x * CELL, y * CELL, CELL, CELL))

        if food:
            draw_cell(screen, food, FOOD)
        for i, segment in enumerate(snake):
            draw_cell(screen, segment, SNAKE_HEAD if i == 0 else SNAKE_BODY)

        screen.blit(font.render(f"Score: {score}", True, TEXT), (10, 8))

        if game_over:
            over = big_font.render("Game Over", True, TEXT)
            hint = font.render("Press R to restart or Esc to quit", True, TEXT)
            screen.blit(over, over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
            screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()