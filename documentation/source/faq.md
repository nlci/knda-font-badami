---
title: NLCI Kannada - Frequently Asked Questions
fontversion: 0.603
---

### *How do I use the halant character as a vowel?*

The fonts have a blank and zero width glyph for U+25CC DOTTED CIRCLE.
This allows the character sequence of

- U+0CCD KANNADA SIGN VIRAMA
- U+0CD5 KANNADA LENGTH MARK

to display as desired for some languages.
[A better solution](https://github.com/n8willis/opentype-shaping-documents/issues/163),
which also works with these fonts, is to use the character sequence

- U+0CD5 KANNADA LENGTH MARK
- U+0CCD KANNADA SIGN VIRAMA

which works for a number of others fonts as well.
