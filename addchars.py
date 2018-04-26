#!/bin/python

import os
import os.path
import sys
import shutil
from wscript import *

charis = '../../../latn/fonts/charis_local/5.000/zip/unhinted/CharisSIL'
gentium = '../../../latn/fonts/gentium_local/basic/1.102/zip/unhinted/GenBkBas'
annapurna = '../../../deva/fonts/annapurna_local/1.203/zip/unhinted/AnnapurnaSIL-'
panini = '../../../deva/fonts/panini/source/Panini'
thiruvalluvar = '../../../taml/fonts/thiruvalluvar/source/ThiruValluvar'
badami = '../badami/source'
exo = '../../../latn/fonts/exo/1.500/zip/unhinted/Exo-'

def runCommand(cmd, ifont, ofont):
    cmd = 'ffcopyglyphs' + ' -f ' + cmd + ' ' + ifont + ' ' + ofont
    print cmd
    os.system(cmd)

def findFile(filename):
    return os.path.join(sys.argv[1], filename)

def modifyFile(cmd, filename):
    tmp = 'tmp.sfd'
    os.rename(findFile(filename), tmp)
    runCommand(cmd, tmp, findFile(filename))
    os.remove(tmp)

def modifySource(sfd, f, s, sn):
    print sfd

    old = findFile(f + s + '.sfd')
    new = findFile(sfd)
    shutil.copyfile(old, new)

    cmd = '-i ' + findFile(os.path.join('..', 'results', 'ufo', f + '-' + sn + '.sfd')) + ' --namefile cs/knda/main_glyphs.txt --rangefile cs/knda/main.txt'
    modifyFile(cmd, sfd)

    cmd = '-i ' + thiruvalluvar + '-' + sn + '.sfd' + ' --rangefile cs/thiruvalluvar/main.txt'
    modifyFile(cmd, sfd)

    ps = s
    ps = ps.replace('-BI', '-B')
    cmd = '-i ' + panini + ps + '.sfd' + ' --rangefile cs/panini/main4knda.txt'
    modifyFile(cmd, sfd)

    asn = sn
    asn = asn.replace('BoldItalic', 'Bold')
    asn = asn.replace('Italic', 'Regular')
    cmd = '-i ' + annapurna + asn + '.ttf' + ' --rangefile cs/annapurna/main.txt'
    modifyFile(cmd, sfd)

    if f == 'Kaveri':
        lighter = {
            'Regular': 'Medium',
            'Italic': 'MediumItalic',
            'Bold': 'SemiBold',
            'BoldItalic': 'SemiBoldItalic'
            }
        heavier = {
            'Regular': 'SemiBold',
            'Italic': 'SemiBoldItalic',
            'Bold': 'Bold',
            'BoldItalic': 'BoldItalic'
            }
        esn = lighter[sn]
        esn = heavier[sn]
        cmd = '-i ' + exo + esn + '.sfd' + ' --namefile cs/exo/main_glyphs.txt --rangefile cs/exo/pre.txt --rangefile cs/exo/main.txt'
        modifyFile(cmd, sfd)
        cmd = '-i ' + charis + s + '.ttf' + ' --rangefile cs/charis/composite4gentium.txt --rangefile cs/charis/extra4exo.txt'
        modifyFile(cmd, sfd)
    else:
        gs = s.replace('-', '')
        cmd = '-i ' + gentium + gs + '.ttf' + ' --namefile cs/gentium/main_glyphs.txt --rangefile cs/gentium/pre.txt --rangefile cs/gentium/main.txt'
        modifyFile(cmd, sfd)
        cmd = '-i ' + charis + s + '.ttf' + ' --rangefile cs/charis/composite4gentium.txt --rangefile cs/charis/extra4gentium.txt'
        modifyFile(cmd, sfd)

for f in faces:
    for (s, sn) in zip(styles, stylesName):
        sn = sn.replace(' ', '')
        modifySource(f + '-' + sn + '.sfd', f, s, sn)
