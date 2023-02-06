#!/usr/bin/env python3
'''Asynch function basics'''
import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''takes in an argument, waits for a random delay, returns it.'''
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    delay = [await task for task in asyncio.as_completed(tasks)]
    return delay
