#!/usr/bin/env python3
""" Async generator """
import asyncio
import random
from typing import Generator

async def async_generator():
    """ loop 10 times and in each asynchronously wait 1 second
        then yield a random number between 0 and 10
    """
    for i in range(10):
        await asyncio.sleep(1)
        yield random.randint(0, 10)


