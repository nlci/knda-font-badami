---
title: NLCI Kannada - Font Features
fontversion: 0.603
---

The NLCI Kannada fonts have some optional features that may be useful or required for particular uses or languages. This document lists all the available features.

These OpenType features are primarily specified using four-letter tags (e.g. 'ss20'). For more information on how to access OpenType features in specific environments and applications, see [Using Font Features](https://software.sil.org/fonts/features).

This page uses web fonts (WOFF2) to demonstrate font features and should display correctly in all modern browsers. For a more concise example of how to use the NLCI Kannada fonts as a web font see [Badami Webfont Example](../web/Badami-webfont-example.html). SIL has detailed information, see [Using SIL Fonts on Web Pages](https://software.sil.org/fonts/webfonts).

*If this document is not displaying correctly a PDF version is also provided in the documentation/pdf folder of the release package.*

## Complete feature list

### Stylistic sets

#### Kannada to Latin Digits <a id="ss19"></a>

<span class='affects'>Affects: U+0CE6 U+0CE7 U+0CE8 U+0CE9 U+0CEA U+0CEB U+0CEC U+0CED U+0CEE U+0CEF</span>

Feature | Sample | Feature setting
------- | ---------------------------- | -------
Default | <span class='badami-R normal'>೦ ೧ ೨ ೩ ೪ ೫ ೬ ೭ ೮ ೯</span> | `ss19=0`
Kannada to Latin Digits | <span class='badami-R normal' style='font-feature-settings: "ss19" 1'>೦ ೧ ೨ ೩ ೪ ೫ ೬ ೭ ೮ ೯</span> | `ss19=1`

#### Latin to Kannada Digits <a id="ss20"></a>

<span class='affects'>Affects: U+0030 U+0031 U+0032 U+0033 U+0034 U+0035 U+0036 U+0037 U+0038 U+0039</span>

Feature | Sample | Feature setting
------- | ---------------------------- | -------
Default | <span class='badami-R normal'>0 1 2 3 4 5 6 7 8 9</span> | `ss20=0`
Latin to Kannada Digits | <span class='badami-R normal' style='font-feature-settings: "ss20" 1'>0 1 2 3 4 5 6 7 8 9</span> | `ss20=1`
