# anon_pcap.py

Mini python script to replace specified value in PCAP(or any binary) file.  
Initially developed with intension of anonymizing sensitive information in PCAP file but this script, as a result, works on any binary.

Currently IP address is not supported but would be implemented some day...

#### IMPORTANT NOTICE:

* This is still experimental, sometimes results in failure due to the change in the length of the field.

* Please check by yourself if this script works right or not every time you run, as there may be the same string at some fields you don't expect, which may cause spoiling the packet format.

## USAGE

```shell-session
# python anon_pcap.py -h
usage: anon_pcap.py [-h] -s SRCPCAP [-d DSTPCAP] [-v VALUES VALUES]

Mini python script to replace specified value in PCAP(or any binary) file.

optional arguments:
  -h, --help            show this help message and exit
  -s SRCPCAP, --srcpcap SRCPCAP
                        Path to the raw PCAP file to be anonymized.
  -d DSTPCAP, --dstpcap DSTPCAP
                        Filename of the anonymized PCAP file.
  -v VALUE VALUE, --values VALUE VALUE
                        A pair of values before/after anonymized.
```

## EXAMPLE

Anonymize MCC/MCC(Country/Operator) information on Diameter packets.  
This is expected to work on IMSI(in User-Name AVP or others if any) and Host/Realm.

```shell-session
# python anon_pcap.py -s path/to/some.pcap -v 440000123456789 999990123456789 -v epc.mnc000.mcc440.3gppnetwork.org epc.mnc999.mcc999.3gppnetwork.org
Replaced "440000123456789" as "999990123456789"
Replaced "epc.mnc000.mcc440.3gppnetwork.org" as "epc.mnc999.mcc999.3gppnetwork.org"
```

Anonymize the website you accessed. (**Currently, this doesn't work actually...**)

```shell-session
# python anon_pcap.py -s samples/httpsample.pcap.pcapng -v www.apple.com www.somesite.com -v /jp/macbook-pro/ /path/to/somepage/ -d samples/http_anon.pcap Replaced "www.apple.com" as "www.somesite.com"
Replaced "/jp/macbook-pro/" as "/path/to/somepage/"
```

## AUTHOR

Yoshiyuki Kurauchi ([GitHub](https://github.com/wmnsk/))

## LICENSE

[MIT](http://)
