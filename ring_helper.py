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
ALL_UNIVERSES = [199, 200, 201, 205, 206, 207, 211, 212, 217]
INNER_UNIVERSE = [211, 212, 217]
OUTER_UNIVERSE = [199, 200, 201, 205, 206, 207]

A_INNER = [199, 200, 201]
A_OUTER = [205, 206, 207]
B_INNER = [211, 212]
B_OUTER = [217]

# GRBW
WHITE = [0, 0, 0, 255]
ORANGE = [128, 255, 3, 0]
BLUE = [112, 5, 252, 0]
RED = [0, 255, 100, 0]
OFF = [0, 0, 0, 0]

async def set_color(channel: Channel, color):
    await channel.set_values(color*128)
    await channel

async def set_b_ring(node: ArtNetNode, inner_color: RGBW, outer_color: RGBW):
    await asyncio.gather(
        set_ring(node, B_INNER, inner_color.to_GRBW()),
        set_ring(node, B_OUTER, outer_color.to_GRBW())
    )

async def set_a_ring(node: ArtNetNode, inner_color: RGBW, outer_color: RGBW):
    await asyncio.gather(
        set_ring(node, A_INNER, inner_color.to_GRBW()),
        set_ring(node, A_OUTER, outer_color.to_GRBW())
    )

async def set_ring(node: ArtNetNode, universe_list, color):
    tasks = []
    
    for universe_id in universe_list:
        universe = node.add_universe(universe_id)
        channel = universe.add_channel(start=1, width=512)

        tasks.append(
            asyncio.create_task(set_color(channel=channel, color=color))
        )

    await asyncio.gather(*tasks)
