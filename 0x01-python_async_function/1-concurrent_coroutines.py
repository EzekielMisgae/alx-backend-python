#!/usr/bin/env python3
'''Asynch function basics'''
import asyncio
import random
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int = 10) -> List[float]:
    """ Waits wait_random n times """
    tasks = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]
    delay = [await task for task in asyncio.as_completed(tasks)]
    return delay
