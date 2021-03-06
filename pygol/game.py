# -*- coding: utf-8 -*-
from time import sleep

import numpy as np
import pygame

from automaton import (
    add_automaton_glider,
    add_automaton_oscillator_blinker,
    add_automaton_oscillator_line,
    add_automaton_square,
)
from config import Board, Cell, Colour


def neighbourhood(game_state, x, y):
    """ Get the Moore neighborhood (8-neighbourhood) considering a Toroidal space

    Ref: https://en.wikipedia.org/wiki/Cellular_automaton
    """
    return (
        game_state[(x - 1) % Board.NUM_CELLS_X, (y - 1) % Board.NUM_CELLS_Y],
        game_state[x % Board.NUM_CELLS_X, (y - 1) % Board.NUM_CELLS_Y],
        game_state[(x + 1) % Board.NUM_CELLS_X, (y - 1) % Board.NUM_CELLS_Y],
        game_state[(x - 1) % Board.NUM_CELLS_X, y % Board.NUM_CELLS_Y],
        game_state[(x + 1) % Board.NUM_CELLS_X, y % Board.NUM_CELLS_Y],
        game_state[(x - 1) % Board.NUM_CELLS_X, (y + 1) % Board.NUM_CELLS_Y],
        game_state[x % Board.NUM_CELLS_X, (y + 1) % Board.NUM_CELLS_Y],
        game_state[(x + 1) % Board.NUM_CELLS_X, (y + 1) % Board.NUM_CELLS_Y],
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
    if cell_state == Cell.DEAD.value:
        if n_neigh_alive == 3:
            cell_state_next = Cell.ALIVE.value

    # Any live cell with two or three live neighbors survives.
    elif cell_state == Cell.ALIVE.value:
        # Underpopulation (death by solitude)
        if n_neigh_alive < 2:
            cell_state_next = Cell.DEAD.value

        # Overpopulation (death by starvation)
        elif n_neigh_alive > 3:
            cell_state_next = Cell.DEAD.value

    return cell_state_next


def update_screen(screen, game_state, x, y):
    """ Update screen """
    cell_status = game_state[x, y]
    polygon = [
        (x * Board.CELL_WIDTH, y * Board.CELL_HEIGHT),
        ((x + 1) * Board.CELL_WIDTH, y * Board.CELL_HEIGHT),
        ((x + 1) * Board.CELL_WIDTH, (y + 1) * Board.CELL_HEIGHT),
        (x * Board.CELL_WIDTH, (y + 1) * Board.CELL_HEIGHT),
    ]

    if cell_status == Cell.DEAD.value:
        pygame.draw.polygon(screen, Colour.DEAD.value, polygon, width=1)
    else:
        pygame.draw.polygon(screen, Colour.ALIVE.value, polygon, width=0)


def on_mouse_click(game_state):
    """ Revive a cell with left-click and kill a cell with right-click """
    mouse = pygame.mouse.get_pressed()
    pos_x, pos_y = pygame.mouse.get_pos()
    cell_x, cell_y = (
        int(np.floor(pos_x / Board.CELL_WIDTH)),
        int(np.floor(pos_y / Board.CELL_HEIGHT)),
    )
    game_state[cell_x, cell_y] = not mouse[2]
    return game_state


def clear_screen(screen):
    screen.fill(Colour.BG.value)


def random_state():
    return np.random.choice(
        (Cell.ALIVE.value, Cell.DEAD.value), (Board.NUM_CELLS_X, Board.NUM_CELLS_Y)
    )


def populate_with_automata():
    game_state = np.zeros((Board.NUM_CELLS_X, Board.NUM_CELLS_Y))
    game_state = add_automaton_oscillator_line(game_state, 2, 2)
    game_state = add_automaton_square(game_state, 12, 2)
    game_state = add_automaton_oscillator_blinker(game_state, 2, 12)
    game_state = add_automaton_glider(game_state, 12, 12)
    return game_state


def run(screen, initial_method):
    """ Runs the game using a configured screen

     Args:
         screen: a configured pygame screen
         initial_method: a function to initialize the board
     """
    clear_screen(screen)
    game_state = initial_method()

    pause = False
    stop = False
    while not stop:
        new_game_state = np.copy(game_state)
        clear_screen(screen)

        # Allow keyboard and mouse interactions
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.KEYDOWN:
                pause = not pause

                if event.key == pygame.K_q:
                    stop = True

            if sum(pygame.mouse.get_pressed()):
                new_game_state = on_mouse_click(new_game_state)

        # Update all cells
        for y in range(0, Board.NUM_CELLS_X):
            for x in range(0, Board.NUM_CELLS_Y):
                if not pause:
                    new_game_state[x, y] = update_cell(game_state, x, y)

                update_screen(screen, game_state, x, y)

        # Update game state
        game_state = np.copy(new_game_state)
        pygame.display.flip()
        sleep(0.1)


initial_method_options = {
    "random": random_state,
    "auto1": populate_with_automata,
}


def execute(initial_method):
    """ Execute the game """
    pygame.init()
    screen = pygame.display.set_mode((Board.HEIGHT, Board.WIDTH))
    try:
        run(screen, initial_method_options[initial_method])
    except KeyError:
        print("Incorrect initialization name. Check help `-h`. Exiting.")
    exit(0)


if __name__ == "__main__":
    execute("random")
