from othello import Othello
import bitarray
import hashlib

class POG:
    def __init__(self):
        self.group = []


    def search(self, key):
        
        ans = ''
        for i in range(len(self.group)):
            ans += str(self.group[i].search(key))

        #print(f'FOUND = {ans}')

        return int(ans, 2)

    def generate_table(self, table, cnt, i):
        specific_table = table.copy()
        for k, v in specific_table.items():
            new_v = bin(int(v))[2:]
            if len(new_v) != cnt:
                new_v = '0' * (cnt - len(new_v)) + new_v
                
            #print(new_v, len(new_v))
            #print(f'Current othello = {i}, t_k for key {k} and value {bin(int(v))[2:]} is {new_v[i]}')

            specific_table[k] = new_v[i]
        return specific_table


    def construct(self, table):

        # Определяем число Отелло структур
        max_port = max(int(v) for k,v in table.items())
        #print(max_port)
        cnt = len(bin(max_port)[2:])
        #print(cnt)

        for i in range(cnt):
            n = len(table)
            a = bitarray.bitarray(int(n * 1.33))
            b = bitarray.bitarray(int(n * 1.33))
            ma = len(a)
            mb = len(b)
            ha = hashlib.sha3_512
            hb = hashlib.sha256

            oth = Othello(ma, mb, ha, hb, a, b)

            specific_table = self.generate_table(table, cnt, i)
            
            print(specific_table)

            oth.construct(specific_table)

            self.group.append(oth)

    def insert(self, table, k, v):
        cnt = len(self.group)

        new_v = bin(int(v))[2:]
        if len(new_v) != cnt:
            new_v = '0' * (cnt - len(new_v)) + new_v

        for i in range(cnt):
            self.group[i].insert(table, k, new_v[i])

    def delete(self, k):
        pass