import asyncio
import math
import random
import time
from contextlib import suppress

import media
from config import config
from gamesense import GameSense
from gtk import BasicGTK
from gtk.buffer import FrameBuffer
from gtk.manager import DrawMode
from screen import OLEDScreen
from views import views


async def draw_thread(screen: OLEDScreen):
    event_start = None
    using_transition = None
    main_buffer = FrameBuffer(screen.size)
    virtual_buffer = FrameBuffer(screen.size)
    super_buffer = None

    while True:
        sleep = 1 / config.refresh_rate

        if media.latest_event == 'new_song' and using_transition is None:
            super_buffer = FrameBuffer(screen.size)
            super_buffer.buffer = main_buffer.buffer.copy()
            using_transition = config.transition

            if using_transition == 'random':
                using_transition = random.choice(['slide_x', 'slide_y', 'circle'])

        gtk = BasicGTK(virtual_buffer)

        if config.events_duration > 0 and media.latest_event in ['resumed', 'paused']:
            gtk.draw_center_text(2, media.latest_event)
            media.latest_event = None
            sleep = config.events_duration
        else:
            if media.latest_media:
                views[config.view].draw(gtk)
            else:
                gtk.draw_center_text(2, "No music")

        screen_gtk = BasicGTK(main_buffer)

        if media.latest_event == 'new_song':
            if event_start is None:
                event_start = time.time()

            elapsed = time.time() - event_start

            match using_transition:
                case 'circle':
                    gtk.draw_circle(screen.size[0] // 2, screen.size[1] // 2, elapsed * 50, DrawMode.FLIP)
                    gtk.draw_circle(screen.size[0] // 2, screen.size[1] // 2, (elapsed - 0.4) * 50, DrawMode.FLIP)

                    screen_gtk.draw_bitmap(0, 0, main_buffer.size[0], main_buffer.size[1], gtk.buffer.buffer,
                                           f=DrawMode.BLACK)
                case 'slide_x':
                    x = -math.floor(elapsed * (screen.size[0] / config.transition_duration))

                    screen_gtk.draw_bitmap(x, 0, screen.size[0], screen.size[1], super_buffer.buffer,
                                           f=DrawMode.BLACK)
                    screen_gtk.draw_bitmap(x + screen.size[0], 0, main_buffer.size[0], main_buffer.size[1],
                                           gtk.buffer.buffer,
                                           f=DrawMode.BLACK)
                case 'slide_y':
                    y = -math.floor(elapsed * (screen.size[1] / config.transition_duration))

                    screen_gtk.draw_bitmap(0, y, screen.size[0], screen.size[1], super_buffer.buffer,
                                           f=DrawMode.BLACK)
                    screen_gtk.draw_bitmap(0, y + screen.size[1], main_buffer.size[0], main_buffer.size[1],
                                           gtk.buffer.buffer,
                                           f=DrawMode.BLACK)
                case _:
                    raise NotImplementedError(f'Unknown transition: {using_transition}')

            if time.time() - event_start > config.transition_duration:
                media.latest_event = None
                event_start = None
                super_buffer = None
                using_transition = None
        else:
            screen_gtk.draw_bitmap(0, 0, main_buffer.size[0], main_buffer.size[1], gtk.buffer.buffer, f=DrawMode.BLACK)

        await screen.send(main_buffer.buffer)

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
