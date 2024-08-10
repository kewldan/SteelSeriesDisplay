import math

import media
from config import ViewName, config
from gtk import BasicGTK
from gtk.manager import DrawMode
from utils import format_seconds
from .base import View


class WithIconView(View):

    @property
    def name(self) -> ViewName:
        return 'with_icon'

    def draw(self, gtk: BasicGTK) -> None:
        if media.latest_bitmap:
            gtk.draw_bitmap(0, 0, 40, 40, media.latest_bitmap)

        gtk.draw_big_text(42, 0, media.latest_media.title, config.text_speed)
        gtk.draw_big_text(42, 10, media.latest_media.artist, config.text_speed)

        gtk.draw_text(42, 28,
                      f'{format_seconds(media.latest_media.calculated_position.total_seconds())}\r-\r{format_seconds(media.latest_media.end.total_seconds())}')

        for i in range(gtk.buffer.size[0] - 42):
            if i & 1:
                gtk.set_pixel(42 + i, 36, DrawMode.WHITE)
                gtk.set_pixel(42 + i, 38, DrawMode.WHITE)
            else:
                gtk.set_pixel(42 + i, 37, DrawMode.WHITE)
                gtk.set_pixel(42 + i, 39, DrawMode.WHITE)

        gtk.draw_rect(42, 36, math.floor(media.latest_media.position_progress * (gtk.buffer.size[0] - 42)), 4)
