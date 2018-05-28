#!/usr/bin/env python3

import random
import PIL
import PIL.Image
import PIL.ImageDraw
import sys

try:
    dest = sys.argv[1]
except:
    print('usage: %s path' % sys.argv[0])
    sys.exit()

width = 100
height = 100

img = PIL.Image.new('RGB', (width, height))

def fill_colour(img, colour):
    draw = PIL.ImageDraw.Draw(img)
    draw.rectangle((0, 0, img.width-1, img.height-1), colour)

def draw_checkers(img, colour):
    draw = PIL.ImageDraw.Draw(img)
    cols = rows = random.randint(5, 10)
    w = img.width / cols
    h = img.height / rows
    for r in range(rows):
        for c in range(cols):
            if (r+c) % 2 == 0:
                x = c*w
                y = r*h
                draw.rectangle((
                    int(x),
                    int(y),
                    int(x + w),
                    int(y + h)), colour)


colour = (
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255)
)
fill_colour(img, colour)

colour2 = (
    255-colour[0],
    255-colour[1],
    255-colour[2])
draw_checkers(img, colour2)

img.save(dest)
