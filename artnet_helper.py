import asyncio
from pyartnet import ArtNetNode, Channel
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class RGBW:
    """Color helper."""
    Red: int
    Green: int
    Blue: int
    White: int

    def to_GRBW(self) -> Tuple:
        return [self.Green, self.Red, self.Blue, self.White]

@dataclass
class Fixture:
    """List of universes and a color to assign them."""
    Universes: List[int]
    Color: RGBW

async def set_color(channel: Channel, color):
    await channel.set_values(color*128)

async def fade_color(channel: Channel, color, time: int):
    channel.set_fade(color*128, 1000)
    await channel

async def assign_fixtures(node: ArtNetNode, fixtures: List[Fixture], time: int=0):
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
