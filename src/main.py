import asyncio
from contextlib import suppress

from gamesense import GameSense
from screen import OLEDScreen


async def main():
    size = (128, 40)

    gs = GameSense('GRAPHICS', 'Graphics App', 'kewldan')
    await gs.register_game()

    screen = OLEDScreen(gs, size)

    await screen.init()

    while True:
        screen.buffer = [255] * len(screen.buffer)
        await screen.release()
        await asyncio.sleep(0.5)
        screen.buffer = [0] * len(screen.buffer)
        await screen.release()
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
