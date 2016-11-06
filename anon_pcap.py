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
parser.add_argument('-v', '--values', help='A pair of values before/after anonymized.', metavar='VALUE', nargs=2, action='append')
args = parser.parse_args()

src_pcap  = args.srcpcap
dst_pcap  = args.dstpcap
val_pairs = args.values

class PcapData():
    'Main class for PCAP to be handled.'
    def __init__(self, srcpath, dstpath):
        self.dstfile = open(dstpath, 'w')
        self.pcap_bin = self.file2bin(srcpath)
        self.pcap_hex = self.bin2hex(self.pcap_bin)

    def file2bin(self, path):
        bindata = open(path, 'rb').read()
        return bindata

    def bin2hex(self, bindata):
        hexdata = binascii.hexlify(bindata)
        return hexdata

    def str2hex(self, strdata):
        h = binascii.hexlify(strdata)
        return h

    def replace_value(self, strargs):
        for l in strargs:
            self.pcap_mod_hex = self.pcap_hex.replace(self.str2hex(l[0]), self.str2hex(l[1]))
            print 'Replaced "%s" as "%s"' % (l[0], l[1])
        return self.pcap_mod_hex

    def write_pcap(self, hexdata):
        self.dstfile.write(bytearray.fromhex(hexdata))

def main():
    validate(val_pairs)
    p = PcapData(src_pcap, dst_pcap)
    r = p.replace_value(val_pairs)
    p.write_pcap(r)

if __name__ == '__main__':
    main()
