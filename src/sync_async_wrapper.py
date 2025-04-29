from functools import partial
import asyncio

# Wrapper for sync function
def async_wrap(func):
    async def run(*args, **kwargs):
        loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, pfunc)
    return run