import asyncio
from pyartnet import ArtNetNode, Channel
from dataclasses import dataclass
from typing import Tuple
from ring_helper import RGBW, INNER_UNIVERSE, OUTER_UNIVERSE, IP, set_ring

# GRBW
WHITE = [0, 0, 0, 255]
ORANGE = [128, 255, 3, 0]
BLUE = [112, 5, 252, 0]
PINK = [0, 255, 100, 0]
OFF = [0, 0, 0, 0]

MAGENTA = RGBW(237, 4, 249, 0).to_GRBW()
ORANGE = RGBW(100, 11, 0, 0).to_GRBW()
GREEN = RGBW(14, 250, 2, 0).to_GRBW()
YELLOW = RGBW(212, 249, 2, 0).to_GRBW()
RED = RGBW(255, 0, 0, 0).to_GRBW()
PURPLE = RGBW(134, 2, 249, 0).to_GRBW()

TIME = 1000

async def main():
    async with ArtNetNode.create(IP, 6454) as node:
        await asyncio.gather(
            set_ring(node, INNER_UNIVERSE, BLUE, TIME),
            set_ring(node, OUTER_UNIVERSE, PURPLE, TIME),
        )

asyncio.run(main())
