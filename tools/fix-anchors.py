#!/usr/bin/python3

from fontParts.world import *
from palaso.unicode.ucd import get_ucd
import sys

# Open UFO
ufo = sys.argv[1]
font = OpenFont(ufo)

# Modify UFO

# Adjust existing anchors
vs = range(0xFE00, 0xFE0F+1)
for glyph in font:
    continue
    if glyph.unicode in vs: # or glyph.name.startswith('ra.below'):
        glyph.appendAnchor('_none', (0, 0))
    if '_' in glyph.name: # or glyph.name.startswith('ra.below'):
        for anchor in glyph.anchors:
            if anchor.name == '_M':
                glyph.removeAnchor(anchor)

    for anchor in glyph.anchors:
        if anchor.name == '_M':
            anchor.name = '_none'

# Position nukta marks
nuktas = ('nukta', 'nukta.alt')
vedic_dots = ('vedictonetwodotsbelow', 'vedictonedotbelow')
for nukta, vedic_dot in zip(nuktas, vedic_dots):
    vg = font[vedic_dot]
    (xmin, ymin, xmax, ymax) = vg.bounds
    xcenter = (xmin + xmax) / 2
    # The nukta glyphs are references
    # so the calculations were done on the source glyphs.
    ng = font[nukta]
    ng.clearAnchors()
    ng.appendAnchor('_N', (xcenter, ymax))

# Position extra marks
above_marks = ('udatta', 'gravedeva', 'acutedeva', 'doublesvarita', 'vedictonekathakaanudatta', 'candrabindu')
below_marks = ('anudatta', 'vedictonedotbelow', 'vedictonetwodotsbelow', 'vedictonethreedotsbelow')
for glyph_name in above_marks + below_marks:
    glyph = font[glyph_name]
    (xmin, ymin, xmax, ymax) = glyph.bounds
    xcenter = (xmin + xmax) / 2
    glyph.width = 0
    if glyph.name in above_marks:
        glyph.appendAnchor('_C', (xcenter, ymin))
    if glyph.name in below_marks:
        glyph.appendAnchor('_N', (xcenter, ymax))

akhands = ('ka_ssa', 'ja_nya')

ka_base = font['ka.base']
(xmin, ymin, xmax, ymax) = ka_base.bounds
top = ymax

for glyph in font:
    # Remove exisiting N anchors
    for anchor in glyph.anchors:
        if anchor.name == 'N':
            glyph.removeAnchor(anchor)

for glyph in font:
        bounds = glyph.bounds
        if bounds is None:
            continue
        (xmin, ymin, xmax, ymax) = bounds
        xcenter = (xmin + xmax) / 2

        # Position nuktas on sub forms
        if (glyph.name.endswith('.sub') or
            glyph.name in ('ra.below', 'ra.below.large', 'ra.below.ra') + akhands):
            # Add anchors.
            glyph.appendAnchor('N', (xcenter, -271))

        # Position nuktas on base forms
        character_name = ''
        if glyph.unicode:
            character_name = get_ucd(glyph.unicode, 'na')
        if character_name.startswith('KANNADA LETTER'):
            glyph.appendAnchor('C', (100, top + 70))

            # Some consonants have a teardrop shape below the baseline
            # These consonants need to have the nukta positioned lower
            teardrop = 0
            if ymin < -100:
                teardrop = 140
            glyph.appendAnchor('N', (xcenter, -71 - teardrop))

for glyph in font:
        # Position nuktas on base ligatures
        if '_' in glyph.name:
            if glyph.name in akhands or glyph.name.startswith('_'):
                continue
            # Use the location of the nukta on the base glyph (such as ka)
            # for the ligature (such as ka_virama)
            base_glyph_name = glyph.name.split('_')[0]
            base_glyph = font[base_glyph_name]
            for anchor in base_glyph.anchors:
                if anchor.name in ('C', 'N'):
                    glyph.appendAnchor(anchor.name, (anchor.x, anchor.y))

# Save UFO
font.changed()
font.save()
font.close()
