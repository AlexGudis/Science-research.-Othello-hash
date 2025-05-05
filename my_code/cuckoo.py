import hashlib
import random

hash_functions = [hashlib.sha1, hashlib.sha224, hashlib.sha256,
                  hashlib.sha384, hashlib.sha3_512, hashlib.sha512]


load = 35


class Node(object):
    def __init__(self, k, d):
        self.key  = k 
        self.data = d
    def __str__(self):
        return "(" + str(self.key) + ", " + str(self.data) + ")"



class HashTab():
    def __init__(self, size):
        self.array1 = [None] * (size // 2)  # create 2 arrays, both half the length of size
        self.array2 = [None] * (size // 2)
        self.hash1, self.hash2 = random.sample(hash_functions, 2) # random hash func for each array of the cuckoo
        self.keys_cnt = 0                 # total number of nodes 
        self.size = size                  # total size of hash table (both lists in summary)

    # return current number of keys in table    
    def __len__(self): return self.keys_cnt


    def test_corr(self):
        missing = 0
        for i in range(load):
            ans = self.find(str(i)+"foobarbaz")
            if ans == None or ans != i:
                #print(i, "Couldn't find key", str(i)+"foobarbaz")
                missing += 1
            
        print("There were", missing, "records missing from Cuckoo")


    # insert and return true, return False if the key/data is already there,
    # grow the table if necessary 
    def insert(self, k, d):
        #self.test_corr(40)

        if self.find(k) != None:  return False   # if already there, return False (no duplicates)

        n = Node(k, d)                           # create a new node with key/data

        # increase size of table if necessary 
        # Так как нам нужно достичь загрузки в 90%, то делать этого мы не будем
        #if self.keys_cnt >= (self.size // 2):
        #    self.growHash()
        
        position1, position2 = self.hashFunc(n.key)  # hash
        # start the loop checking the 1st position in table 1
        pos = position1
        table = self.array1

        #       
        for _ in range(5):
            #print('Inserting...')
            
            if table[pos] == None:               # if the position in the current table is empty
                table[pos] = n                   # insert the node there and return True
                self.keys_cnt += 1
                return True
            
            n, table[pos] = table[pos], n       # else, evict item in pos and insert the item
                                                # then deal with the displaced node.

            if pos == position1:                            # if we're checking the 1st table right now, 
                position1, position2 = self.hashFunc(n.key) # hash the displaced node,
                pos = position2                             # and check its 2nd position 
                table = self.array2                  # in the 2nd table (next time through loop)
            else:                               
                position1, position2 = self.hashFunc(n.key) # otherwise, hash the displaced node,
                pos == position1                            # and check the 1st table position. 
                table = self.array1


        # This line will never be executed due to infinite loop above
        
        #self.growHash()               # grow and rehash if we make it here. No grow, we want 90% loadfactor  
        
        #print('REHASH')
        self.rehash(self.size)                           
        self.insert(n.key, n.data)      # deal with evicted item

        return True

    
    def hashFunc(self, s):
        x = int.from_bytes(self.hash1(s.encode()).digest())      # hash twice 
        y = int.from_bytes(self.hash2(s.encode()).digest())
        
        return x % self.size // 2, y % self.size // 2
    



    # return string representation of both tables
    def __str__(self):
        str1 = "Table 1: [ " + str(self.array1[0]) 
        str2 = " Table 2: [ " + str(self.array2[0]) 
        for i in range(1, self.size):
            str1 += ", " + str(self.array1[i])
        str1 += "]"

        for i in range(1, self.size):
           str2 += ", " + str(self.array2[i]) 
        str2 += "]"
        
        return str1 + str2 
    


    # get new hash functions and reinsert everything 
    def rehash(self, size):        
        temp = HashTab(size)    # create new hash tables
        temp.hash1, temp.hash2 = random.sample(hash_functions, 2)   # get new hash functions
        

        # re-hash each item and insert it into the correct position in the new tables
        for i in range(self.size // 2):
            x = self.array1[i]
            y = self.array2[i]
            if x != None:
                #print(f'INSERTING = {x.key}, {x.data}')
                temp.insert(x.key, x.data)
            if y != None:
                #print(f'INSERTING = {y.key}, {y.data}')
                temp.insert(y.key, y.data)

        # save new tables S
        self.array1 = temp.array1
        self.array2 = temp.array2
        self.keys_cnt = temp.keys_cnt
        self.size = temp.size
        self.hash1 = temp.hash1
        self.hash2 = temp.hash2


    # Increase the hash table's size x 2 
    def growHash(self):
        newSize = self.size * 2
        # re-hash each item and insert it into the
        # correct position in the new table
        self.rehash(newSize)
    

    # Return data if there, otherwise return None
    def find(self, k):
        pos1, pos2 = self.hashFunc(k)               # check both positions the key/data
        x = self.array1[pos1]                       # could be in. return data if found.
        y = self.array2[pos2]  

        #try:
        #    print(f'x = {x.key}-{x.value}, y = {y.key}-{y.value} for KEY {k}')   
        #except AttributeError:
        #    pass            
        
        if x != None and x.key == k:  return x.data
        if y != None and y.key == k:  return y.data
    
        # return None if the key can't be found     
        return None
    

    # delete the node associated with that key and return True on success
    def delete(self, k):
        pos1, pos2 = self.hashFunc(k)  
        x = self.array1[pos1]
        y = self.array2[pos2]
        if  x != None and  x.key == k:  self.array1[pos1] = None
        elif y != None and y.key == k:  self.array2[pos2] = None
        else:   return False   # the key wasnt found in either possible position
        self.keys_cnt -= 1 
        return True
    


def test():
    size = load
    missing = 0
    found = 0 
    
    # create a hash table with an initially small number of bukets
    c = HashTab(100)
    
    # Now insert size key/data pairs, where the key is a string consisting
    # of the concatenation of "foobarbaz" and i, and the data is i
    inserted = 0
    find_after = 0
    for i in range(size):
        #print(f'Inserting {i} / {size}') 
        if c.insert(str(i)+"foobarbaz", i):
            inserted += 1

        ans = c.find(str(i)+"foobarbaz")
        if ans == i:
            find_after += 1
        else:
            print(f'ERROR: {str(i)+"foobarbaz"}')
        
    print("There were", inserted, "nodes successfully inserted")
    print(f"Totally correctly inserted = {find_after}")
        
        
    # Make sure that all key data pairs that we inserted can be found in the
    # hash table. This ensures that resizing the number of buckets didn't 
    # cause some key/data pairs to be lost.
    for i in range(size):
        ans = c.find(str(i)+"foobarbaz")
        if ans == None or ans != i:
            #print(i, "Couldn't find key", str(i)+"foobarbaz")
            missing += 1
            
    print("There were", missing, "records missing from Cuckoo")
    
    # Makes sure that all key data pairs were successfully deleted 
    '''for i in range(size): 
           c.delete(str(i)+"foobarbaz")
        
    for i in range(size): 
        ans = c.find(str(i)+"foobarbaz") 
        if ans != None or ans == i: 
            print(i, "Couldn't delete key", str(i)+"foobarbaz") 
            found += 1
    print("There were", found, "records not deleted from Cuckoo") '''



    print("REHASH")
    c.rehash(100)

    for i in range(size):
        ans = c.find(str(i)+"foobarbaz")
        if ans == None or ans != i:
            print(i, "Couldn't find key", str(i)+"foobarbaz")
            missing += 1
            
    print("There were", missing, "records missing from Cuckoo")
    #c.test_corr()

def main():
    test()
    
if __name__ == '__main__':
    main()       

