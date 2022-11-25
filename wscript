#!/usr/bin/python3
# this is a smith configuration file

# badami

# command line options
opts = preprocess_args(
    {'opt' : '-l'}, # build fonts from legacy for inclusion into final fonts
    {'opt' : '-r'}, # only build the main regular font
    {'opt' : '-s'}  # only build a single font family
    )

import os2

# override the default folders
DOCDIR = ['documentation', 'web']

# set the font name, licensing, description, and version
script='knda'
APPNAME='nlci-' + script
LICENSE='OFL.txt'

DESC_SHORT='Kannada Unicode font with OT support'
DESC_NAME='NLCI-' + script
getufoinfo('source/Badami-Regular.ufo')
# BUILDLABEL = 'beta1'

# Set up tests
TEXTSIZE=16
ftmlTest('tools/ftml-smith.xsl')

# set fonts to build
faces = ('Badami', 'Kaveri')
facesLegacy = ('BADA', 'KAVE')
styles = ('-R', '-B', '-I', '-BI')
stylesName = ('Regular', 'Bold', 'Italic', 'Bold Italic')
stylesLegacy = ('', 'BD', 'I', 'BI')
dspaces = ('Roman', 'Italic')

if '-r' in opts or '-s' in opts:
    faces = (faces[0],)

if '-r' in opts:
    dspaces = ('Regular',)

# set build parameters
fontbase = 'source/'
archive = fontbase + 'archive/unhinted/'
generated = 'generated/'
tag = script.upper()
omitaps = '--omitaps "_V V"'

panose = [2, 0, 0, 3]
codePageRange = [0, 29]
unicodeRange = [0, 1, 2, 3, 4, 5, 6, 7, 15, 22, 29, 31, 32, 33, 35, 38, 39, 40, 45, 60, 62, 67, 69, 91]
hackos2 = os2.hackos2(panose, codePageRange, unicodeRange)

if '-l' in opts:
    for f, fLegacy in zip(faces, facesLegacy):
        for (s, sn, sLegacy) in zip(styles, stylesName, stylesLegacy):
            font(target = process('ufo/' + f + '-' + sn.replace(' ', '') + '.ttf',
                    cmd(hackos2 + ' ${DEP} ${TGT}'),
                    name(f, lang='en-US', subfamily=(sn))
                    ),
                source = legacy(f + s + '.ttf',
                                source = archive + fLegacy + sLegacy + '.ttf',
                                xml = fontbase + 'badami_unicode.xml',
                                params = '',
                                noap = '')
                )

if '-l' in opts:
    faces = list()
for f in faces:
    p = package(
        appname = APPNAME + '-' + f.lower(),
        version = VERSION,
        docdir = DOCDIR # 'documentation'
    )
    for dspace in dspaces:
        designspace('source/' + f + dspace + '.designspace',
            target = process('${DS:FILENAME_BASE}.ttf',
                cmd('psfchangettfglyphnames ${SRC} ${DEP} ${TGT}', ['source/${DS:FILENAME_BASE}.ufo']),
            ),
            # params = '--decomposeComponents --removeOverlaps',
            opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
                mapfile = generated + '${DS:FILENAME_BASE}.map',
                master = fontbase + 'master.feax',
                make_params = omitaps + ' -L last',
                params = ''
                ),
            # graphite = gdl(generated + '${DS:FILENAME_BASE}.gdl',
            #    master = fontbase + 'master.gdl',
            #    make_params = '-p 1',
            #    params =  '-e ${DS:FILENAME_BASE}_gdlerr.txt'
            #    ),
            classes = fontbase + 'badami_classes.xml',
            ap = generated + '${DS:FILENAME_BASE}.xml',
            version = VERSION,
            woff = woff('woff/${DS:FILENAME_BASE}', type='woff2',
                metadata = '../source/${DS:FAMILYNAME_NOSPC}-WOFF-metadata.xml'),
            script = 'knd2', # 'knda'
            package = p,
            pdf = fret(params = '-oi')
            )
