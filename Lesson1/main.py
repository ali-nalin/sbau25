#main.py
import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, FPS
import colors
from maze_data import MAZE1, START_POSITION, END_POSITION
from algorithms import bfs

def draw_maze(screen, maze, visited_cells, optimal_path, player_pos, steps_taken):
    """
    Draw the maze, highlighting visited cells in blue, optimal path in cyan,
    and start/end squares in green and red. Also, display the player and steps taken.
    """
    font = pygame.font.SysFont(None, 20)  # Font for step labels

    rows = len(maze)
    cols = len(maze[0])

    # 1) Draw the base maze
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[r][c] == 1:
                color = colors.WALL_COLOR
            else:
                color = colors.UNEXPLORED_COLOR
            pygame.draw.rect(screen, color, rect)

    # 2) Highlight visited cells in blue
    for r, c in visited_cells:
        rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, colors.VISITED_COLOR, rect)

    # 3) Highlight the optimal path in cyan
    for r, c in optimal_path:
        rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, colors.OPTIMAL_PATH_COLOR, rect)

    # 4) Label the start and end squares with "A" and "B"
    start_r, start_c = START_POSITION
    start_rect = pygame.Rect(start_c * CELL_SIZE, start_r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, colors.START_COLOR, start_rect)
    start_text = font.render("A", True, (255, 255, 255))  # white text
    start_text_rect = start_text.get_rect(center=start_rect.center)
    screen.blit(start_text, start_text_rect)

    end_r, end_c = END_POSITION
    end_rect = pygame.Rect(end_c * CELL_SIZE, end_r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, colors.END_COLOR, end_rect)
    end_text = font.render("B", True, (255, 255, 255))  # white text
    end_text_rect = end_text.get_rect(center=end_rect.center)
    screen.blit(end_text, end_text_rect)

    # 5) Draw the player position
    player_r, player_c = player_pos
    player_rect = pygame.Rect(player_c * CELL_SIZE, player_r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, colors.PLAYER_COLOR, player_rect)

    # 6) Display the steps taken counter
    steps_text = font.render(f"Steps: {steps_taken}", True, (255, 255, 255))
    screen.blit(steps_text, (10, 10))  # Display in the top-left corner

    # 7) Draw grid lines for each cell
    for r in range(rows + 1):
        pygame.draw.line(screen, colors.GRID_COLOR, (0, r * CELL_SIZE), (SCREEN_WIDTH, r * CELL_SIZE))  # Horizontal lines
    for c in range(cols + 1):
        pygame.draw.line(screen, colors.GRID_COLOR, (c * CELL_SIZE, 0), (c * CELL_SIZE, SCREEN_HEIGHT))  # Vertical lines


def run_game(screen, clock):
    visited_cells, optimal_path = bfs(MAZE1, START_POSITION, END_POSITION)

    player_pos = list(START_POSITION)
    steps_taken = 0  # Counter for steps

    running = True
    while running:
        clock.tick(FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # WASD Movement logic
                new_r, new_c = player_pos

                if event.key == pygame.K_w:
                    new_r = player_pos[0] - 1
                elif event.key == pygame.K_s:
                    new_r = player_pos[0] + 1
                elif event.key == pygame.K_a:
                    new_c = player_pos[1] - 1
                elif event.key == pygame.K_d:
                    new_c = player_pos[1] + 1

                # Validate movement: stay in bounds & avoid walls
                rows, cols = len(MAZE1), len(MAZE1[0])
                if 0 <= new_r < rows and 0 <= new_c < cols and MAZE1[new_r][new_c] == 0:
                    if [new_r, new_c] != player_pos:
                        player_pos = [new_r, new_c]
                        steps_taken += 1  # Increment steps

        # Draw everything
        screen.fill((0, 0, 0))  # Clear screen
        draw_maze(screen, MAZE1, visited_cells, optimal_path, player_pos, steps_taken)
        pygame.display.flip()  # Update the display

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    run_game(screen, clock)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
