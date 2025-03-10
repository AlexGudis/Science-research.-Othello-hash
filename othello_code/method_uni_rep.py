from random import shuffle
from collections import deque

from blank_method import BlankMethod, Info
from function import HashFunction


class UniversalReplacement(BlankMethod):
    def __init__(self, key_size, array_size, hash_num):
        super().__init__(array_size)
        self.key_size = key_size
        self.hash_funs = deque(HashFunction(key_size, self.hash_size, array_size) for _ in range(hash_num))

    def search(self, key):
        info = Info(
            type='uni.search',
            records=self.records,
            key_inc=key in self.array
        )
        for h in self.hash_funs:
            info.hash += 1
            info.memory += 1
            code = h(key)
            if self.array[code] == key:
                return info
        info.failed = True
        return info

    def insert(self, key):
        info = Info(
            type='uni.insert',
            records=self.records,
            key_inc=key in self.array
        )
        place = None
        for tries in range(100):
            if tries % 10:
                shuffle(self.hash_funs)
            for h in self.hash_funs:
                info.hash += 1
                info.memory += 1
                code = h(key)
                if self.array[code] == key:
                    info.memory += 1
                    return info
                if self.array[code] == 0 and place is None:
                    place = code

            if place is not None:
                self.records += 1
                self.array[place] = key
                info.memory += 1
                return info

            info.memory += 4
            key, self.array[code] = self.array[code], key
            self.hash_funs.rotate()
        info.error = True
        return info

    def delete(self, key):
        info = Info(
            type='uni.delete',
            records=self.records,
            key_inc=key in self.array
        )
        for h in self.hash_funs:
            info.hash += 1
            info.memory += 1
            code = h(key)
            if self.array[code] == key:
                info.memory += 1
                self.array[code] = 0
                self.records -= 1
                return info
        info.failed = True
        return info
