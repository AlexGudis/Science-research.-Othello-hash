import othello
import binascii
import json
import bitarray
from math import log2, ceil
import zlib
import hashlib


def test(oth, json_dict):
    keys = []
    values = []
    for k, v in json_dict.items():
        keys.append(k)
        values.append(v)

    oth.construct(json_dict)
    #print(oth.a)
    #print(oth.b)

    cnt = 0
    for i in range(n):
       key = keys[i]
       ans = oth.search(key)

       #print(ans,json_dict[key])
       if str(json_dict[key]) == str(ans):
              cnt += 1

    return cnt


with open('mac_vlan_mapping.json', 'r') as JSON:
    json_dict = json.load(JSON)

n = len(json_dict)
a = bitarray.bitarray(int(n * 1.33))
b = bitarray.bitarray(int(n * 1.33))
ma = len(a)
mb = len(b)
ha = hashlib.sha3_512
hb = hashlib.sha256


oth = othello.Othello(ma, mb, ha, hb, a, b)

cnt = test(oth, json_dict)

print(f'Correct is {cnt} of {n}')



oth.insert(json_dict, "EC:94:9F:FG:A8:37-2051", "0")
