import math
import time
from enum import Enum
from typing import Callable

from config import config
from .alphabet import bitmap_font
from .buffer import FrameBuffer


class DrawMode(Enum):
    NONE = -1
    WHITE = 0
    BLACK = 1
    FLIP = 2


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_text_width(text: str) -> int:
    return len(text) * 7


class BasicGTK:
    def __init__(self, buffer: FrameBuffer, clear_buffer: bool = True):
        self.buffer = buffer
        if clear_buffer:
            self.buffer.clear()

    def draw_callable(self, x: int, y: int, w: int, h: int, get_pixel: Callable[[int, int], bool],
                      t: DrawMode, f: DrawMode, **kwargs):
        for i in range(w):
            for j in range(h):
                self.set_pixel(x + i, y + j, t if get_pixel(i, j) else f, **kwargs)

    def draw_rect(self, x: int, y: int, w: int, h: int, t: DrawMode = DrawMode.WHITE, f: DrawMode = DrawMode.NONE,
                  **kwargs):
        self.draw_callable(x, y, w, h, lambda _, _0: True, t, f, **kwargs)

    def draw_bitmap(self, x: int, y: int, w: int, h: int, bitmap: list[int], t: DrawMode = DrawMode.WHITE,
                    f: DrawMode = DrawMode.NONE, **kwargs):
        self.draw_callable(x, y, w, h, lambda i, j: bool(bitmap[(i + j * w) // 8] & (1 << (7 - (i % 8)))), t, f,
                           **kwargs)

    def draw_text(self, x: int, y: int, text: str, mode: DrawMode = DrawMode.WHITE, **kwargs):
        margin = 0

        for letter in text.upper():
            if letter == '\r':
                margin += 4
                continue
            bitmap = bitmap_font.get(letter)
            if bitmap:
                self.draw_bitmap(x + margin, y, 8, 7, bitmap, mode, DrawMode.NONE, **kwargs)
            margin += 7

    def draw_center_text(self, y: int, text: str, mode: DrawMode = DrawMode.WHITE, **kwargs):
        width = get_text_width(text)

        x = (self.buffer.size[0] - width) // 2

        self.draw_text(x, y, text, mode, **kwargs)

    def draw_big_text(self, x: int, y: int, text: str, speed: float = 1., **kwargs):
        max_width = self.buffer.size[0] - x
        width = get_text_width(text)
        if width > max_width:
            text = text + '   '
            width = get_text_width(text)

            full_cycle = width / speed

            cycle = time.time() % (full_cycle + config.carousel_stop_time)
            if cycle < config.carousel_stop_time:
                self.draw_text(x, y, text)
            else:
                self.draw_text(x - (math.floor((cycle - config.carousel_stop_time) * speed) % width), y, text * 2,
                               bounds=(x, y, *self.buffer.size), **kwargs)
        else:
            self.draw_text(x, y, text)

    def draw_progress(self, x: int, y: int, w: int, h: int, v: float, border: int = 1, **kwargs):
        self.draw_rect(x, y, w, h, DrawMode.WHITE, **kwargs)
        self.draw_rect(x + border, y + border, w - border * 2, h - border * 2, DrawMode.BLACK, **kwargs)
        self.draw_rect(x + border, y + border, math.floor((w - border * 2) * v), h - border * 2, DrawMode.WHITE,
                       **kwargs)

    def draw_circle(self, cx: int, cy: int, r: float, mode: DrawMode = DrawMode.WHITE, **kwargs):
        if r < 0:
            return

        for x in range(self.buffer.size[0]):
            for y in range(self.buffer.size[1]):
                if distance((cx, cy), (x, y)) < r:
                    self.set_pixel(x, y, mode, **kwargs)

    def set_pixel(self, x: int, y: int, v: DrawMode, **kwargs):
        bounds = kwargs.get('bounds') or (0, 0, *self.buffer.size)
        if x < bounds[0] or y < bounds[1] or x >= bounds[2] or y >= bounds[3]:
            return

        byte_index = (x + y * self.buffer.size[0]) // 8
        bit_index = 7 - (x % 8)

        if v == DrawMode.WHITE:
            self.buffer.buffer[byte_index] |= (1 << bit_index)
        elif v == DrawMode.BLACK:
            self.buffer.buffer[byte_index] &= ~(1 << bit_index)
        elif v == DrawMode.FLIP:
            self.buffer.buffer[byte_index] ^= (1 << bit_index)
