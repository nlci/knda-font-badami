#!/bin/python

# set OS/2 bits using hackos2

def reversebytes(bytes):
    result = ''
    for byte in bytes:
        result = "%02X%s" % (byte, result)
    return result

def makehex(bits):
    result = 0
    for bit in bits:
        result = result | (1<<bit)
    return "%X" % result

def hackos2(panose, codePageRange, unicodeRange):
    command = 'hackos2 -p %s -c %s -u %s' % (reversebytes(panose),
                                             makehex(codePageRange),
                                             makehex(unicodeRange))
    return command
