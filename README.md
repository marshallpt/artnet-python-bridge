# Art-Net Python Bridge
Art-Net publisher / subscriber node to expose a 10-universe GRBW
LED strip fixture as four RGBW fixtures to be controlled in grandMA3.

## How
This would not have been possible without the following Pyton libraries:
- [pyartnet](https://pypi.org/project/pyartnet/): for publishing Art-Net data
- [python-artnet](https://pypi.org/project/python-artnet/) (and its example code): for subscribing / polling Art-Net data

Massive shoutout to the mainainers of these libraries.

## What
- **artnet_helper.py**:
    - RGBW helper class because GRBW is unintuitive
    - Helper methods for assigning an RGBW color value to an arbitrary number of Art-Net universes simulatenously
- **ring_helper.py**:
    - Constants for the ring fixture
- **ring_script.py**:
    - Set color values for the ring once
- **ring_artnet_bridge.py**:
    - Continuously poll the first 16 channels of an Art-Net universe and set those values to the ring

## Why
Had an upcoming show with this ring fixture installed and no way
to communicate with it. The long-term plan is to use pixel mapping software
(Madrix) to control it, but we didn't have the time to configure it, and the
LD wanted to be able to control the color (alongside every other fixture)
with grandMA3, and we ran up against fixture count limitations when trying
to communicate with it directly..

Am happy to report this script worked flawlessly for the show. The only issue
we ran into was I used the world's worst patch cable and my laptop got 
disconnected from the switch briefly, but once that was corrected, the ring
immediately resumed responding to commands.

## Usage
### Preparation
1. Clone the repo
1. Create a virtual environment and install the dependencies in `requirements.txt`
1. Create a helper class for your fixture in the style of **ring_helper.py**. What you'll need is:
    1. IP address for the Art-Net node where it lives
    1. `List[int]` of universes it uses
    

> [!NOTE]
> Because I wrote this for a GRBW fixture, that's what all the assignment
> commands in **artnet_helper.py** assume the desired output is. To change
> this, make your own getter in the `RGBW` object in the style of
> `to_GRBW()` and replace all the references to that method.

### One-off command
This is useful for identifying what universes are being used by a fixture,
troubleshooting, or setting-and-forgetting something.

1. Prepare **ring_script.py**:
    1. Import your IP address and universe list from your fixture helper class
    1. Replace `RING_CONTROLLER_IP` with the IP address imported in the previous step
    1. Create an `RGBW` object of the color you want to use (or use one of the pre-defined ones)
    1. Create a list of one or multiple `Fixture`s with the colors you've made and universes you've imported
    1. Update the call to `assign_fixtures()` with the list of `Fixture`s made in the previous step
1. Run **ring_script.py** in your activated terminal

### Bridge
For mapping multiple universes to a manageable set of fixtures.

1. Prepare **ring_artnet_bridge.py**:
    1. Import your universe list from your fixture helper class
    1. Replace `artnetListenUniverse` with the universe # you want to subscribe to / want your light software to publish to
    1. Update the universes being used in the `Fixture`s in the while loop with the ones from your import class
    1. Update DMX mapping to taste
1. Run **ring_artnet_bridge.py** in your activated terminal

> [!NOTE]
> When I started writing this I didn't think the performance would
> be up to par for smooth animations, but I had no issues running
> the bridge seen/described here on an i7-8750H (6-core, 12 thread)
> Dell XPS from 2018. The refresh rate was extremely smooth and 
> it looked like it was being controlled natively from grandMA3.