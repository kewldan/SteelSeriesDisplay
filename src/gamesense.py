import itertools
import json
import os
from enum import Enum

import aiohttp


class Endpoints(str, Enum):
    REGISTER_GAME = '/game_metadata'
    REMOVE_GAME = '/remove_game'
    REGISTER_EVENT = '/register_game_event'
    BIND_EVENT = '/bind_game_event'
    REMOVE_EVENT = '/remove_game_event'
    SEND_EVENT = '/game_event'
    HEARTBEAT = '/game_heartbeat'


class GameSense():
    def __init__(self, game: str = None, game_display_name: str = None, developer=None,
                 deinitialize_timer_length_ms=None):
        self.game = game
        self.game_display_name = game_display_name or self.game
        self.developer = developer
        self.deinitialize_timer_length_ms = deinitialize_timer_length_ms
        self.ep = Endpoints
        self.value_cycler = itertools.cycle(range(1, 100))
        self.timeout = 1
        path = os.path.expandvars(
            r'%programdata%\SteelSeries\SteelSeries Engine 3\coreProps.json')
        self.hostname = 'http://' + json.load(open(path))['address']

    async def _post(self, endpoint: str, data: dict = None, uri: str | None = None) -> dict[str, ...]:
        url = self.hostname + endpoint
        if uri:
            url += uri
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as resp:
                return await resp.json()

    # game stuff
    async def register_game(self, game_name: str = None, reset=False):
        """
        Register the game with SteelSeries engine.\n
        `reset` True to remove the game before re-adding
        """
        if reset:
            await self.unregister_game()
        return await self._post(self.ep.REGISTER_GAME, {
            "game": game_name or self.game,
            "game_display_name": self.game_display_name,
            "developer": self.developer
        })

    async def unregister_game(self, game_name: str = None):
        """
        Unregisters the game with SteelSeries engine
        """
        return await self._post(self.ep.REMOVE_GAME, {
            "game": game_name or self.game
        })

    # event stuff
    async def bind_event(self, event_name: str, min_value=0, max_value=100, icon_id=None, handlers: list = None,
                   data_fields: list = None, game_name: str = None, full_data: dict = None):
        """
        Bind an event to this game
        """
        packet = full_data or {
            "game": game_name or self.game,
            "event": event_name,
            "min_value": min_value,
            "max_value": max_value,
            "icon_id": icon_id,
            "handlers": handlers or [],
            "data_fields": data_fields or []
        }
        return await self._post(self.ep.BIND_EVENT, packet)

    # def register_event(self):
    #     raise NotImplementedError

    async def remove_event(self, event_name: str, game_name: str = None):
        """
        Remove the given event from the game
        """
        return await self._post(self.ep.REMOVE_EVENT, {
            "game": game_name or self.game,
            "event": event_name
        })

    async def send_event(self, event_name: str, data: dict, game_name: str = None, full_data: dict = None):
        """
        Send an event to the engine
        """
        packet = full_data or {
            "game": game_name or self.game,
            "event": event_name,
            "data": data
        }
        return await self._post(self.ep.SEND_EVENT, packet)

    async def send_heartbeat(self, game_name: str = None):
        packet = {
            "game": game_name or self.game
        }
        return await self._post(self.ep.HEARTBEAT, packet)
