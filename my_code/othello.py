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
        i = int.from_bytes(self.ha(key.encode()).digest()) % self.hash_size
        j = int.from_bytes(self.hb(key.encode()).digest()) % self.hash_size
        return self.a[i] ^ self.b[j]

    def check_cycle(self):
        "Checks if any cycle exists in graph g"
        try:
            nx.find_cycle(self.g)
            return True
        except nx.exception.NetworkXNoCycle:
            return False
        
    def generate_edges(self, table):
        """Генерация рёбер двудольного графа с классами рёбер"""
        edges = []  # Список рёбер
        left_nodes = set()
        right_nodes = set()

        for k, v in table.items():
            # Генерируем номера узлов через хеши
            left_node = int.from_bytes(self.ha(k.encode()).digest()) % self.hash_size
            right_node = int.from_bytes(self.hb(k.encode()).digest()) % self.hash_size

            # Узлы без классов
            left_node_sig = f"{left_node}_L"
            right_node_sig = f"{right_node}_R"

            # Добавляем рёбра с атрибутом класса
            edges.append((left_node_sig, right_node_sig, str(v)))

            # Добавляем узлы без классов
            left_nodes.add(left_node_sig)
            right_nodes.add(right_node_sig)

        return edges, sorted(left_nodes, reverse=True), sorted(right_nodes, reverse=True)


    def draw_graph(self, left_nodes, right_nodes, node_colors):
        """Функция рисует граф с раскрашенными рёбрами"""
        
        nx.set_node_attributes(self.g, {node: 0 for node in left_nodes}, "bipartite")
        nx.set_node_attributes(self.g, {node: 1 for node in right_nodes}, "bipartite")

        pos = nx.bipartite_layout(self.g, left_nodes)

        # Цвета рёбер по классу
        edge_colors = ["green" if data['edge_class'] == '1' else "blue" for u, v, data in self.g.edges(data=True)]

        plt.figure(figsize=(8, 5))
        nx.draw(self.g, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, width=2, font_color="red")
        
        plt.show()


    def dfs_edges(self, graph, start, visited_edges, edge_order):
        """Итеративный DFS-обход рёбер"""
        stack = [start]
        visited_nodes = set()

        while stack:
            node = stack.pop()
            if node not in visited_nodes:
                visited_nodes.add(node)
                for neighbor in graph.neighbors(node):
                    edge = tuple(sorted((node, neighbor)))  # Упорядочиваем ребро
                    if edge not in visited_edges:
                        visited_edges.add(edge)
                        edge_order.append(edge)
                        stack.append(neighbor)

    def check_edges_colors(self):
        "Позволяет посмотреть на узлы, ребра, их классы"
        cnt = 0
        for u, v, data in self.g.edges(data=True):
            print(f"{cnt}: Ребро {u} - {v}, Класс: {data['edge_class']}")
            cnt += 1


    def construct(self, table):
        "Create and fill the whole structure of Othello based on MAC-VLAN table"
        
        #phase 1
        cycle = True
        edges = []
        node_colors = dict()
        while cycle:
            print('START or cycle found')
            # вот здесь надо выбирать новые хеш-функции из некоторого набора

            self.g.clear()  # очищаем граф перед построением
            edges, left_nodes, right_nodes = self.generate_edges(table)

            # Добавляем вершины и ребра в граф
            self.g.add_nodes_from(left_nodes, bipartite=0)
            self.g.add_nodes_from(right_nodes, bipartite=1)

            # Добавляем рёбра с атрибутом "класс"
            for u, v, edge_class in edges:
                self.g.add_edge(u, v, edge_class=edge_class)


            # Изначально все вершины покрашены в серый цвет
            node_colors = {node: "gray" for node in left_nodes}  # Левые вершины
            node_colors.update({node: "gray" for node in right_nodes})  # Правые вершины
            nx.set_node_attributes(self.g, node_colors, "color")
            colors = [self.g.nodes[node]["color"] for node in self.g.nodes]

            # Отрисовка графа
            self.draw_graph(left_nodes, right_nodes, colors)

            # Проверка графа на циклы
            cycle = self.check_cycle()

        #print(edges)

        #phase 2. DFS traversal
        # Полный обход графа, включая все компоненты
        visited_edges = set()
        dfs_edge_order = []
        for node in self.g.nodes:
            if all(tuple(sorted((node, neighbor))) in visited_edges for neighbor in self.g.neighbors(node)):
                continue  # Пропускаем вершины, если все рёбра уже посещены
            self.dfs_edges(self.g, node, visited_edges, dfs_edge_order)
        
        self.check_edges_colors()
        print(f'DFS order = {dfs_edge_order}')


        # Обход рёбер и перекраска вершин по правилам
        for u, v in dfs_edge_order:
            u_indexes = u.split('_')
            v_indexes = v.split('_')
            #print(u_indexes)
            t_k = int(self.g[u][v]['edge_class'])
            i, j = int(u_indexes[0]), int(v_indexes[0])
            if node_colors[u] == "gray" and node_colors[v] == "gray":
                #print('Both gray')
                # if all undef then a[i] = 0, b[j] = t(k)
                self.a[i] = 0
                self.b[j] = t_k
                node_colors[u] = "white"
                if t_k:
                    node_colors[v] = "black"
                else:
                    node_colors[v] = "white"


            elif node_colors[u] != "gray" or node_colors[v] != "gray":
                #print('One of them are not gray')
                if node_colors[u] != "gray": # which means that a[i] is set
                    self.b[j] = self.a[i] ^ t_k
                    if self.b[j]:
                        node_colors[v] = 'black'
                    else:
                        node_colors[v] = 'white'
                else: # which means that b[j] is set
                    self.a[i] = self.b[j] ^ t_k
                    if self.a[i]:
                        node_colors[u] = 'black'
                    else:
                        node_colors[u] = 'white'
            
                
        nx.set_node_attributes(self.g, node_colors, "color")
        colors = [self.g.nodes[node]["color"] for node in self.g.nodes]
        
        # Отрисовка графа
        self.draw_graph(left_nodes, right_nodes, colors)


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