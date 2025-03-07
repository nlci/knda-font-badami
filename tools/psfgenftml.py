#!/usr/bin/python3
__doc__ = '''generate ftml tests from glyph_data.csv and UFO'''
__url__ = 'https://github.com/silnrsi/pysilfont'
__copyright__ = 'Copyright (c) 2018-2022 SIL International  (https://www.sil.org)'
__license__ = 'Released under the MIT License (https://opensource.org/licenses/MIT)'
__author__ = 'Bob Hallissy'

import re
from silfont.core import execute
import silfont.ftml_builder as FB
from palaso.unicode.ucd import get_ucd

argspec = [
    ('ifont', {'help': 'Input UFO'}, {'type': 'infont'}),
    ('output', {'help': 'Output file ftml in XML format', 'nargs': '?'}, {'type': 'outfile', 'def': '_out.ftml'}),
    ('-i','--input', {'help': 'Glyph info csv file'}, {'type': 'incsv', 'def': 'glyph_data.csv'}),
    ('-f','--fontcode', {'help': 'letter to filter for glyph_data'},{}),
    ('--prevfont', {'help': 'font file of previous version'}, {'type': 'filename', 'def': None}),
    ('-l','--log', {'help': 'Set log file name'}, {'type': 'outfile', 'def': '_ftml.log'}),
    ('--langs', {'help':'List of bcp47 language tags', 'default': None}, {}),
    ('--rtl', {'help': 'enable right-to-left features', 'action': 'store_true'}, {}),
    ('--norendercheck', {'help': 'do not include the RenderingUnknown check', 'action': 'store_true'}, {}),
    ('-t', '--test', {'help': 'name of the test to generate', 'default': None}, {}),
    ('-s','--fontsrc', {'help': 'font source: "url()" or "local()" optionally followed by "=label"', 'action': 'append'}, {}),
    ('--scale', {'help': 'percentage to scale rendered text (default 100)'}, {}),
    ('--ap', {'help': 'regular expression describing APs to examine', 'default': '.'}, {}),
    ('-w', '--width', {'help': 'total width of all <string> column (default automatic)'}, {}),
    ('--xsl', {'help': 'XSL stylesheet to use'}, {}),
]

ageToFlag = 14.0
ageColor = '#FFC8A0'      # light orange -- marks if there is a char from above Unicode version or later
missingColor = '#FFE0E0'  # light red -- mark if a char is missing from UFO
newColor = '#F0FFF0'      # light green -- mark if char is not in previous version (if --prevFont supplied)
backgroundLegend = f'Background colors: light orange: includes a character from Unicode version {ageToFlag} or later; ' + \
                   'light red: a character is missing from UFO; ' \
                   'light green: a character is new in this version of the font'

def doit(args):
    logger = args.logger

    # Read input csv
    builder = FB.FTMLBuilder(logger, incsv=args.input, fontcode=args.fontcode, font=args.ifont, ap=args.ap,
                             rtlenable=args.rtl, langs=args.langs)

    # Override default base (25CC) for displaying combining marks:
    builder.diacBase = 0x0C95   # ka
    dotted_circle = 0x25CC

    # Specify blocks of primary and secondary scripts
    block = range(0x0CB0, 0x0CFF+1)

    # Useful ranges of codepoints
    uids = sorted(builder.uids())
    vowels = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Vowel_Independent']
    consonants = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Consonant']
    nukta = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Nukta'][0]
    matras = [uid for uid in uids if 'VOWEL SIGN' in get_ucd(uid, 'na')]
    virama = [uid for uid in uids if get_ucd(uid, 'InSC') == 'Virama'][0]
    digits = [uid for uid in uids if builder.char(uid).general == 'Nd' and uid in block]
    punct = [uid for uid in uids if get_ucd(uid, 'gc').startswith('P')]

    ka = consonants[0]
    ga = consonants[2]
    gha = consonants[3]
    ja = consonants[7]
    nya = consonants[9]
    ssa = consonants[32]
    matra_like = matras + [virama]
    wrap_matras = [0x0CC3, 0x0CC4, 0x0CC8]
    ka_ssa = (ka,virama,ssa)
    ja_nya = (ja,virama,nya)
    akhands = [ka_ssa, ja_nya]
    nine = digits[-1]

    # Initialize FTML document:
    # Default name for test: AllChars or something based on the csvdata file:
    test = args.test or 'AllChars (NG)'
    widths = None
    if args.width:
        try:
            width, units = re.match(r'(\d+)(.*)$', args.width).groups()
            if len(args.fontsrc):
                width = int(round(int(width)/len(args.fontsrc)))
            widths = {'string': f'{width}{units}'}
            logger.log(f'width: {args.width} --> {widths["string"]}', 'I')
        except:
            logger.log(f'Unable to parse width argument "{args.width}"', 'W')
    # split labels from fontsource parameter
    fontsrc = []
    labels = []
    for sl in args.fontsrc:
        try:
            s, l = sl.split('=',1)
            fontsrc.append(s)
            labels.append(l)
        except ValueError:
            fontsrc.append(sl)
            labels.append(None)
    ftml = FB.FTML(test, logger, comment=backgroundLegend, rendercheck=not args.norendercheck, fontscale=args.scale,
                   widths=widths, xslfn=args.xsl, fontsrc=fontsrc, fontlabel=labels, defaultrtl=args.rtl)

    if args.prevfont is not None:
        try:
            from fontTools.ttLib import TTFont
            font = TTFont(args.prevfont)
            prevCmap = font.getBestCmap()
        except:
            logger.log(f'Unable to open previous font {args.prevfont}', 'S')


    def setBackgroundColor(uids):
        # if any uid in uids is missing from the UFO, set test background color to missingColor
        if any(uid in builder.uidsMissingFromUFO for uid in uids):
            ftml.setBackground(missingColor)
        # else if any uid in uids has Unicode age >= ageToFlag, then set the test background color to ageColor
        elif max(map(lambda x: float(get_ucd(x, 'age')), uids)) >= ageToFlag:
            ftml.setBackground(ageColor)
        elif args.prevfont and any(uid not in prevCmap for uid in uids):
            ftml.setBackground(newColor)

    if test.lower().startswith("allchars"):
        # all chars that should be in the font:
        ftml.startTestGroup('Encoded characters')
        for uid in uids:
            if uid < 32: continue
            c = builder.char(uid)
            setBackgroundColor((uid,))
            for featlist in builder.permuteFeatures(uids=(uid,)):
                ftml.setFeatures(featlist)
                builder.render((uid,), ftml)
                # Don't close test -- collect consecutive encoded chars in a single row
            ftml.clearFeatures()
            if len(c.langs):
                for langID in builder.allLangs:
                    ftml.setLang(langID)
                    builder.render((uid,), ftml)
                ftml.clearLang()
            ftml.clearBackground()

        # Add unencoded specials and ligatures -- i.e., things with a sequence of USVs in the glyph_data:
        ftml.startTestGroup('Specials & ligatures from glyph_data')
        for basename in builder.specials():
            special = builder.special(basename)
            setBackgroundColor(special.uids)
            for featlist in builder.permuteFeatures(uids=special.uids, feats=special.feats):
                ftml.setFeatures(featlist)
                builder.render(special.uids, ftml)
                # close test so each special is on its own row:
                ftml.closeTest()
            ftml.clearFeatures()
            if len(special.langs):
                for langID in builder.allLangs:
                    ftml.setLang(langID)
                    builder.render(special.uids, ftml)
                    ftml.closeTest()
                ftml.clearLang()
            ftml.clearBackground()

    if test.lower().startswith("proof"):
        # Characters used to create SILE test data
        ftml.startTestGroup('Proof')
        for section in (vowels, consonants, matra_like, digits, punct):
            builder.render(section, ftml)
            ftml.closeTest()

    if test.lower().startswith("diac"):
        # Diac attachment:

        # Representative base and diac chars:
        repDiac = list(filter(lambda x: x in builder.uids(), (0x0C81, 0x0C82, 0x0C83, nukta)))
        repBase = list(filter(lambda x: x in builder.uids(), (0x0C95, 0x0CDE, dotted_circle)))

        ftml.startTestGroup('Representative diacritics on all bases that take diacritics')
        for uid in uids:
            # ignore bases outside of the primary script:
            if uid not in block: continue
            c = builder.char(uid)
            # Always process Lo, but others only if they take marks:
            if c.general == 'Lo' or c.isBase:
                for diac in repDiac:
                    setBackgroundColor((uid,diac))
                    for featlist in builder.permuteFeatures(uids=(uid,diac)):
                        ftml.setFeatures(featlist)
                        # Don't automatically separate connecting or mirrored forms into separate lines:
                        builder.render((uid,diac), ftml, addBreaks=False)
                    ftml.clearFeatures()
                ftml.closeTest()

        ftml.startTestGroup('All diacritics on representative bases')
        for uid in uids:
            # ignore marks outside of the primary script:
            if uid not in block: continue
            c = builder.char(uid)
            if c.general == 'Mn':
                for base in repBase:
                    for featlist in builder.permuteFeatures(uids=(uid,base)):
                        ftml.setFeatures(featlist)
                        builder.render((base,uid), ftml, keyUID=uid, addBreaks=False)
                    ftml.clearFeatures()
                ftml.closeTest()

    if test.lower().startswith("matras"):
        ftml.startTestGroup('Consonants with matras')
        for c in consonants + [dotted_circle]:
            for m in matra_like:
                builder.render((c,m,nine), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

        ftml.startTestGroup('Akhands with matras')
        for a in akhands:
            for m in matra_like:
                builder.render((a+(m,)), ftml, label=f'{a[0]:04X}', comment=builder.char(a[0]).basename)
        ftml.closeTest()

        ftml.startTestGroup('Consonant with one or two sub forms and a wrap matra')
        for c in consonants:
            for wm in wrap_matras:
                builder.render((c,virama,c,wm,c), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
                builder.render((c,virama,c,virama,c,wm,c), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

    if test.lower().startswith("conjuncts"):
        ftml.startTestGroup('Consonant with one sub form')
        for c1 in consonants:
            for c2 in consonants:
                builder.render((c1,virama,c2,c2), ftml, label=f'{c1:04X}', comment=builder.char(c1).basename)
            ftml.closeTest()

        ftml.startTestGroup('Consonant with nukta and one sub form')
        for c1 in consonants:
            for c2 in consonants:
                builder.render((c1,nukta,virama,c2,c2), ftml, label=f'{c1:04X}', comment=builder.char(c1).basename)
            ftml.closeTest()

        ftml.startTestGroup('Consonant with nukta and one sub form and matra')
        for c in consonants:
            for m in matra_like:
                builder.render((c,nukta,virama,c,m,nine), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

        for c0 in (ka, ga, gha, ja):
            label = f'U+{c0:04X}'
            comment = builder.char(c0).basename
            ftml.startTestGroup(f'Consonant {label} {comment} with two sub forms')
            for c1 in consonants:
                for c2 in consonants:
                    builder.render((c0,virama,c1,virama,c2,c2), ftml, label=f'{c1:04X}', comment=builder.char(c1).basename)
                ftml.closeTest()

        ftml.startTestGroup('Consonant with two sub forms and matra')
        for c in consonants:
            for m in matra_like:
                builder.render((c,virama,c,virama,c,m,nine), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

        ftml.startTestGroup('Consonant with two sub forms (all with nuktas) and matra')
        for c in consonants:
            for m in matra_like:
                builder.render((c,nukta,virama,c,nukta,virama,c,nukta,m,c,nukta), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

    if test.lower().startswith("nuktas"):
        ftml.startTestGroup('Vowels')
        for v in vowels:
            builder.render((v,nukta), ftml, label=f'{v:04X}', comment=builder.char(v).basename)
            ftml.closeTest()

        ftml.startTestGroup('Consonants')
        for c in consonants:
            builder.render((c,nukta), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

        ftml.startTestGroup('Akhands')
        for a in akhands:
            builder.render((a+(nukta,)), ftml, label=f'{a[0]:04X}', comment=builder.char(a[0]).basename)
        ftml.closeTest()

        ftml.startTestGroup('Consonants with matra and nukta')
        for c in consonants:
            for m in matra_like:
                builder.render((c,m,nukta), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

        ftml.startTestGroup('Akhands with matra and nukta')
        for a in akhands:
            for m in matra_like:
                builder.render((a+(m,)+(nukta,)), ftml, label=f'{a[0]:04X}', comment=builder.char(a[0]).basename)
        ftml.closeTest()

        ftml.startTestGroup('Consonants with nukta and matra')
        for c in consonants:
            for m in matra_like:
                builder.render((c,nukta,m), ftml, label=f'{c:04X}', comment=builder.char(c).basename)
            ftml.closeTest()

        ftml.startTestGroup('Akhands with nukta and matra')
        for a in akhands:
            for m in matra_like:
                builder.render((a+(nukta,)+(m,)), ftml, label=f'{a[0]:04X}', comment=builder.char(a[0]).basename)
        ftml.closeTest()

    # Write the output ftml file
    ftml.writeFile(args.output)


def cmd() : execute("UFO",doit,argspec)
if __name__ == "__main__": cmd()
