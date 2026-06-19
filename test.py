from ring_helper import RingHelper, RGBW

import asyncio


async def main():
    async with await RingHelper.create() as controller:
        print(controller.node)
        await controller.run(color=RGBW(255, 0, 0, 0))

asyncio.run(main())

