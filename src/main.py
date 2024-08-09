import asyncio
import math
from contextlib import suppress

import media
from gamesense import GameSense
from gtk import BasicGTK
from gtk.manager import DrawMode
from screen import OLEDScreen


def format_seconds(seconds: float) -> str:
    seconds = math.floor(seconds)
    return f'{seconds // 60:02}:{seconds % 60:02}'


async def draw_thread(screen: OLEDScreen):
    while True:
        sleep = 0.1

        async with BasicGTK(screen) as gtk:
            if media.latest_event:
                gtk.draw_center_text(2, media.latest_event)
                media.latest_event = None
                sleep = 1
            else:
                if media.latest_media:
                    gtk.draw_big_text(0, media.latest_media.title, 6.)
                    gtk.draw_big_text(12, media.latest_media.artist, 6.)

                    position_progress = (
                            media.latest_media.calculated_position.total_seconds() / media.latest_media.end.total_seconds())

                    gtk.draw_progress(2, 24, screen.size[0] - 4, 10, position_progress)
                    gtk.draw_center_text(26,
                                         f'{format_seconds(media.latest_media.calculated_position.total_seconds())} - {format_seconds(media.latest_media.end.total_seconds())}',
                                         DrawMode.FLIP)
                else:
                    gtk.draw_text(2, 2, "No music")

        await asyncio.sleep(sleep)


async def fetch_music_thread() -> None:
    while True:
        await media.get_media_info()
        await asyncio.sleep(0.05)


async def main():
    size = (128, 40)

    gs = GameSense('GRAPHICS', 'Music display', 'kewldan')
    await gs.register_game()

    screen = OLEDScreen(gs, size)

    await screen.init()

    await asyncio.gather(fetch_music_thread(), draw_thread(screen))


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
