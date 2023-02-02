#!/usr/bin/env python3
""" Takes a string k and an int OR float, returns a tuple """

from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Takes a string and int/float and returns a tuple"""
    return (k, v ** 2)
