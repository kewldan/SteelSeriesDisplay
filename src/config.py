import json
import os.path
from typing import Literal

from pydantic import BaseModel

ViewName = Literal['icon_less', 'with_icon']


class Config(BaseModel):
    width: int = 128
    height: int = 40
    transition: Literal['disabled', 'circle', 'slide'] = 'circle'
    refresh_rate: int = 10
    music_refresh_rate: int = 20
    events_duration: float = 1.
    text_speed: float = 6.
    row_gap: int = 6
    view: ViewName = 'with_icon'

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
