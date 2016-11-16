# anon_pcap.py

Mini python script to replace specified value in PCAP file.  
Initially developed with intension of anonymizing sensitive information in PCAP file but this script, as a result, works on any binary.

#### IMPORTANT NOTICE:

* This is still experimental, sometimes results in failure due to some unexpected changes. Please check by yourself(with Wireshark or some good decoder tools) if this script works as you expected or not every time you run, as there may be some unexpected changes in cases like;
  * The same string at some other fields you don't expect, which may cause spoiling the packet format.
  * Some protocols which have the "strict" format may be spoiled when you are ignorant of the specifications.  

* If the fields you want to rewrite is in the lower layer or famous enough to be decoded easily, it's better to use other nice tools such as [dpkt](https://github.com/kbandla/dpkt) or [tcprewrite](http://tcpreplay.synfin.net/wiki/tcprewrite).

* Any pull request will be welcome to improve this easy but stupid script.

## USAGE

```shell-session
# python anon_pcap.py -h
usage: anon_pcap.py [-h] -s SRCPCAP [-d DSTPCAP] [-v STRVAL STRVAL]
                    [-x HEXVAL HEXVAL]

Mini python script to replace specified value in PCAP(or any binary) file.

optional arguments:
  -h, --help            show this help message and exit
  -s SRCPCAP, --srcpcap SRCPCAP
                        Path to the raw PCAP file to be anonymized.
  -d DSTPCAP, --dstpcap DSTPCAP
                        Filename of the anonymized PCAP file.
  -v STRVAL STRVAL, --strvals STRVAL STRVAL
                        A pair of values before/after anonymized in STRING
                        format.
  -x HEXVAL HEXVAL, --hexvals HEXVAL HEXVAL
                        A pair of values before/after anonymized in HEX
                        format.
```

## EXAMPLE

Anonymize MCC/MNC(Country/Operator) information in Diameter packets.  
This is expected to work on IMSI(in User-Name AVP or others if any) and Host/Realm.

```shell-session
# python anon_pcap.py -s path/to/src.pcap -d path/to/dst.pcap \
-v 440000123456789 999990123456789 \
-v epc.mnc000.mcc440.3gppnetwork.org epc.mnc999.mcc999.3gppnetwork.org
```

Anonymize source/destination Global Titles and IMSI, and changes MAC/IP addresses.  
MAC/IP can only be replaced when specified as HEX string with "-x" keyword.

```shell-session
# python anon_pcap.py -s path/to/src.pcap -d path/to/dst.pcap \
-v 441481000001 441481009999 \ # Src GT(E.164)
-v 126800000001 126800009999 \ # Dst GT(E.164)
-v 23455000000001 23455000009999 \ # IMSI(E.212)
-x 080042000001 080042ffffff \ # MAC Address in hex #1: "08:00:42:00:00:01" to "08:00:42:ff:ff:ff"
-x 080042000002 080042999999 \ # MAC Address in hex #2: "08:00:42:00:00:02" to "08:00:42:99:99:99"
-x deadbeef 6f6f6f6f # IP Address in hex #1: "222.173.190.239" to "111.111.111.111"
-x beefdead dededede # IP Address in hex #2: "190.239.222.173" to "222.222.222.222"

```

## NOTES

In some kind of "legacy" protocol, we sometimes need to be sure of its endiannes. For instance, the IMSI(E.212 number) "440980123456789" in SS7/SIGTRAN PCAP is written as "44900821436587f9" in hexstream.  
Currently, this script is tested on the following values in SIGTRAN packets and confirmed to work. Please let me know if you had the unexpected results.

| Fields | Human Readable | Actual Hex | Notes |
| --- | --- | --- | --- |
| IMSI | 440980123456789 | 44900821436587f9 | The last digit is filled with 'f' |
| MSISDN | 81901234567 | 1809214365f7 | The last digit is filled with 'f' when the length is odd |
| Global Title | 81901234567 | 180921436507 | The last digit is filled with '0' when the length is odd |


## AUTHOR

Yoshiyuki Kurauchi ([GitHub](https://github.com/wmnsk/))

## LICENSE

[MIT](https://github.com/wmnsk/anon_pcap/blob/master/MIT.md)
