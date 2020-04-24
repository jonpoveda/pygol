# -*- coding: utf-8 -*-
import argparse

from game import execute, initial_method_options

init_options = ", ".join(initial_method_options.keys())

parser = argparse.ArgumentParser()
parser.add_argument(
    "init",
    help=f"Select initialization. Options: {init_options} (default: random)",
    type=str,
    default="random",
)
args = parser.parse_args()

execute(args.init)
