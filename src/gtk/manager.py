import math
import time
from enum import Enum
from typing import Callable

from screen import OLEDScreen
from .alphabet import bitmap_font


class DrawMode(Enum):
    WHITE = 0
    BLACK = 1
    FLIP = 2


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_text_width(text: str) -> int:
    return len(text) * 8


class BasicGTK:
    def __init__(self, screen: OLEDScreen):
        self.screen = screen

    async def __aenter__(self) -> "BasicGTK":
        self.clear()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.screen.release()

    def clear(self):
        for i in range(len(self.screen.buffer)):
            self.screen.buffer[i] = 0

    def draw_callable(self, x: int, y: int, w: int, h: int, get_pixel: Callable[[int, int], bool],
                      mode: DrawMode = DrawMode.WHITE):
        for i in range(w):
            for j in range(h):
                if get_pixel(i, j):
                    self.set_pixel(x + i, y + j, mode)

    def draw_rect(self, x: int, y: int, w: int, h: int, v: DrawMode = DrawMode.WHITE):
        self.draw_callable(x, y, w, h, lambda _, _0: True, v)

    def draw_bitmap(self, x: int, y: int, w: int, h: int, bitmap: list[int], mode: DrawMode = DrawMode.WHITE):
        self.draw_callable(x, y, w, h, lambda i, j: bool(bitmap[(i + j * w) // 8] & (1 << (7 - (i % 8)))), mode)

    def draw_text(self, x: int, y: int, text: str, mode: DrawMode = DrawMode.WHITE):
        margin = 0

        for letter in text.upper():
            bitmap = bitmap_font.get(letter)
            if bitmap:
                self.draw_bitmap(x + margin, y, 8, 7, bitmap, mode)
            margin += 8

    def draw_center_text(self, y: int, text: str, mode: DrawMode = DrawMode.WHITE):
        width = get_text_width(text)

        x = (self.screen.size[0] - width) // 2

        self.draw_text(x, y, text, mode)

    def draw_big_text(self, y: int, text: str, speed: float = 1.):
        width = get_text_width(text)
        if width > self.screen.size[0] * .9:
            text = text + '   '
            width = get_text_width(text)
            self.draw_text(-(math.floor(time.time() * speed) % width), y, text * 2)
        else:
            self.draw_center_text(y, text)

    def draw_progress(self, x: int, y: int, w: int, h: int, v: float, border: int = 1):
        self.draw_rect(x, y, w, h, DrawMode.WHITE)
        self.draw_rect(x + border, y + border, w - border * 2, h - border * 2, DrawMode.BLACK)
        self.draw_rect(x + border, y + border, math.floor((w - border * 2) * v), h - border * 2, DrawMode.WHITE)

    def draw_circle(self, cx: int, cy: int, r: float, mode: DrawMode = DrawMode.WHITE):
        if r < 0:
            return

        for x in range(self.screen.size[0]):
            for y in range(self.screen.size[1]):
                if distance((cx, cy), (x, y)) < r:
                    self.set_pixel(x, y, mode)

    def set_pixel(self, x: int, y: int, v: DrawMode):
        if x < 0 or y < 0 or x >= self.screen.size[0] or y >= self.screen.size[1]:
            return

        byte_index = (x + y * self.screen.size[0]) // 8
        bit_index = 7 - (x % 8)

        if v == DrawMode.WHITE:
            self.screen.buffer[byte_index] |= (1 << bit_index)
        elif v == DrawMode.BLACK:
            self.screen.buffer[byte_index] &= ~(1 << bit_index)
        elif v == DrawMode.FLIP:
            self.screen.buffer[byte_index] ^= (1 << bit_index)
