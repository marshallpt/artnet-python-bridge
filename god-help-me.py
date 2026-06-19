import asyncio
import threading
from pyartnet import ArtNetNode

IP = '2.0.0.6'
UNIVERSE_LIST = [199, 200, 201, 205, 206, 207, 211, 212, 217]
# GRBW
ORANGE = [128, 255, 3, 0]
BLUE = [112, 5, 252, 0]
RED = [0, 255, 100, 0]

async def set_color(channel, color):
    channel.add_fade(color*128, 1000)
    await channel

async def main():

    async with ArtNetNode.create(IP, 6454) as node:

        for universe_id in UNIVERSE_LIST:
            
            print(f"UNIVERSE: {universe_id}")
            universe = node.add_universe(universe_id)
            channel = universe.add_channel(start=1, width=512)

            await set_color(channel=channel, color=BLUE)

asyncio.run(main())
