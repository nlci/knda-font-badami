#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)
print(f'posistion_subs.py for {ufo}')

# Modify UFO
layer = font.getLayer(font.defaultLayer.name)
for glyph in layer:
    for anchor in glyph.anchors:
        # print(f'{glyph.name} {anchor.name} x:{anchor.x} y:{anchor.y}')
        (xmin, ymin, xmax, ymax) = glyph.bounds
        if anchor.name == '_Sub':
            # Mark
            anchor.x = xmin
            anchor.y = 0
        if anchor.name == 'Sub':
            # Base
            # print(f'{glyph.name}: {xmin} {xmax}')
            anchor.x = xmax + 50
            anchor.y = -200

# Save UFO
font.changed()
font.save()
font.close()
