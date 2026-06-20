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
artnetUniverse = 0

### Art-Net Setup ###
# Sets debug in Art-Net module.
# Creates Artnet socket on the selected IP and Port
async def main():
    artNet = Artnet.Artnet(artnetBindIp, DEBUG=debug)
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
                        sequenceNo = artNetPacket.sequence
                        
                        # Then print out the data from each channel
                        print("Received data: ", end="")
                        inner = RGBW(dmxPacket[0], dmxPacket[1], dmxPacket[2], dmxPacket[3])
                        outer = RGBW(dmxPacket[4], dmxPacket[5], dmxPacket[6], dmxPacket[7])
                        print(f"{inner=}{outer=}")
                        await asyncio.gather(
                            set_inner_ring(node, inner),
                            set_outer_ring(node, outer)
                        )
            time.sleep(0.1)
            
        except KeyboardInterrupt:
            break

    # Close the various connections cleanly so nothing explodes :)
    artNet.close()
    sys.exit()

asyncio.run(main())