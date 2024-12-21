
"""
This example demonstrates how to setup extended collatz tree explorer program using
lothar module. Use WASD keys to move through the extended tree, press Q to exit.

"""

import os
import sys
import time
import keyboard
import lothar

# Run with parameters:
#   <initial number>
#   <view size>
#   <start row>
#   <start column>
#   <clear command (for Windows OS it's `cls`, for Linux usually `clear`)>

run = True
argument = int(sys.argv[1])
view_size = int(sys.argv[2])
anchor = [int(sys.argv[3]),int(sys.argv[4])]
ccmd = sys.argv[5]

os.system(ccmd)
while run:
    lothar.table(
        1,
        row_range=(anchor[0], anchor[0]+view_size-1),
        col_range=(anchor[1], anchor[1]+view_size-1),
        show=True,
        spacing=16,
        proc=lothar.default_proc
    )
    time.sleep(0.1)

    key = keyboard.read_key().lower()
    if   key == 'w':
        anchor[0] -= 1
    elif key == 's':
        anchor[0] += 1
    elif key == 'd':
        anchor[1] -= 1
    elif key == 'a':
        anchor[1] += 1
    elif key == 'q':
        run = False
    os.system(ccmd)

