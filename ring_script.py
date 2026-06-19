import asyncio
from pyartnet import ArtNetNode, Channel
from dataclasses import dataclass
from typing import Tuple
from ring_helper import RGBW, INNER_UNIVERSE, OUTER_UNIVERSE, IP

# GRBW
WHITE = [0, 0, 0, 255]
ORANGE = [128, 255, 3, 0]
BLUE = [112, 5, 252, 0]
RED = [0, 255, 100, 0]
OFF = [0, 0, 0, 0]

MAGENTA = RGBW(100, 28, 1, 0).to_GRBW()
ORANGE = RGBW(100, 11, 0, 0).to_GRBW()

async def set_color(channel: Channel, color):
    channel.add_fade(color*128, 1000)
    await channel

async def set_ring(node: ArtNetNode, universe_list, color):
    tasks = []
    
    for universe_id in universe_list:    
        print(f"UNIVERSE: {universe_id}")
        universe = node.add_universe(universe_id)
        channel = universe.add_channel(start=1, width=512)

        tasks.append(
            asyncio.create_task(set_color(channel=channel, color=color))
        )

    await asyncio.gather(*tasks)

async def main():
    async with ArtNetNode.create(IP, 6454) as node:
        await asyncio.gather(
            set_ring(node, INNER_UNIVERSE, MAGENTA),
            set_ring(node, OUTER_UNIVERSE, ORANGE),
        )

asyncio.run(main())
