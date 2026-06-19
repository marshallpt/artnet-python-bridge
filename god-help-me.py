import asyncio
from pyartnet import ArtNetNode

IP = '2.0.0.6'
UNIVERSE_LIST = [199, 200, 201, 205, 206, 207, 211, 212, 217]
# GRBW
COLOR = [0, 255, 255, 0]

async def main():

    async with ArtNetNode.create(IP, 6454) as node:

        for universe_id in UNIVERSE_LIST:
            
            print(f"UNIVERSE: {universe_id}")
            universe = node.add_universe(universe_id)
            channel = universe.add_channel(start=1, width=512)

            channel.add_fade(COLOR*128, 500)

            await channel

asyncio.run(main())
