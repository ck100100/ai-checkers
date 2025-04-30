LIST OF CHANGES

- Made a node.py file with each node object representing 1 board state
could be merged with board state.py in the future

- Made a replay viewer to review our bots' games without staring at arrays.
works with arrays of board sttates and not moves each turn, more inefficient, easier to work with

- Made a ddummy main to test our code.

I have detailed comments in each file. 

TODO (other than move forward w the project)

- Clean up some stuff noted with my coomments (constants, some code etc)

- Move main's methods in other files

- understand this way of writing functions:
def __init__(self, pawnType:type[PawnType], coordinates:Coordinates):

afta gia simera
GN


IF THE AI TRAINING IS NOT RUNNING BECAUSE OF A HIP ERROR TYPE THIS IN THE CONSOLE:

export HSA_OVERRIDE_GFX_VERSION=10.3.0  # Force gfx1030 compatibility
export HIP_VISIBLE_DEVICES=0  # Explicitly select GPU 0