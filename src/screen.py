from gamesense import GameSense


class OLEDScreen:
    def __init__(self, gs: GameSense, size: tuple[int, int]):
        self.gs = gs
        self.size = size

    async def init(self):
        await self.gs.bind_event('DISPLAY', handlers=[
            {
                "datas": [
                    {

                        "has-text": False,
                        "image-data": [0] * (self.size[0] * self.size[1] // 8)
                    }
                ],

                "device-type": f"screened-{self.size[0]}x{self.size[1]}",
                "mode": "screen",
                "zone": "one"
            }
        ])

    async def send(self, buffer: list[int]):
        data = {
            "value": next(self.gs.value_cycler),
            "frame": {
                f"image-data-{self.size[0]}x{self.size[1]}": buffer
            }
        }

        await self.gs.send_event("DISPLAY", data)
