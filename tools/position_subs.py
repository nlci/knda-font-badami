#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO

# Make sure we only have one layer
# for layer in font.layers:
#     print(layer.name)

# Show the default layer
# print(font.defaultLayer.name)

layer = font.getLayer(font.defaultLayer.name)
for glyph in layer:
    for anchor in glyph.anchors:
        # print('{} {} x:{} y:{}'.format(glyph.name, anchor.name, anchor.x, anchor.y))
        if anchor.name == '_Sub':
            # Mark
            anchor.x = -600
            anchor.y = -300
        if anchor.name == 'Sub':
            # Base
            anchor.x = 600
            anchor.y = -600

# Save UFO
font.changed()
font.save()
font.close()
