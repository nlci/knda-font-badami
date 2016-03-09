# badami

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
styles = ('-R', '-B', '-I', '-BI')
stylesName = ('Regular', 'Bold', 'Italic', 'Bold Italic')

# set build parameters
fontbase = 'source/'
tag = script.upper()

panose = [2, 0, 0, 3]
codePageRange = [0]
unicodeRange = [0, 15, 22, 31]
hackos2 = os2.hackos2(panose, codePageRange, unicodeRange)

for f in faces:
#    p = package(
#        appname = APPNAME + '-' + f.lower(),
#        version = VERSION,
#        outdir = 'packages',
#        zipdir = ''
#    )
    for (s, sn) in zip(styles, stylesName):
        font(target = process(tag + f + '-' + sn.replace(' ', '') + '.ttf',
                cmd(hackos2 + ' ${DEP} ${TGT}'),
                name(tag + ' ' + f, lang='en-US', subfamily=(sn))
                ),
            source = fontbase + f + s + '.sfd',
            #sfd_master = fontbase + 'master.sfd',
            opentype = internal(),
            #graphite = gdl(fontbase + f + s + '.gdl',
            #    master = fontbase + 'master.gdl',
            #    make_params = '',
            #    params = ''
            #    ),
            #classes = fontbase + 'badami_classes.xml',
            ap = f + s + '.xml',
            version = TTF_VERSION,
            copyright = COPYRIGHT,
            license = ofl('Badami', 'Kaveri', 'NLCI'),
            woff = woff(),
            script = 'knda',
            #package = p,
            fret = fret(params = '-r')
            )
