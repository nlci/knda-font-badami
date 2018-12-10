#!/usr/bin/python3

from nameslist import *
from fontParts.world import *
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)
print(f'Add anchors for {ufo}')

# Modify UFO

# Akhands
akhand1 = ('ka_ssa', 'ka_ssa.base', 'ka_ssa.imathra')
akhand2 = ('ja_nya', 'ja_nya.base', 'ja_nya.imathra')
akhands = akhand1 + akhand2

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
    if (glyph.name.endswith('.sub') or
        glyph.name in ('ra.below', 'ra.below.large', 'ra.below.ra') + akhands):
        # Add anchors.
        glyph.appendAnchor('S', (xmax + 50, -200))
        if glyph.name.endswith('.sub'):
            glyph.appendAnchor('_S', (xmin, 0))

    # Position nuktas on bases
    if glyph.unicode in Vowels + Consonants or glyph.name in akhands:
        glyph.appendAnchor('N', (xcenter, ymin + noffset))

# Save UFO
font.changed()
font.save()
font.close()
