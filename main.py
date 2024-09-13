import asyncio

from bot import main
from notification import run_task

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.gather(main(), run_task()))