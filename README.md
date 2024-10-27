# anon_pcap.py

Mini python script to replace specified value in a PCAP file.  
Initially developed to anonymize sensitive information in PCAP file, but this script should work on any binary.

#### Disclaimer

Beware of the unexpected changes made by this script.
It is recommended to specify the as long value as possible, and to check the output PCAP file carefully.

## Features

* Replace specified value in PCAP file.
  * Works for TBCD-encoded values (e.g. IMSI, MSISDN, Global Title).
  * Any field can be replaced in hex format (as copied as hexstream on Wireshark).

## Usage

```shell-session
$ python3 ./anon_pcap.py -h
usage: anon_pcap.py [-h] -s SRCPCAP [-d DSTPCAP] [-v STRVAL STRVAL] [-x HEXVAL HEXVAL]

Mini python script to replace specified value in PCAP (or any binary) file.

options:
  -h, --help            show this help message and exit
  -s SRCPCAP, --srcpcap SRCPCAP
                        Path to the raw PCAP file to be anonymized.
  -d DSTPCAP, --dstpcap DSTPCAP
                        Filename of the anonymized PCAP file.
  -v STRVAL STRVAL, --strvals STRVAL STRVAL
                        A pair of values before/after anonymized in STRING format.
  -x HEXVAL HEXVAL, --hexvals HEXVAL HEXVAL
                        A pair of values before/after anonymized in HEX format.
```

## Examples

Replace [MCC/MNC information](https://github.com/wmnsk/mccmnc_scraper) in Diameter packets.  
This example is expected to work on IMSI (in User-Name AVP or others if any) and Host/Realm.

```shell-session
$ python anon_pcap.py -s path/to/src.pcap -d path/to/dst.pcap \
    -v 440000123456789 999990123456789 \
    -v epc.mnc000.mcc440.3gppnetwork.org epc.mnc999.mcc999.3gppnetwork.org
```

Replace source/destination Global Titles and IMSI in telco protocols (with BCD encoding).
Note that you don't have to specify the swapped hex values in this case.

```shell-session
$ python anon_pcap.py -s path/to/src.pcap -d path/to/dst.pcap \
    -v 441481000001 441481009999 \ # Some E.164 value
    -v 126800000001 126800009999 \ # Some E.164 value
    -v 23455000000001 23455000009999  # Some IMSI (E.212) value
```

Replace MAC/IP addresses in any packets.  
They can only be replaced when specified in HEX string with "-x" keyword.

```shell-session
$ python anon_pcap.py -s path/to/src.pcap -d path/to/dst.pcap \
    -x 080042000001 080042ffffff \ # MAC Address in hex #1: "08:00:42:00:00:01" to "08:00:42:ff:ff:ff"
    -x 080042000002 080042999999 \ # MAC Address in hex #2: "08:00:42:00:00:02" to "08:00:42:99:99:99"
    -x deadbeef 6f6f6f6f # IP Address in hex #1: "222.173.190.239" to "111.111.111.111"
    -x beefdead dededede # IP Address in hex #2: "190.239.222.173" to "222.222.222.222"
```

## Author

Yoshiyuki Kurauchi ([GitHub](https://github.com/wmnsk/) / [Twitter](https://twitter.com/wmnskdmms/))

## License

[MIT](https://github.com/wmnsk/anon_pcap/blob/master/LICENSE)
