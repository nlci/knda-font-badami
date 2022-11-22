#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO
vs = range(0xFE00, 0xFE0F+1)
for glyph in font:
    if glyph.unicode in vs: # or glyph.name.startswith('ra.below'):
        glyph.appendAnchor('_none', (0, 0))
    if '_' in glyph.name: # or glyph.name.startswith('ra.below'):
        for anchor in glyph.anchors:
            if anchor.name == '_M':
                glyph.removeAnchor(anchor)

    for anchor in glyph.anchors:
        if anchor.name == '_M':
            anchor.name = '_none'

# Save UFO
font.changed()
font.save()
font.close()
