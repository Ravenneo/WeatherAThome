#!/usr/bin/env python

import time

from rgbmatrix5x5 import RGBMatrix5x5

print("""
RGBMatrix5x5 - Emoji Loop Demo
Displays a loop of emojis on the 5x5 LED matrix.
Press Ctrl+C to exit!
""")

rgbmatrix5x5 = RGBMatrix5x5()

rgbmatrix5x5.set_clear_on_exit()
rgbmatrix5x5.set_brightness(0.8)

# Define emoji pixel art designs

otro = ["RR   ",
        "RRR  ",
        " RRR ",
        "RRR  ",
        "RR   ",
]
emoji_loop = [otro]

def draw_emoji(emoji, r, g, b):
    for y in range(5):
        for x in range(5):
            if emoji[y][x] == "R":
                rgbmatrix5x5.set_pixel(x, y, r, g, b)
            else:
                rgbmatrix5x5.set_pixel(x, y, 0, 0, 0)
    rgbmatrix5x5.show()


while True:


    # Green heart
    draw_emoji(otro, 0, 255, 0)
    time.sleep(1)
