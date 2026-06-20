import asyncio
from pyartnet import ArtNetNode, Channel
from dataclasses import dataclass
from typing import Tuple

@dataclass
class RGBW:
    """Data helper."""
    Red: int
    Green: int
    Blue: int
    White: int

    def to_GRBW(self) -> Tuple:
        return [self.Green, self.Red, self.Blue, self.White]

IP = '2.0.0.6'
ALL_UNIVERSES = [199, 200, 201, 205, 206, 207, 211, 212, 217, 218]
INNER_UNIVERSE = [211, 212, 217, 218]
OUTER_UNIVERSE = [199, 200, 201, 205, 206, 207]

# GRBW
WHITE = [0, 0, 0, 255]
ORANGE = [128, 255, 3, 0]
BLUE = [112, 5, 252, 0]
RED = [0, 255, 100, 0]
OFF = [0, 0, 0, 0]

async def set_color(channel: Channel, color, time: int):
    await channel.set_values(color*128)
    await channel

async def fade_color(channel: Channel, color, time: int):
    channel.set_fade(color*128, 1000)
    await channel

async def set_inner_ring(node: ArtNetNode, color: RGBW, time: int):
    await set_ring(node, INNER_UNIVERSE, color.to_GRBW(), time)

async def set_outer_ring(node: ArtNetNode, color: RGBW, time: int):
    await set_ring(node, OUTER_UNIVERSE, color.to_GRBW(), time)

async def set_ring(node: ArtNetNode, universe_list, color: RGBW, time: int):
    tasks = []
    
    for universe_id in universe_list:
        universe = node.add_universe(universe_id)
        channel = universe.add_channel(start=1, width=512)

        tasks.append(
            asyncio.create_task(set_color(channel=channel, color=color.to_GRBW(), time=time))
        )

    await asyncio.gather(*tasks)
