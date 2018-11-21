#!/usr/bin/python3

from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)
print(f'Add anchors for {ufo}')

# Modify UFO
layer = font.getLayer(font.defaultLayer.name)

# Position ematra...

# Badami has two stray contours on the virama glyph.
# As a result, the bounding box values for this glyph are not useful.
# We will use bounding box of the first (good) contour,
# and ignore the other contours. They can be removed later.
ematra = font['ematra']
if font.info.familyName == 'Badami':
    (xmin, ymin, xmax, ymax) = ematra[0].bounds  # box of first contour
else:
    (xmin, ymin, xmax, ymax) = ematra.bounds

ematra.appendAnchor('_V', (xmin, ymin))

for glyph in layer:

    # ...on some consonants.
    if glyph.name in ('jha.base', 'ma.base', 'ya.base'):
        (xmin, ymin, xmax, ymax) = glyph.bounds
        xcenter = (xmin + xmax) / 2
        anchor = glyph.appendAnchor('V', (xcenter, ymax))

    # Position sub sub forms
    if glyph.name.endswith('.sub') or glyph.name in ('ra.below', 'ra.below.large', 'ra.below.ra'):
        (xmin, ymin, xmax, ymax) = glyph.bounds
        anchor = glyph.appendAnchor('Sub', (xmax + 50, -200))
        if glyph.name.endswith('.sub'):
            anchor = glyph.appendAnchor('_Sub', (xmin, 0))

# Save UFO
font.changed()
font.save()
font.close()
