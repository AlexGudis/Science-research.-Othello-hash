import numpy as np
from math import ceil, log2
from collections import defaultdict

from blank_method import Info
from function import HashFunction


class DefaultHashing:
    def __init__(self, key_size, array_size, keys):
        self.array_size = array_size
        self.hash_size = ceil(log2(array_size))
        self.array = defaultdict(list)
        self.keys = keys
        self.records = 0
        self.key_size = key_size
        self.hash_fun = HashFunction(key_size, self.hash_size, self.array_size)

    def search(self, key):
        info = Info(
            type='dfh.search',
            records=self.records,
            key_inc=key in self.keys
        )
        info.hash += 1
        idx = self.hash_fun(key)
        info.memory += 1
        lst = self.array[idx]
        if not lst:
            info.failed = True
            return info
        for i in lst:
            info.memory += 1
            if i == key:
                return info
            info.memory += 1
        info.failed = True
        return info

    def insert(self, key):
        info = Info(
            type='dfh.insert',
            records=self.records,
            key_inc=key in self.keys
        )
        info.hash += 1
        idx = self.hash_fun(key)
        info.memory += 1
        lst = self.array[idx]
        for i in lst:
            info.memory += 1
            if i == key:
                info.memory += 1
                return info
            info.memory += 1
        info.memory += 3
        lst.append(key)
        return info

    def delete(self, key):
        info = Info(
            type='dfh.delete',
            records=self.records,
            key_inc=key in self.keys
        )
        info.hash += 1
        idx = self.hash_fun(key)
        info.memory += 1
        lst = self.array[idx]
        if not lst:
            info.failed = True
            return info
        for i in lst:
            info.memory += 1
            if i == key:
                info.memory += 3
                lst.remove(key)
                return info
            info.memory += 1
        info.failed = True
        return info