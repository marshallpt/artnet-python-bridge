import asyncio
from pyartnet import ArtNetNode

IP = '2.0.0.6'
UNIVERSE_START = 199
UNIVERSE_END = 200

async def main():

    async with ArtNetNode.create(IP, 6454) as node:
         # Create universe 0
        universe = node.add_universe(199)

        # Add a channel to the universe which consists of 3 values
        # Default size of a value is 8Bit (0..255) so this would fill
        # the DMX values 1..3 of the universe
        for i in range(1, 512, 3):
            channel = universe.add_channel(start=i, width=3)

            # Fade channel to 255,0,0 in 5s
            # The fade will automatically run in the background
            channel.add_fade([255,255,0], 1000)

            # this can be used to wait till the fade is complete
            await channel

asyncio.run(main())
