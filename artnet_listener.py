import time
import sys
from python_artnet import python_artnet as Artnet
from ring_helper import RGBW, IP, set_b_ring, set_a_ring
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
                        a_inner = RGBW(dmxPacket[0], dmxPacket[1], dmxPacket[2], dmxPacket[3])
                        a_outer = RGBW(dmxPacket[4], dmxPacket[5], dmxPacket[6], dmxPacket[7])
                        b_inner = RGBW(dmxPacket[8], dmxPacket[9], dmxPacket[10], dmxPacket[11])
                        b_outer = RGBW(dmxPacket[12], dmxPacket[13], dmxPacket[14], dmxPacket[15])
                        print(f"{a_inner=}{a_outer=}{b_inner=}{b_outer=}")
                        await set_a_ring(node, a_inner, a_outer)
                        await set_b_ring(node, b_inner, b_outer)
            time.sleep(0.01)
            
        except KeyboardInterrupt:
            break

    # Close the various connections cleanly so nothing explodes :)
    artNet.close()
    sys.exit()

asyncio.run(main())