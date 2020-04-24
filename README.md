[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# The Game of Life

This project is about implementing a basic version of the Conway's [_The Game of Life_][wiki-tgol] in python.

## How to run

Create a python virtualenv using [pipenv][pipenv-doc]

```shell script
pipenv install
```

To run it as a command-line program execute:

```shell script
python pygol/game.py
```

## Interaction

- You can quit the game by pressing `q`
- You can pause and resume the game pressing any key in your keyboard
- You can change cell state (alive, dead) using the mouse:
    - Left-click for setting a cell alive
    - Right-click for setting a cell dead

[wiki-tgol]: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
[pipenv-doc]: https://pipenv.pypa.io/en/latest/
