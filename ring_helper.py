import asyncio
from pyartnet import ArtNetNode, Channel
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class RGBW:
    """Data helper."""
    Red: int
    Green: int
    Blue: int
    White: int

    def to_GRBW(self) -> Tuple:
        return [self.Green, self.Red, self.Blue, self.White]

@dataclass
class Fixture:
    Universes: List[int]
    Color: RGBW

IP = '2.0.0.6'
ALL_UNIVERSES = [199, 200, 201, 205, 206, 207, 211, 212, 217, 218]
INNER_UNIVERSE = [211, 212, 217, 218]
OUTER_UNIVERSE = [199, 200, 201, 205, 206, 207]

A_INNER = [199, 200, 201]
A_OUTER = [205, 206, 207]
B_INNER = [211, 212]
B_OUTER = [217, 218]

async def set_color(channel: Channel, color):
    await channel.set_values(color*128)
    await channel

async def fade_color(channel: Channel, color, time: int):
    channel.set_fade(color*128, 1000)
    await channel

async def assign_fixture(node: ArtNetNode, fixtures: List[Fixture], time: int=0):
    tasks = []
    
    for fixture in fixtures:
        for universe_id in fixture.Universes:
            universe = node.add_universe(universe_id)
            channel = universe.add_channel(start=1, width=512)

            if time == 0:
                tasks.append(
                    asyncio.create_task(set_color(channel=channel, color=fixture.Color.to_GRBW()))
                )
            else:
                tasks.append(
                    asyncio.create_task(fade_color(channel=channel, color=fixture.Color.to_GRBW(), time=time))
                )

    await asyncio.gather(*tasks)
