from time import thread_time
import random as rd
import json

from method_lin_uni import LinearUniversal
from method_uni_rep import UniversalReplacement
from method_othello import OthelloMultiplied


def time_format(seconds):
    s = int(seconds)
    h = s // 3600
    m = (s % 3600) // 60
    s = s % 60
    return f"{h:>4}h {m:>02}m {s:>02}s"


def processing(method, keys, filename):
    ds = []

    key = rd.randrange(1 << 60)
    ds.append(method.insert(key))
    keys.add(key)

    key = rd.randrange(1 << 60)
    ds.append(method.insert(key))
    keys.add(key)

    keys2 = list(keys)

    key = rd.choice(keys2)
    ds.append(method.insert(key))

    while (key := rd.randrange(1 << 60)) in keys: pass
    ds.append(method.search(key))

    key = rd.choice(keys2)
    ds.append(method.search(key))

    while (key := rd.randrange(1 << 60)) in keys: pass
    ds.append(method.delete(key))

    key = rd.choice(keys2)
    ds.append(method.delete(key))
    keys.discard(key)

    with open(filename, 'a') as file:
        for d in ds:
            file.write(json.dumps(d._asdict()))
            file.write('\n')


arr_size = 16000  # 1111111 277777 72222
tbl_size = 250000  # 1000000 250000 65000


def main():
    lin = LinearUniversal(60, arr_size, 10)
    uni = UniversalReplacement(60, arr_size, 20)
    oth = OthelloMultiplied(60, arr_size)
    keys_l = set()
    keys_u = set()
    keys_o = set()
    file_l = f"records{tbl_size}/lin"
    file_u = f"records{tbl_size}/uni"
    file_o = f"records{tbl_size}/oth"

    start = thread_time()
    for n in range(tbl_size):
        if not n % 100:
            print(f"{n:>7} rules in {time_format(thread_time() - start)}")
        processing(lin, keys_l, file_l + f"{n//10000}")
        processing(uni, keys_u, file_u + f"{n//10000}")
        processing(oth, keys_o, file_o + f"{n//10000}")


if __name__ == "__main__":
    main()