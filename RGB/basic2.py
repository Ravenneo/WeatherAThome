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

colorful_emoji = [
    [(255, 192, 203, "R"), (0, 0, 255, "R"), (255, 192, 203, "R"), (0, 0, 255, "R"), (255, 192, 203, "R")],
    [(0, 0, 255, "R"), (255, 192, 203, " "), (255, 192, 203, "R"), (255, 192, 203, " "), (0, 0, 255, "R")],
    [(255, 192, 203, "R"), (255, 192, 203, "R"), (0, 0, 255, "R"), (255, 192, 203, "R"), (255, 192, 203, "R")],
    [(255, 192, 203, " "), (255, 192, 203, "R"), (255, 192, 203, "R"), (255, 192, 203, "R"), (255, 192, 203, " ")],
    [(255, 192, 203, " "), (255, 192, 203, " "), (255, 192, 203, " "), (255, 192, 203, " "), (255, 192, 203, " ")],
]

emoji_loop = [colorful_emoji]

def draw_colorful_emoji(emoji):
    for y in range(5):
        for x in range(5):
            r, g, b, char = emoji[y][x]
            if char == "R":
                rgbmatrix5x5.set_pixel(x, y, r, g, b)
            else:
                rgbmatrix5x5.set_pixel(x, y, 0, 0, 0)
    rgbmatrix5x5.show()


while True:


    draw_colorful_emoji(colorful_emoji)
    time.sleep(1)

