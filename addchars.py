#!/bin/python

import os
import os.path
import sys
from wscript import *

nlci = '../../../../work/nlci/projects/fonts/charsets/'
charis = '../../../latn/fonts/charis_local/5.000/zip/CharisSIL'
gentium = '../../../latn/fonts/gentium_local/basic/1.102/zip/GenBkBas'
annapurna = '../../../deva/fonts/annapurna_local/1.203/zip/AnnapurnaSIL-'
badami = '../badami/source'

def runCommand(cmd, filenames):
    cmd = sys.argv[1] + ' -f ' + cmd + ' ' + filenames
    print cmd
    os.system(cmd)

def findFile(filename):
    return os.path.join(sys.argv[2], filename)

def modifyFile(cmd, filename):
    tmp = 'tmp.sfd'
    os.rename(findFile(filename), tmp)
    runCommand(cmd, tmp + ' ' + findFile(filename))
    os.remove(tmp)

def modifySource(sfd, f, s, sn):
    print sfd

    cmd = '-i ' + findFile(os.path.join('..', 'results', f + '-' + sn.replace(' ', '') + '.ttf')) + ' --namefile knda_glyphs.txt --rangefile knda.txt'
    modifyFile(cmd, sfd)

    asn = sn
    asn = asn.replace('Bold Italic', 'Bold')
    asn = asn.replace('Italic', 'Regular')
    cmd = '-i ' + annapurna + asn + '.ttf' + ' --rangefile ' + os.path.join(nlci, 'annapurna', 'indic.txt')
    # modifyFile(cmd, sfd)

    cmd = '-s 0.5 -i ' + charis + s + '.ttf' + ' -n uni0334.Lrg --rangefile pre.txt --rangefile nrsi.txt --rangefile pua.txt --rangefile nlci-latin.txt'
    # cmd = '-s 0.5 -i ' + charis + s + '.ttf' + ' --rangefile nrsi.txt --rangefile nlci.txt'
    # modifyFile(cmd, sfd)

    # ms = s.replace('-', '')
    # cmd = '-s 0.5 -i ' + gentium + ms + '.ttf' + ' --rangefile pre.txt --rangefile nrsi.txt --rangefile nlci.txt'
    # modifyFile(cmd, sfd)
    # findFile(os.path.join('..', 'results', f + '-' + sn.replace(' ', '') + '.ttf'))

for f in faces:
    for (s, sn) in zip(styles, stylesName):
        modifySource(f + s + '.sfd', f, s, sn)
# modifySource('master.sfd', 'Badami', '-R', 'Regular')
