#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
anon_pcap.py - Mini python script to replace specified value in PCAP file.

Copyright(C) 2016-2024 Yoshiyuki Kurauchi
License: MIT (https://github.com/wmnsk/anon_pcap/blob/master/LICENSE)
Latest version is available on GitHub (https://github.com/wmnsk/anon_pcap).
'''

from binascii import hexlify as hx


def validate_args(v, a):
    '''Check the length of each argument in pairs.'''
    if v is None and a is None:
        print('ERROR: No replace argument specified. Quitting.')
        quit(-1)
    if v is not None:
        for x in v:
            if len(x[0]) != len(x[1]):
                print('ERROR: Value to be replaced should be the same in length.')
                print('%s\t : %d' % (x[0], len(x[0])))
                print('%s\t : %d' % (x[1], len(x[1])))
                quit(1)

    if a is not None:
        for x in a:
            if len(x[0]) != len(x[1]):
                print('ERROR: Value to be replaced should be the same in length.')
                print('%s\t : %d' % (x[0], len(x[0])))
                print('%s\t : %d' % (x[1], len(x[1])))
                quit(1)


class PcapHandler:
    '''Main class for PCAP to be handled.'''
    def __init__(self, srcpath, dstpath):
        self.dstfile = open(dstpath, 'wb')
        self.pcap_bin = self.file2bin(srcpath)
        self.pcap_hex = self.bin2hex(self.pcap_bin)

    def file2bin(self, path):
        '''read pcap file as binary.'''
        with open(path, 'rb') as d:
            bindata = d.read()
        return bindata

    def bin2hex(self, bindata):
        '''convert binary into hexadecimal.'''
        hexdata = hx(bindata).decode('utf-8')
        return hexdata

    def str2hex(self, strdata):
        '''convert string into hexadecimal.'''
        hexdata = hx(strdata.encode('utf-8')).decode('utf-8')
        return hexdata

    def swap_str(self, strdata, fill):
        '''swap argument string by two characters.
        (implemented for telco protocols with tbcd encoding).
        '''
        if len(strdata) % 2 == 1:
            strdata = strdata + fill
        return ''.join(map(lambda x: x[::-1], [strdata[i: i+2] for i in range(0, len(strdata), 2)]))

    def replace_strval(self, strargs):
        '''replace value with string-formatted argument (-v).'''
        for l in strargs:
            orgstr = l[0]
            modstr = l[1]
            if self.str2hex(orgstr) not in self.pcap_hex:
                self.pcap_hex = self.pcap_hex.replace(
                    self.swap_str(orgstr, 'f'),
                    self.swap_str(modstr, 'f')
                )
                self.pcap_hex = self.pcap_hex.replace(
                    self.swap_str(orgstr, '0'),
                    self.swap_str(modstr, '0')
                )
                print(f'Replaced "{orgstr}" as "{modstr}"')
            else:
                self.pcap_hex = self.pcap_hex.replace(
                    self.str2hex(orgstr), self.str2hex(modstr)
                )
                print(f'Replaced "{orgstr}" as "{modstr}"')
        return self.pcap_hex

    def replace_hexval(self, hexargs):
        '''replace value with hex-formatted argument (-x).'''
        for l in hexargs:
            orghex = l[0]
            modhex = l[1]
            self.pcap_hex = self.pcap_hex.replace(orghex, modhex)
            print(f'Replaced "{orghex}" as "{modhex}"')
        return self.pcap_hex

    def write_pcap(self, hexdata):
        '''write modified data as binary (pcap) file.'''
        self.dstfile.write(bytearray.fromhex(hexdata))
        self.dstfile.close()


def test_diameter():
    '''Testing replacements using diameter DWR packet.'''
    org_path = './testpcaps/diameter_DWR.pcap'
    tmp_path = './testpcaps/diameter_DWR_tmp.pcap'

    str_pairs = [
        ['some00.node00.', 'some99.node99.'],
        ['mnc999.mcc999.', 'mnc000.mcc000.'],
    ]
    hex_pairs = [
        ['0b0b0b0b0b0b', '0a0a0a0a0a0a'],
        ['01010101', '6f6f6f6f']
    ]

    p = PcapHandler(org_path, tmp_path)
    r = p.replace_strval(str_pairs)
    r = p.replace_hexval(hex_pairs)
    p.write_pcap(r)

    with open('testpcaps/diameter_DWR_tmp.pcap', 'rb') as tmp, open('testpcaps/diameter_DWR_mod.pcap', 'rb') as mod:
        tmpfile = tmp.read()
        modfile = mod.read()

    assert (tmpfile == modfile)


def main():
    from argparse import ArgumentParser as AP

    parser = AP(description='Mini python script to replace specified value in PCAP (or any binary) file.')
    parser.add_argument(
        '-s', '--srcpcap',
        help='Path to the raw PCAP file to be anonymized.',
        required=True
    )
    parser.add_argument(
        '-d', '--dstpcap',
        help='Filename of the anonymized PCAP file.',
        default='anonymized.pcap'
    )
    parser.add_argument(
        '-v', '--strvals',
        help='A pair of values before/after anonymized in STRING format.',
        metavar='STRVAL',
        nargs=2,
        action='append'
    )
    parser.add_argument(
        '-x', '--hexvals',
        help='A pair of values before/after anonymized in HEX format.',
        metavar='HEXVAL',
        nargs=2,
        action='append'
    )
    args = parser.parse_args()

    validate_args(args.strvals, args.hexvals)

    p = PcapHandler(args.srcpcap, args.dstpcap)
    if args.strvals is not None:
        r = p.replace_strval(args.strvals)
    if args.hexvals is not None:
        r = p.replace_hexval(args.hexvals)
    p.write_pcap(r)


if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1 and argv[1] == 'test':
        test_diameter()
    else:
        main()
