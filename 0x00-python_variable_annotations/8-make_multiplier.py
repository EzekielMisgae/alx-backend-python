#!/usr/bin/env python3
""" Takes a float multiplier,
returns a function that multiplies a float by multiplier """

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Takes a float and returns a float"""
    return (lambda x: multiplier*x)
