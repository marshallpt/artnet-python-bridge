import asyncio
from pyartnet import ArtNetNode, Channel
from dataclasses import dataclass
from typing import Tuple
from ring_helper import RGBW, ALL_UNIVERSES, IP, assign_fixtures, Fixture

# GRBW
WHITE = [0, 0, 0, 255]
ORANGE = [128, 255, 3, 0]
BLUE = [112, 5, 252, 0]
PINK = [0, 255, 100, 0]
OFF = [0, 0, 0, 0]

MAGENTA = RGBW(237, 4, 249, 0)
ORANGE = RGBW(100, 11, 0, 0)
GREEN = RGBW(14, 250, 2, 0)
YELLOW = RGBW(212, 249, 2, 0)
RED = RGBW(255, 0, 0, 0)
PURPLE = RGBW(134, 2, 249, 0)

TIME = 1000

async def main():
    async with ArtNetNode.create(IP, 6454) as node:
        entire_ring = Fixture(ALL_UNIVERSES, YELLOW)
        await asyncio.gather(
            assign_fixtures(node, [entire_ring], TIME)
        )

asyncio.run(main())
