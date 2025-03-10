import othello
import binascii
import json
import bitarray
from math import log2, ceil
import zlib
import hashlib


with open('mac_vlan_mapping.json', 'r') as JSON:
       json_dict = json.load(JSON)
n = len(json_dict)
a = bitarray.bitarray(int(n * 2))
b = bitarray.bitarray(int(n * 2))
ma = len(a)
mb = len(b)
ha = hashlib.md5
hb = hashlib.sha256


oth = othello.Othello(ma, mb, ha, hb, a, b)
oth.construct(json_dict)
