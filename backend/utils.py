import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, Any


async def run_in_executor(func: Callable, *args: Any) -> Any:
    with ProcessPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, func, *args)
