# badami

# command line options
opts = preprocess_args(
    {'opt' : '-l'}, # build fonts from legacy for inclusion into final fonts
    {'opt' : '-p'}, # do not run psfix on the final fonts
    {'opt' : '-s'}  # only build a single font
    )

import os2

# set folder names
out='results'
TESTDIR='tests'
STANDARDS='tests/reference'

# set meta-information
script='knda'
APPNAME='nlci-' + script
VERSION='0.101'
TTF_VERSION='0.101'
COPYRIGHT='Copyright (c) 2009-2015, NLCI (http://www.nlci.in/fonts/)'

DESC_SHORT='Kannada Unicode font with OT support'
DESC_LONG='''
Pan Kannada font designed to support all the languages using the Kannada script.
'''
DESC_NAME='NLCI-' + script
DEBPKG='fonts-nlci-' + script

# set test parameters
TESTSTRING=u'\u0c95'

# set fonts to build
faces = ('Badami', 'Kaveri')
facesLegacy = ('BADA', 'KAVE')
styles = ('-R', '-B', '-I', '-BI')
stylesName = ('Regular', 'Bold', 'Italic', 'Bold Italic')
stylesLegacy = ('', 'BD', 'I', 'BI')

if '-s' in opts:
    faces = (faces[0],)
    facesLegacy = (facesLegacy[0],)
    styles = (styles[0],)
    stylesName = (stylesName[0],)
    stylesLegacy = (stylesLegacy[0],)

# set build parameters
fontbase = 'source/'
tag = script.upper()

panose = [2, 0, 0, 3]
codePageRange = [0]
unicodeRange = [0, 15, 22, 31]
hackos2 = os2.hackos2(panose, codePageRange, unicodeRange)

if '-l' in opts:
    for f, fLegacy in zip(faces, facesLegacy):
        for (s, sn, sLegacy) in zip(styles, stylesName, stylesLegacy):
            font(target = process(f + '-' + sn.replace(' ', '') + '.ttf',
                    cmd('psfix ${DEP} ${TGT}'),
                    ),
                source = legacy(f + s + '.ttf',
                                source = fontbase + 'archive/' + fLegacy + sLegacy + '.ttf',
                                xml = fontbase + 'badami_unicode.xml',
                                noap = '')
                )

psfix = 'cp' if '-p' in opts else 'psfix'

for f in faces:
#    p = package(
#        appname = APPNAME + '-' + f.lower(),
#        version = VERSION,
#        outdir = 'packages',
#        zipdir = ''
#    )
    for (s, sn) in zip(styles, stylesName):
        font(target = process(tag + f + '-' + sn.replace(' ', '') + '.ttf',
                cmd(psfix + ' ${DEP} ${TGT}'),
                cmd(hackos2 + ' ${DEP} ${TGT}'),
                name(tag + ' ' + f, lang='en-US', subfamily=(sn))
                ),
            source = fontbase + f + s + '.sfd',
            opentype = fea(fontbase + f + s + '.fea',
                master = fontbase + 'master.fea',
                make_params = '' # might need -z 8 to work around a FontForge bug
                ),
            graphite = gdl(fontbase + f + s + '.gdl',
               master = fontbase + 'master.gdl',
               make_params = '',
               params = ''
               ),
            #classes = fontbase + 'badami_classes.xml',
            ap = fontbase + f + s + '.xml',
            version = TTF_VERSION,
            copyright = COPYRIGHT,
            license = ofl('Badami', 'Kaveri', 'NLCI'),
            woff = woff(),
            script = 'knda',
            #package = p,
            fret = fret(params = '-r')
            )
