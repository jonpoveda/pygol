# -*- coding: utf-8 -*-
""" Some known automata

Reference: `Jarkko Kari - Cellular Automata`__

.. _Automata: https://www.cs.tau.ac.il/~nachumd/models/CA.pdf

__ Automata_
"""

from config import Cell


def add_automaton_glider(game_state, x, y):
    """ Adds an still life square automaton.

    Representation::

         x
          x
        xxx
    """
    game_state[x + 1, y + 1] = Cell.ALIVE.value
    game_state[x + 2, y + 2] = Cell.ALIVE.value
    game_state[x + 2, y + 3] = Cell.ALIVE.value
    game_state[x + 1, y + 3] = Cell.ALIVE.value
    game_state[x, y + 3] = Cell.ALIVE.value
    return game_state


def add_automaton_square(game_state, x, y):
    """ Adds an still life square automaton.

    Representation::

        xx
        xx
    """
    game_state[x, y] = Cell.ALIVE.value
    game_state[x, y + 1] = Cell.ALIVE.value
    game_state[x + 1, y] = Cell.ALIVE.value
    game_state[x + 1, y + 1] = Cell.ALIVE.value
    return game_state


def add_automaton_oscillator_line(game_state, x, y):
    """ Adds an oscillator line automaton.

    Representation::

        xxx
    """
    game_state[x, y] = Cell.ALIVE.value
    game_state[x, y + 1] = Cell.ALIVE.value
    game_state[x, y + 2] = Cell.ALIVE.value
    return game_state


def add_automaton_oscillator_blinker(game_state, x, y):
    """ Adds an oscillator blinker automaton.

    Representation::

         xxx
        xxx
    """
    game_state[x + 1, y] = Cell.ALIVE.value
    game_state[x + 2, y] = Cell.ALIVE.value
    game_state[x + 3, y] = Cell.ALIVE.value
    game_state[x, y + 1] = Cell.ALIVE.value
    game_state[x + 1, y + 1] = Cell.ALIVE.value
    game_state[x + 2, y + 1] = Cell.ALIVE.value
    return game_state
