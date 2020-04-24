# -*- coding: utf-8 -*-
from time import sleep

import numpy as np
import pygame

from config import (
    ALIVE,
    ALIVE_COLOUR,
    BG_COLOUR,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CELL_HEIGHT,
    CELL_WIDTH,
    DEAD,
    DEAD_COLOUR,
    NUM_CELLS_X,
    NUM_CELLS_Y,
)


def neighbourhood(game_state, x, y):
    """ Get the Moore neighborhood (8-neighbourhood) considering a Toroidal space

    Ref: https://en.wikipedia.org/wiki/Cellular_automaton
    """
    return (
        game_state[(x - 1) % NUM_CELLS_X, (y - 1) % NUM_CELLS_Y],
        game_state[x % NUM_CELLS_X, (y - 1) % NUM_CELLS_Y],
        game_state[(x + 1) % NUM_CELLS_X, (y - 1) % NUM_CELLS_Y],
        game_state[(x - 1) % NUM_CELLS_X, y % NUM_CELLS_Y],
        game_state[(x + 1) % NUM_CELLS_X, y % NUM_CELLS_Y],
        game_state[(x - 1) % NUM_CELLS_X, (y + 1) % NUM_CELLS_Y],
        game_state[x % NUM_CELLS_X, (y + 1) % NUM_CELLS_Y],
        game_state[(x + 1) % NUM_CELLS_X, (y + 1) % NUM_CELLS_Y],
    )


def update_cell(game_state, x, y):
    """ Apply Conway's Game of Life rules

    Rules:
        1. Any live cell with two or three live neighbors survives.
        2. Any dead cell with three live neighbors becomes a live cell.
        3. All other live cells die in the next generation. Similarly, all other dead
            cells stay dead.
    """
    n_neigh_alive = sum(neighbourhood(game_state, x, y))
    cell_state = game_state[x, y]
    cell_state_next = cell_state

    # Any dead cell with three live neighbors becomes a live cell.
    if cell_state == DEAD:
        if n_neigh_alive == 3:
            cell_state_next = ALIVE

    # Any live cell with two or three live neighbors survives.
    elif cell_state == ALIVE:
        # Underpopulation (death by solitude)
        if n_neigh_alive < 2:
            cell_state_next = DEAD

        # Overpopulation (death by starvation)
        elif n_neigh_alive > 3:
            cell_state_next = DEAD

    return cell_state_next


def update_screen(screen, game_state, x, y):
    """ Update screen """
    cell_status = game_state[x, y]
    polygon = [
        (x * CELL_WIDTH, y * CELL_HEIGHT),
        ((x + 1) * CELL_WIDTH, y * CELL_HEIGHT),
        ((x + 1) * CELL_WIDTH, (y + 1) * CELL_HEIGHT),
        (x * CELL_WIDTH, (y + 1) * CELL_HEIGHT),
    ]

    if cell_status == DEAD:
        pygame.draw.polygon(screen, DEAD_COLOUR, polygon, width=1)
    else:
        pygame.draw.polygon(screen, ALIVE_COLOUR, polygon, width=0)


def on_mouse_click(game_state):
    """ Revive a cell with left-click and kill a cell with right-click """
    mouse = pygame.mouse.get_pressed()
    pos_x, pos_y = pygame.mouse.get_pos()
    cell_x, cell_y = (
        int(np.floor(pos_x / CELL_WIDTH)),
        int(np.floor(pos_y / CELL_HEIGHT)),
    )
    game_state[cell_x, cell_y] = not mouse[2]
    return game_state


def run(screen):
    screen.fill(BG_COLOUR)
    game_state = np.random.randint(0, 2, (NUM_CELLS_X, NUM_CELLS_Y))

    pause = False
    while True:
        new_game_state = np.copy(game_state)
        screen.fill(BG_COLOUR)

        # Allow keyboard and mouse interactions
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.KEYDOWN:
                pause = not pause

            if sum(pygame.mouse.get_pressed()):
                new_game_state = on_mouse_click(new_game_state)

        # Update all cells
        for y in range(0, NUM_CELLS_X):
            for x in range(0, NUM_CELLS_Y):
                if not pause:
                    new_game_state[x, y] = update_cell(game_state, x, y)

                update_screen(screen, game_state, x, y)

        # Update game state
        game_state = np.copy(new_game_state)
        pygame.display.flip()
        sleep(0.1)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((BOARD_HEIGHT, BOARD_WIDTH))
    run(screen)
