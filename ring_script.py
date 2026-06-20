import asyncio
from pyartnet import ArtNetNode
from ring_helper import (
    ALL_UNIVERSES, 
    OUTER_UNIVERSE,
    A_INNER,
    A_OUTER,
    B_INNER,
    B_OUTER,
    RING_CONTROLLER_IP
)
from artnet_helper import RGBW, Fixture, assign_fixtures

MAGENTA = RGBW(237, 4, 249, 0)
CYAN = RGBW(0, 200, 255, 0)
BLUE = RGBW(0, 0, 255, 0)
ORANGE = RGBW(100, 11, 0, 0)
GREEN = RGBW(14, 250, 2, 0)
YELLOW = RGBW(212, 249, 2, 0)
RED = RGBW(255, 0, 0, 0)
PURPLE = RGBW(134, 2, 249, 0)

TIME = 1000

async def main():
    async with ArtNetNode.create(RING_CONTROLLER_IP, 6454) as node:
        
        fixtures = [
            Fixture(A_INNER, MAGENTA),
            Fixture(A_OUTER, CYAN),
            Fixture(B_INNER, PURPLE),
            Fixture(B_OUTER, BLUE),
        ]
        
        await asyncio.gather(
            assign_fixtures(node, fixtures, TIME)
        )

asyncio.run(main())
