#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import binascii

def validate(vps):
    '''Check the length of each argment in pairs. (Need better error handling...)'''
    for l in vps:
        if len(l[0]) != len(l[1]):
            print 'ERROR: Value to be replaced should be the same in length.'
            print '%s\t : %d' % (l[0], len(l[0]))
            print '%s\t : %d' % (l[1], len(l[1]))
            quit(-1)
        else:
            return True

parser = argparse.ArgumentParser(description='Mini python script to replace specified value in PCAP(or any binary) file.')
parser.add_argument('-s', '--srcpcap', help='Path to the raw PCAP file to be anonymized.', required=True)
parser.add_argument('-d', '--dstpcap', help='Filename of the anonymized PCAP file.', default='anonymized.pcap')
parser.add_argument('-v', '--strvals', help='A pair of values before/after anonymized in STRING format.', metavar='STRVAL', nargs=2, action='append')
parser.add_argument('-x', '--hexvals', help='A pair of values before/after anonymized in HEX format.', metavar='HEXVAL', nargs=2, action='append')
args = parser.parse_args()

src_pcap  = args.srcpcap
dst_pcap  = args.dstpcap
str_pairs = args.strvals
hex_pairs = args.hexvals

class PcapData():
    'Main class for PCAP to be handled.'
    def __init__(self, srcpath, dstpath):
        self.dstfile = open(dstpath, 'w')
        self.pcap_bin = self.file2bin(srcpath)
        self.pcap_hex = self.bin2hex(self.pcap_bin)

    def file2bin(self, path):
        ''' open pcap file as binary. '''
        bindata = open(path, 'rb').read()
        return bindata

    def bin2hex(self, bindata):
        ''' convert binary into hexadecimal. '''
        hexdata = binascii.hexlify(bindata)
        return hexdata

    def str2hex(self, strdata):
        ''' convert string into hexadecimal. '''
        hexdata = binascii.hexlify(strdata)
        return hexdata

    def swap_str(self, strdata, fill):
        ''' swap argument string by two characters(for the legacy protocols like SS7). '''
        if len(strdata) % 2 == 1:
            strdata = strdata + fill
        swapped = ''.join(map(lambda x: x[::-1], [strdata[i: i+2] for i in range(0, len(strdata), 2)])) # python magic!
        return swapped

    def replace_strval(self, strargs):
        ''' replace value with string-formatted argument(-v). '''
        for l in strargs:
            if self.str2hex(l[0]) not in self.pcap_hex:
                self.pcap_hex = self.pcap_hex.replace(self.swap_str(l[0], 'f'), self.swap_str(l[1], l[1][-1]))
                self.pcap_hex = self.pcap_hex.replace(self.swap_str(l[0], '0'), self.swap_str(l[1], l[1][-1]))
                print 'Replaced "%s" as "%s"' % (l[0], l[1])
            else:
                self.pcap_hex = self.pcap_hex.replace(self.str2hex(l[0]), self.str2hex(l[1]))
                print 'Replaced "%s" as "%s"' % (l[0], l[1])
        return self.pcap_hex

    def replace_hexval(self, hexargs):
        ''' replace value with hex-formatted argument(-x). '''
        for l in hexargs:
            self.pcap_hex = self.pcap_hex.replace(l[0], l[1])
            print 'Replaced "%s" as "%s"' % (l[0], l[1])
        return self.pcap_hex

    def write_pcap(self, hexdata):
        ''' write modified data as binary(pcap) file. '''
        self.dstfile.write(bytearray.fromhex(hexdata))

def main():
    validate(str_pairs)
    p = PcapData(src_pcap, dst_pcap)
    r = p.replace_strval(str_pairs)
    r = p.replace_hexval(hex_pairs)
    p.write_pcap(r)

if __name__ == '__main__':
    main()
