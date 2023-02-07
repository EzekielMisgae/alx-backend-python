#!/usr/bin/env python3
""" Async generator """
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """ loop 10 times and in each asynchronously wait 1 second
        then yield a random number between 0 and 10
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
