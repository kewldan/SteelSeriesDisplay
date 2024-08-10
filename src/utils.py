import math


def format_seconds(seconds: float) -> str:
    seconds = math.floor(seconds)
    return f'{seconds // 60:02}:{seconds % 60:02}'
