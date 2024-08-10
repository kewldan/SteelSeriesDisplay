class FrameBuffer:
    def __init__(self, size: tuple[int, int]):
        self.size = size
        self.buffer = [0] * (self.size[0] * self.size[1] // 8)

    def clear(self):
        for i in range(len(self.buffer)):
            self.buffer[i] = 0
