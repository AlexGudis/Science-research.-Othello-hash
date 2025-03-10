import networkx as nx
from networkx.algorithms import bipartite
from math import log2, ceil
import matplotlib.pyplot as plt
import hashlib

hash_functions = [hashlib.sha1, hashlib.sha224, hashlib.sha256, hashlib.sha384, hashlib.sha3_512, hashlib.sha512]

class Othello:
    def __init__(self, ma, mb, ha, hb, a, b):
        self.ma = ma # The size of bit array a
        self.mb = mb # The size of bit array b
        self.ha = ha # Hash function for array a
        self.hb = hb # Hash function for array a
        self.hash_size = self.ma
        self.g = nx.Graph() # Bipartite graph G. It's empty from the start
        self.a = a # Bit array a
        self.b = b # Bit array b

        print(f'Generated Othello structure with ma={ma}, mb={mb}, hash_size={self.hash_size}')

    def search(self, key):
        "Found a value (dest port) for key in MAC-VLAN table"
        return self.a[self.ha(key)] ^ self.b[self.hb(key)]

    def check_cycle(self):
        "Checks if any cycle exists in graph g"
        try:
            nx.find_cycle(self.g)
            return True
        except nx.exception.NetworkXNoCycle:
            return False
        
    def generate_edges(self, table):
        "A function to generete edges of a bipartite graph"
        e = [] # a list of edges
        for k,v in table.items():
            left_node = int.from_bytes(self.ha(k.encode()).digest()) % self.hash_size
            right_node = int.from_bytes(self.hb(k.encode()).digest()) % self.hash_size
            e.append((str(left_node) + '_L', str(right_node) + '_R'))
        return e

    def draw_graph(self, left_nodes, right_nodes):
        nx.set_node_attributes(self.g, {node: 0 for node in left_nodes}, "bipartite")
        nx.set_node_attributes(self.g, {node: 1 for node in right_nodes}, "bipartite")

        # Построение правильного расположения
        pos = nx.bipartite_layout(self.g, left_nodes)

        # Визуализация
        plt.figure(figsize=(8, 5))
        nx.draw(self.g, pos, with_labels=True, node_color=['lightblue' if node in left_nodes else 'lightgreen' for node in self.g.nodes], edge_color="black")
        plt.show()


    def construct(self, table):
        "Create and fill the whole structure of Othello based on MAC-VLAN table"
        
        #phase 1
        cycle = True
        edges = []
        while cycle:
            # вот здесь надо выбирать новые хеш-функции из некоторого набора

            self.g.clear()  # очищаем граф перед построением
            edges = self.generate_edges(table)

            left_nodes = {el[0] for el in edges}
            right_nodes = {el[1] for el in edges}

            self.g.add_nodes_from(left_nodes, bipartite=0)
            self.g.add_nodes_from(right_nodes, bipartite=1)
            self.g.add_edges_from(edges)
            print(edges)
            self.draw_graph(left_nodes, right_nodes)
            cycle = self.check_cycle()

        print(edges)


        #phase 2. DFS traversal
        

    def insert(self, key):
        "Insert a key into Othello structure"
        pass


    def addX(self, key):
        "Input key into X"
        pass

    def addY(self, key):
        "Input key into Y"
        pass

    def alter(self, key):
        "Change key value place"
        pass

    def delete(self, key):
        "Delete key from Othello structure"
        pass