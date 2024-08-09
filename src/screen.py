from gamesense import GameSense


class OLEDScreen:
    def __init__(self, gs: GameSense, size: tuple[int, int]):
        self.gs = gs
        self.size = size
        self.buffer = [0] * (size[0] * size[1] // 8)

    async def init(self):
        await self.gs.bind_event('DISPLAY', handlers=[
            {
                "datas": [
                    {

                        "has-text": False,
                        "image-data": self.buffer
                    }
                ],

                "device-type": f"screened-{self.size[0]}x{self.size[1]}",
                "mode": "screen",
                "zone": "one"
            }
        ])

    async def release(self):
        data = {
            "value": next(self.gs.value_cycler),
            "frame": {
                f"image-data-{self.size[0]}x{self.size[1]}": self.buffer
            }
        }

        await self.gs.send_event("DISPLAY", data)
