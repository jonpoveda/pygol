# -*- coding: utf-8 -*-
import enum
from enum import Enum


@enum.unique
class Cell(Enum):
    DEAD = 0
    ALIVE = 1


class Board(object):
    HEIGHT, WIDTH = 1024, 1024
    NUM_CELLS_X, NUM_CELLS_Y = 25, 25
    CELL_HEIGHT = HEIGHT / NUM_CELLS_Y
    CELL_WIDTH = WIDTH / NUM_CELLS_X


class Colour(Enum):
    BG = 25, 25, 25
    DEAD = 128, 128, 128
    ALIVE = 255, 255, 255
