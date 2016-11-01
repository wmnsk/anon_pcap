#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import binascii

parser = argparse.ArgumentParser(description='Mini python script to replace specified value in PCAP(or any binary) file.')
parser.add_argument('-s', '--srcpcap', help='Path to the raw PCAP file to be anonymized.', required=True)
parser.add_argument('-d', '--dstpcap', help='Filename of the anonymized PCAP file.', default='anonymized.pcap')
parser.add_argument('-v', '--values', help='A pair of values before/after anonymized.', metavar='VALUE', nargs=2, action='append')
args = parser.parse_args()

def strtohex(s):
    h = binascii.hexlify(s)
    return h

def convert_valargs(vps):
    vp = []
    for l in vps:
        vp.append(map(strtohex, l))
    return vp

def read_as_bin(path):
    with open(path, 'rb') as infile:
        binfile = infile.read()
    return binfile

def bintohex(b):
    pcap_hex = binascii.hexlify(pcap_bin)

src_pcap  = args.srcpcap
dst_pcap  = open(args.dstpcap, 'w')
val_pairs = convert_valargs(args.values)

class PktCap(object):
    'Main class for PCAP to be handled.'
    def __init__(self, srcpath, dstpath):
        self.dst = dstpath
        self.pcap_bin = read_as_bin(srcpath)
        self.pcap_hex = binascii.hexlify(self.pcap_bin)

    def replace_value(self, vps):
        for l in vps:
            self.pcap_hex = self.pcap_hex.replace(l[0], l[1])
            print 'Replaced "%s" as "%s"' % (binascii.unhexlify(l[0]), binascii.unhexlify(l[1]))
        return self.pcap_hex

    def hex_to_pcap(self, hexlified):
        self.pcap_mod_bin = bytearray.fromhex(hexlified)
        self.dst.write(self.pcap_mod_bin)

def main():
    p = PktCap(src_pcap, dst_pcap)
    r = p.replace_value(val_pairs)
    p.hex_to_pcap(r)

if __name__ == '__main__':
    main()
