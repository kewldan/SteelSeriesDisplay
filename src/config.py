import json
import os.path
from typing import Literal

from pydantic import BaseModel

ViewName = Literal['icon_less', 'with_icon']
Transition = Literal['disabled', 'circle', 'slide_x', 'slide_y', 'random']


class Config(BaseModel):
    width: int = 128
    height: int = 40
    transition: Transition = 'circle'
    transition_duration: float = 3.
    refresh_rate: int = 10
    music_refresh_rate: int = 20
    events_duration: float = 0.
    text_speed: float = 6.
    view: ViewName = 'with_icon'
    carousel_stop_time: float = 3.

    def __init__(self) -> None:
        if os.path.exists('config.json'):
            with open('config.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                super().__init__(**data)
        else:
            super().__init__()

        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.model_dump(), f, sort_keys=True, indent=4)


config = Config()
