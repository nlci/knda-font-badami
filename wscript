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
DOCDIR='documentation'
OUTDIR='installers'
ZIPDIR='releases'
TESTDIR='tests'
STANDARDS='tests/reference'

# set the font name, licensing, description, and version
script='knda'
APPNAME='nlci-' + script
#COPYRIGHT='Copyright (c) 2009-2018, NLCI (http://www.nlci.in/fonts/)'
LICENSE='OFL.txt'

DESC_SHORT='Kannada Unicode font with OT support'
#DESC_LONG='''
#Pan Kannada font designed to support all the languages using the Kannada script.
#'''
DESC_NAME='NLCI-' + script
DEBPKG='fonts-nlci-' + script
getufoinfo('source/Badami-Regular.ufo')

# set test parameters
TESTSTRING=u'\u0c95'
ftmlTest('tools/FTMLcreateList.xsl')
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
archive = fontbase + 'archive/'
generated = 'generated/'
tag = script.upper()

#panose = [2, 0, 0, 3]
#codePageRange = [0]
#unicodeRange = [0, 1, 15, 22, 31]
#hackos2 = os2.hackos2(panose, codePageRange, unicodeRange)

if '-l' in opts:
    for f, fLegacy in zip(faces, facesLegacy):
        for (s, sn, sLegacy) in zip(styles, stylesName, stylesLegacy):
            gentium = '../../../../latn/fonts/gentium_local/basic/1.102/zip/unhinted/2048/GenBkBas' + s.replace('-', '') + '.ttf'
            charis = '../../../../latn/fonts/charis_local/5.000/zip/unhinted/2048/CharisSIL' + s + '.ttf'
            font(target = process('ufo/' + f + '-' + sn.replace(' ', '') + '.ttf',
                    cmd('cp ${DEP} ${TGT}'),
                    ),
                source = legacy(f + s + '.ttf',
                                source = archive + 'unhinted/' + fLegacy + sLegacy + '.ttf',
                                xml = fontbase + 'badami_unicode.xml',
                                params = '-f ' + gentium,
                                noap = '')
                )

psfix = 'cp' if '-p' in opts else 'psfix'

if '-l' in opts:
    faces = list()
for f in faces:
#    p = package(
#        appname = APPNAME + '-' + f.lower(),
#        version = VERSION,
#        outdir = 'packages',
#        zipdir = ''
#    )
    for (s, sn) in zip(styles, stylesName):
        snf = '-' + sn.replace(' ', '')
        fontfilename = tag + f + '-' + sn.replace(' ', '')
        font(target = process(fontfilename + '.ttf',
                cmd(psfix + ' ${DEP} ${TGT}'),
                #cmd(hackos2 + ' ${DEP} ${TGT}'),
                name(tag + ' ' + f, lang='en-US', subfamily=(sn))
                ),
            source = fontbase + f + snf + '.ufo',
            opentype = fea(fontbase + 'master.fea', no_make = True),
            # opentype = fea(generated + f + s + '.fea',
            #     master = fontbase + 'master.fea',
            #     make_params = '' # might need -z 8 to work around a FontForge bug
            #     ),
            graphite = gdl(generated + f + s + '.gdl',
               master = fontbase + 'master.gdl',
               make_params = '-p 1',
               params = ''
               ),
            #classes = fontbase + 'badami_classes.xml',
            ap = generated + f + s + '.xml',
            version = VERSION,
            #copyright = COPYRIGHT,
            #license = ofl('Badami', 'Kaveri', 'NLCI'),
            woff = woff('woff/' + fontfilename + '.woff', params = '-v ' + VERSION + ' -m ../' + fontbase + f + '-WOFF-metadata.xml'),
            script = 'knda',
            #package = p,
            fret = fret(params = '-r')
            )
