# Mostly copy/pasted from:
# https://github.com/sciencegey/python_artnet/blob/main/samples/exampleReceiver.py

import time
import sys
from python_artnet import python_artnet as Artnet
from ring_helper import RGBW, IP, set_inner_ring, set_outer_ring
from pyartnet import ArtNetNode, Channel
import asyncio

debug = True

# What DMX channels we want to listen to
dmxChannels = [1,2,3,4,5,6,7,8]

### ArtNet Config ###
artnetBindIp = "0.0.0.0"
artnetUniverse = 3

### Art-Net Setup ###
# Sets debug in Art-Net module.
# Creates Artnet socket on the selected IP and Port
async def main():
    artNet = Artnet.Artnet(artnetBindIp, DEBUG=debug)
    inner = RGBW(0, 0, 0, 0)
    outer = RGBW(0, 0, 0, 0)
    while True:
        try:
            async with ArtNetNode.create(IP, 6454) as node:
                # First get the latest Art-Net data
                artNetBuffer = artNet.readBuffer()
                # And make sure we actually got something
                if artNetBuffer is not None:
                    # Get the packet from the buffer for the specific universe
                    artNetPacket = artNetBuffer[artnetUniverse]
                    # And make sure the packet has some data
                    if artNetPacket.data is not None:
                        # Stores the packet data array
                        dmxPacket = artNetPacket.data
                        
                        # Then print out the data from each channel
                        print("Received data: ", end="")
                        new_inner = RGBW(dmxPacket[0], dmxPacket[1], dmxPacket[2], dmxPacket[3])
                        new_outer = RGBW(dmxPacket[4], dmxPacket[5], dmxPacket[6], dmxPacket[7])
                        print(f"{new_inner=}{new_outer=}")
                        await set_outer_ring(node, new_outer, 1000)
                        await set_inner_ring(node, new_inner, 1000)
            time.sleep(0.01)
            
        except KeyboardInterrupt:
            break

    # Close the various connections cleanly so nothing explodes :)
    artNet.close()
    sys.exit()

asyncio.run(main())