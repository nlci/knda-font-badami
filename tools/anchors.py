#!/usr/bin/python3

from nameslist import *
from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)
print(f'Add anchors for {ufo}')

# Modify UFO

# Position nukta marks
glyph = font['nukta']
(a_xmin, a_ymin, a_xmax, a_ymax) = glyph[2].bounds
(b_xmin, b_ymin, b_xmax, b_ymax) = glyph[3].bounds
xcenter = (a_xmin + b_xmax) / 2
noffset = (a_ymin + b_ymax) / 2
glyph.appendAnchor('_N', (xcenter, noffset))

glyph = font['nukta.alt']
(a_xmin, a_ymin, a_xmax, a_ymax) = glyph[2].bounds
xcenter = (a_xmin + a_xmax) / 2
ycenter = (a_ymin + a_ymax) / 2
glyph.appendAnchor('_N', (xcenter, ycenter))

# Position ematra...

# Badami has two stray contours on the virama glyph.
# As a result, the bounding box values for this glyph are not useful.
# We will use bounding box of the first (good) contour,
# and ignore the other contours. They can be removed later.
#ematra = font['ematra']
#if font.info.familyName == 'Badami':
#    (xmin, ymin, xmax, ymax) = ematra[0].bounds  # box of first contour
#else:
#    (xmin, ymin, xmax, ymax) = ematra.bounds

#ematra.appendAnchor('_V', (xmax, ymin))

for glyph in font:
    bounds = glyph.bounds
    if bounds is None:
        continue
    (xmin, ymin, xmax, ymax) = bounds
    xcenter = (xmin + xmax) / 2

    # ...on some consonants.
    #if glyph.name in ('jha.base', 'ma.base', 'ya.base'):
    #    glyph.appendAnchor('V', (xcenter, ymax + 50))

    # Position sub sub forms
    if glyph.name.endswith('.sub') or glyph.name in ('ra.below', 'ra.below.large', 'ra.below.ra'):
        glyph.appendAnchor('S', (xmax + 50, -200))
        if glyph.name.endswith('.sub'):
            glyph.appendAnchor('_S', (xmin, 0))

    # Position nuktas on bases
    if glyph.unicode in Vowels + Consonants:
        glyph.appendAnchor('N', (xcenter, ymin + noffset))

    # Akhands
    if glyph.name == 'ka':
        glyph.appendAnchor('K', (xcenter, 0))
    if glyph.name == 'ja':
        glyph.appendAnchor('J', (xcenter, 0))
    if glyph.name == 'ssa.sub':
        glyph.appendAnchor('_K', (xcenter, 0))
    if glyph.name == 'nya.sub':
        glyph.appendAnchor('_J', (xcenter, 0))

# Save UFO
font.changed()
font.save()
font.close()
