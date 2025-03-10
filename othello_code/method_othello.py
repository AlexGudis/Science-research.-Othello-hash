import numpy as np
from collections import defaultdict
from math import log2, ceil

from blank_method import BlankMethod, Info
from function import HashFunction


class OthelloMultiplied(BlankMethod):
    def __init__(self, key_size, array_size):
        super().__init__(array_size)
        self.next_place = 0
        self.part_size = int(array_size * 1.3)
        self.hash_size = ceil(log2(self.part_size))
        self.key_size = key_size
        self.hash_fun1, self.hash_fun2 = [HashFunction(key_size, self.hash_size, self.part_size) for _ in range(2)]
        self.ver_array = np.empty(self.part_size * 2, dtype=int)
        self.connections = defaultdict(set)

    def search(self, key):
        info = Info(
            type='oth.search',
            records=self.records,
            key_inc=key in self.array
        )
        info.hash += 2
        u, v = self.hash_fun1(key), self.hash_fun2(key) + self.part_size
        info.memory += 2
        code = self.ver_array[u] ^ self.ver_array[v]
        if code >= self.array_size:
            info.failed = True
            return info
        info.memory += 1
        if self.array[code] == key:
            return info
        info.failed = True
        return info

    def insert(self, key):
        info = Info(
            type='oth.insert',
            records=self.records,
            key_inc=key in self.array
        )
        info.hash += 2
        u, v = self.hash_fun1(key), self.hash_fun2(key) + self.part_size
        if v in self.connections[u]:
            code = self.ver_array[u] ^ self.ver_array[v]
            info.memory += 1
            if self.array[code] == key:
                info.memory += 1
                return info
            info.failed = True
            return info

        visited = {u}
        tmp = self.connections[u]
        while tmp:
            visited.update(tmp)
            tmp = set.union(*(self.connections[i] for i in tmp)) - visited
            if v in tmp:
                info.failed = True
                return info

        self.connections[u].add(v)
        self.connections[v].add(u)

        info.memory += 1
        self.array[self.next_place] = key
        self.records += 1
        info.memory += 2
        x = self.ver_array[u] ^ self.ver_array[v] ^ self.next_place
        for ver in visited:
            info.memory += 1
            self.ver_array[ver] ^= x

        while self.array[self.next_place]:
            info.memory += 1
            self.next_place = (self.next_place + 1) % self.array_size
        return info

    def delete(self, key):
        info = Info(
            type='oth.delete',
            records=self.records,
            key_inc=key in self.array
        )
        info.hash += 2
        u, v = self.hash_fun1(key), self.hash_fun2(key) + self.part_size
        if v not in self.connections[u]:
            info.failed = True
            return info
        info.memory += 2
        code = self.ver_array[u] ^ self.ver_array[v]
        info.memory += 1
        if self.array[code] != key:
            info.failed = True
            return info
        info.memory += 1
        self.records -= 1
        self.array[code] = 0
        self.connections[u].remove(v)
        self.connections[v].remove(u)
        return info
