import asyncio
import math
import time
from contextlib import suppress

import media
from config import config
from gamesense import GameSense
from gtk import BasicGTK
from gtk.manager import DrawMode
from screen import OLEDScreen


def format_seconds(seconds: float) -> str:
    seconds = math.floor(seconds)
    return f'{seconds // 60:02}:{seconds % 60:02}'


def draw_icon(arr: list, w: int, h: int):
    if len(arr) < w * h:
        rows = []
        for r in range(0, len(arr), len(arr) // w):
            rows.append(arr[r:r + len(arr) // h - 1])
        for i, r in enumerate(rows):
            if len(r) < w:
                rows[i].extend([0] * (w - len(r)))
        if len(rows) < h:
            rows.extend([[0] * w] * (h - len(rows)))
        arr = [a for b in rows for a in b]

    new_arr = []
    temp_byte = ''
    for c in arr:
        if int(c) > 1:
            c = 1
        temp_byte += str(c)
        if len(temp_byte) == 8:
            new_arr.append(int(temp_byte, 2))
            temp_byte = ''
    return new_arr


async def draw_thread(screen: OLEDScreen):
    event_start = None

    while True:
        sleep = 1 / config.refresh_rate

        async with BasicGTK(screen) as gtk:
            if config.events_duration > 0 and media.latest_event in ['resumed', 'paused']:
                gtk.draw_center_text(2, media.latest_event)
                media.latest_event = None
                sleep = config.events_duration
            else:
                if media.latest_icon:
                    b = draw_icon(media.latest_icon, 40, 40)

                    gtk.draw_bitmap(0, 0, 40, 40, b)

                if media.latest_media:
                    gtk.draw_text(42, 0, media.latest_media.title, config.text_speed)
                    gtk.draw_text(42, 7 + config.row_gap, media.latest_media.artist, config.text_speed)

                    position_progress = (
                            media.latest_media.calculated_position.total_seconds() / media.latest_media.end.total_seconds())

                    gtk.draw_progress(2, 14 + config.row_gap * 2, screen.size[0] - 4, 10, position_progress)
                    gtk.draw_center_text(14 + config.row_gap * 2 + 2,
                                         f'{format_seconds(media.latest_media.calculated_position.total_seconds())} - {format_seconds(media.latest_media.end.total_seconds())}',
                                         DrawMode.FLIP)
                else:
                    gtk.draw_text(2, 2, "No music")

            if media.latest_event == 'new_song':
                if event_start is None:
                    event_start = time.time()

                elapsed = time.time() - event_start

                if config.transition == 'circle':
                    gtk.draw_circle(screen.size[0] // 2, screen.size[1] // 2, elapsed * 50, DrawMode.FLIP)
                    gtk.draw_circle(screen.size[0] // 2, screen.size[1] // 2, (elapsed - 0.4) * 50, DrawMode.FLIP)
                elif config.transition == 'slide':
                    pass

                if time.time() - event_start > 2:
                    media.latest_event = None
                    event_start = None

        await asyncio.sleep(sleep)


async def fetch_music_thread() -> None:
    while True:
        await media.get_media_info()
        await asyncio.sleep(1 / config.music_refresh_rate)


async def main():
    size = (config.width, config.height)

    gs = GameSense('GRAPHICS', 'Music display', 'kewldan')
    await gs.register_game()

    screen = OLEDScreen(gs, size)

    await screen.init()

    await asyncio.gather(fetch_music_thread(), draw_thread(screen))


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
