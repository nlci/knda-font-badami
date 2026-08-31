#!/usr/bin/python3
# this is a smith configuration file

# badami

# command line options
opts = preprocess_args(
    {'opt' : '-l'}, # build fonts from legacy for inclusion into final fonts
    {'opt' : '-r'}, # only build the main regular font
    {'opt' : '-s'}, # only build the main font family
    )

import os2

# override the default folders
DOCDIR = ['documentation', 'web']

# set the font name, licensing, description, and version
prefix = 'nlci-knda-'
APPNAME = prefix + 'badami'
LICENSE='OFL.txt'

DESC_SHORT='Kannada Unicode font with OT support'
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

# set build parameters
fontbase = 'source/'
archive = fontbase + 'archive/unhinted/'
generated = 'generated/'
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

cmds = [
    cmd('psfchangettfglyphnames ${SRC} ${DEP} ${TGT}', ['${source}']),
    cmd('gftools fix-nonhinting -q --no-backup ${DEP} ${TGT}'),
    ]

for dspace in dspaces:
    designspace('source/' + 'Badami' + dspace + '.designspace',
        target = process('${DS:FILENAME_BASE}.ttf', *cmds),
        # params = '--decomposeComponents --removeOverlaps',
        instances = ['Badami Regular'] if '-r' in opts else None,
        opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
            mapfile = generated + '${DS:FILENAME_BASE}.map',
            master = fontbase + 'master.feax',
            make_params = omitaps + '--psfCompatible -L last',
            params = ''
            ),
        # graphite = gdl(generated + '${DS:FILENAME_BASE}.gdl',
        #    master = fontbase + 'master.gdl',
        #    make_params = '-p 1',
        #    params =  '-e ${DS:FILENAME_BASE}_gdlerr.txt'
        #    ),
        # classes = fontbase + 'badami_classes.xml',
        ap = generated + '${DS:FILENAME_BASE}.xml',
        version = VERSION,
        woff = woff('web/${DS:FILENAME_BASE}', type='woff2',
            metadata = '../source/${DS:FAMILYNAME_NOSPC}-WOFF-metadata.xml'),
        script = 'knd2', # 'knda'
        pdf = fret(params = '-oi')
        )

if '-s' not in opts:
    kaveripackage = package(
        appname = prefix + 'kaveri',
        version = VERSION,
        docdir = {'documentation': 'documentation', 'web_kaveri': 'web'}
    )
    for dspace in dspaces:
        designspace('source/' + 'Kaveri' + dspace + '.designspace',
            target = process('${DS:FILENAME_BASE}.ttf', *cmds),
            opentype = fea(generated + '${DS:FILENAME_BASE}.fea',
                mapfile = generated + '${DS:FILENAME_BASE}.map',
                master = fontbase + 'master.feax',
                make_params = omitaps + '--psfCompatible -L last',
                params = ''
                ),
            # classes = fontbase + 'badami_classes.xml',
            ap = generated + '${DS:FILENAME_BASE}.xml',
            version = VERSION,
            woff = woff('web_kaveri/${DS:FILENAME_BASE}', type='woff2',
                metadata = '../source/${DS:FAMILYNAME_NOSPC}-WOFF-metadata.xml',
                dontship = True),
            script = 'knd2',
            package = kaveripackage,
            pdf = fret(params = '-oi')
            )
