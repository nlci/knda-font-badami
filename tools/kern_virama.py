#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)
print(f'Kern virama in {ufo}')

# Modify UFO
kern = int(sys.argv[2])
virama = font['virama']
# virama.leftMargin += kern
for contour in virama.contours:
    for point in contour.points:
        if point.x < 0:
            print(f'adjusting point at {point.x}, {point.y}')
            point.x -= kern

# for glyph in font:
#     if glyph.name.endswith('.base'):
#         print(f'{glyph.name}, {glyph.width}')

# Save UFO
font.changed()
font.save()
font.close()
