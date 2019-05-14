#!/usr/bin/python
# this is a smith configuration file

# badami

# command line options
opts = preprocess_args(
    {'opt' : '-l'}, # build fonts from legacy for inclusion into final fonts
    {'opt' : '-p'}, # do not run psfix on the final fonts
    {'opt' : '-s'}  # only build a single font
    )

import os2

# set the default output folders
out='results'

# locations of files needed for some tasks
DOCDIR = ['documentation', 'web']
STANDARDS='tests/reference'

# set the font name, licensing, description, and version
script='knda'
APPNAME='nlci-' + script
LICENSE='OFL.txt'

DESC_SHORT='Kannada Unicode font with OT support'
DESC_NAME='NLCI-' + script
DEBPKG='fonts-nlci-' + script
getufoinfo('source/Badami-Regular.ufo')

# set test parameters
TESTSTRING=u'\u0c95'
#ftmlTest('tools/FTMLcreateList.xsl')
ftmlTest('tools/ftml-padauk.xsl')
testCommand('sile', cmd='${SILE} -o "${TGT}" "${SRC[0].abspath()}" -f "${SRC[1]}"', extracmds=['sile'], shapers=0, supports=['.sil'], ext='.pdf')

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
archive = fontbase + 'archive/unhinted/'
generated = 'generated/'
tag = script.upper()

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

psfix = 'cp' if '-p' in opts else 'psfix'

if '-l' in opts:
    faces = list()
for f in faces:
    p = package(
        appname = APPNAME + '-' + f.lower(),
        version = VERSION,
        docdir = DOCDIR # 'documentation'
    )
    for sn in stylesName:
        snf = '-' + sn.replace(' ', '')
        fontfilename = tag + f + snf
        font(target = process(fontfilename + '.ttf',
                cmd('${PSFCHANGETTFGLYPHNAMES} ${SRC} ${DEP} ${TGT}', [fontbase + f + snf + '.ufo']),
                name(tag + ' ' + f, lang='en-US', subfamily=(sn))
                ),
            source = fontbase + f + snf + '.ufo',
            opentype = fea(fontbase + 'master.fea', no_make = True),
            # opentype = fea(generated + f + snf + '.fea',
            #     master = fontbase + 'master.fea',
            #     make_params = '' # might need -z 8 to work around a FontForge bug
            #     ),
            graphite = gdl(generated + f + snf + '.gdl',
               master = fontbase + 'master.gdl',
               make_params = '-p 1',
               params =  '-e ' + f + snf + '_gdlerr.txt'
               ),
            #classes = fontbase + 'badami_classes.xml',
            ap = generated + f + snf + '.xml',
            version = VERSION,
            woff = woff('woff/' + fontfilename + '.woff', params = '-v ' + VERSION + ' -m ../' + fontbase + f + '-WOFF-metadata.xml'),
            script = 'knda',
            package = p,
            fret = fret(params = '-r -oi')
            )

def configure(ctx):
    ctx.find_program('psfchangettfglyphnames')
