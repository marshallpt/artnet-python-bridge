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

# GRBW
WHITE = [0, 0, 0, 255]
ORANGE = [128, 255, 3, 0]
BLUE = [112, 5, 252, 0]
RED = [0, 255, 100, 0]
OFF = [0, 0, 0, 0]

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

# class RingHelper():
#     def __init__(self, node: ArtNetNode):
#         self.node = node

#     @classmethod
#     async def create(cls):
#         node = await ArtNetNode.create(IP, 6454)
#         return cls(node)

#     async def __aenter__(self):
#         return self

#     async def __aexit__(self, exc_type, exc, tb):
#         await self.node.close()
#         pass

#     async def run(self, color: RGBW):
#         await asyncio.gather(
#             set_ring(self.node, INNER_UNIVERSE, color.to_GRBW()),
#             set_ring(self.node, OUTER_UNIVERSE, color.to_GRBW()),
#         )
    
#     async def update_inner_ring(self, color: RGBW):
#         tasks = []
#         for universe_id in INNER_UNIVERSE:    
#             print(f"UNIVERSE: {universe_id}")
#             universe = self.node.add_universe(universe_id)
#             channel = universe.add_channel(start=1, width=512)

#             tasks.append(
#                 asyncio.create_task(set_color(channel=channel, color=color.to_GRBW()))
#             )
#         await asyncio.gather(*tasks)

async def main():
    async with ArtNetNode.create(IP, 6454) as node:
        await asyncio.gather(
            set_ring(node, INNER_UNIVERSE, ORANGE),
            set_ring(node, OUTER_UNIVERSE, BLUE),
        )

asyncio.run(main())
