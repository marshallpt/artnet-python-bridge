import asyncio
import threading
from pyartnet import ArtNetNode, Channel

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

async def main():
    async with ArtNetNode.create(IP, 6454) as node:
        await asyncio.gather(
            set_ring(node, INNER_UNIVERSE, OFF),
            set_ring(node, OUTER_UNIVERSE, OFF),
        )

asyncio.run(main())
