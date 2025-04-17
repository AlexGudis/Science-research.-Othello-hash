import networkx as nx
from networkx.algorithms import bipartite
from math import log2, ceil
import matplotlib.pyplot as plt
import hashlib
import random
from common import Info

hash_functions = [hashlib.sha1, hashlib.sha224, hashlib.sha256,
    hashlib.sha384, hashlib.sha3_512, hashlib.sha512]


class Othello:
    def __init__(self, ma, mb, ha, hb, a, b):
        self.ma = ma  # The size of bit array a
        self.mb = mb  # The size of bit array b
        self.ha = ha  # Hash function for array a
        self.hb = hb  # Hash function for array a
        self.hash_size = self.ma
        self.g = nx.Graph()  # Bipartite graph G. It's empty from the start
        self.a = a  # Bit array a
        self.b = b  # Bit array b

        print(
            f'Generated Othello structure with ma={ma}, mb={mb}, hash_size={self.hash_size}')

    def search(self, key):
        info = Info(type='oth.search')

        """Found a value (dest port) for key in MAC-VLAN table"""
        i = int.from_bytes(self.ha(key.encode()).digest()) % self.hash_size
        j = int.from_bytes(self.hb(key.encode()).digest()) % self.hash_size
        info.hash += 2
        info.memory += 2
        return self.a[i] ^ self.b[j], info

    def check_cycle(self):
        """Checks if any cycle exists in graph g"""
        try:
            nx.find_cycle(self.g)
            return True
        except nx.exception.NetworkXNoCycle:
            return False

    def generate_edges(self, table):
        """Генерация рёбер двудольного графа с классами рёбер"""
        edges = set()  # Список рёбер
        left_nodes = set()
        right_nodes = set()
        check_cycl = False

        info = Info()

        for k, v in table.items():
            # Генерируем номера узлов через хеши
            left_node = int.from_bytes(
                self.ha(k.encode()).digest()) % self.hash_size
            right_node = int.from_bytes(
                self.hb(k.encode()).digest()) % self.hash_size
            
            info.hash += 2

            # Узлы без классов
            left_node_sig = f"{left_node}_L"
            right_node_sig = f"{right_node}_R"

            if (left_node_sig, right_node_sig, '1') in edges or (left_node_sig, right_node_sig, '0') in edges:
                #print('pipipipi')
                check_cycl = True

            #print(k,left_node_sig, right_node_sig, str(v))

            # Добавляем рёбра с атрибутом класса
            edges.add((left_node_sig, right_node_sig, str(v)))

            # Добавляем узлы без классов
            left_nodes.add(left_node_sig)
            right_nodes.add(right_node_sig)

        return edges, sorted(left_nodes, reverse=True), sorted(right_nodes, reverse=True), check_cycl, info

    def draw_graph(self):
        """Функция рисует граф с раскрашенными рёбрами"""
        left_nodes = [n for n, d in self.g.nodes(
            data=True) if d["bipartite"] == 0]
        right_nodes = [n for n, d in self.g.nodes(
            data=True) if d["bipartite"] == 1]
        left_nodes = sorted(left_nodes, reverse=True)
        right_nodes = sorted(right_nodes, reverse=True)
        node_colors = [self.g.nodes[node]["color"] for node in self.g.nodes]
        edge_colors = ["green" if data['edge_class'] ==
            '1' else "blue" for u, v, data in self.g.edges(data=True)]

        pos = nx.bipartite_layout(self.g, left_nodes)

        plt.figure(figsize=(8, 5))
        nx.draw(self.g, pos, with_labels=True, node_color=node_colors,
                edge_color=edge_colors, width=2, font_color="red")

        plt.show()

    '''def check_edges_colors(self):
        "Позволяет посмотреть на узлы, ребра, их классы"
        cnt = 0
        for u, v, data in self.g.edges(data=True):
            print(f"{cnt}: Ребро {u} - {v}, Класс: {data['edge_class']}")
            cnt += 1
    '''
    
    def recolor_both_gray(self, t_k, u, v, i, j):
        self.a[i] = 0
        self.b[j] = t_k
        self.g.nodes[u]['color'] = "white"
        if t_k:
            self.g.nodes[v]['color'] = "black"
        else:
            self.g.nodes[v]['color'] = "white"

    def recolor_not_gray(self, t_k, u, v, i, j):
        if self.g.nodes[u]['color'] != "gray": # which means that a[i] is set
            self.b[j] = self.a[i] ^ t_k
            if self.b[j]:
                self.g.nodes[v]['color'] = 'black'
            else:
                self.g.nodes[v]['color'] = 'white'
        else: # which means that b[j] is set
            self.a[i] = self.b[j] ^ t_k
            if self.a[i]:
                self.g.nodes[u]['color'] = 'black'
            else:
                self.g.nodes[u]['color'] = 'white'


    def recolor_dfs(self, dfs_edges, info):
        for u, v in dfs_edges:
            u_indexes = u.split('_')
            v_indexes = v.split('_')
            t_k = int(self.g[u][v]['edge_class'])
            i, j = int(u_indexes[0]), int(v_indexes[0])
            if self.g.nodes[u]['color'] == "gray" and self.g.nodes[v]['color'] == "gray":
                #print('Both gray')
                self.recolor_both_gray(t_k, u, v, i, j)

            elif self.g.nodes[u]['color'] != "gray" or self.g.nodes[v]['color'] != "gray":
                #print('One of them are not gray')
                self.recolor_not_gray(t_k, u, v, i, j) 
            
            info.memory += 2
            #print(u, v)
            #self.draw_graph()
        return info


    def recolor(self, info=None):
        if info is None:
            info = Info()

        components = list(nx.connected_components(self.g))
        all_dfs_edges = []
        for component in components:
            subgraph = self.g.subgraph(component)
            start_node = next(iter(component))  # Берем любую вершину в компоненте
            dfs_edges = list(nx.edge_dfs(subgraph, source=start_node))
            all_dfs_edges.extend(dfs_edges)

        
        all_dfs_edges = [(u, v) if u.endswith("_L") else (v, u) for u, v in all_dfs_edges]
        #print(all_dfs_edges, len(all_dfs_edges))

        info = self.recolor_dfs(all_dfs_edges, info)
        
        return info

    def construct(self, table):
        """Create and fill the whole structure of Othello based on MAC-VLAN table"""
        info = Info(type='oth_construct')

        #phase 1
        cycle = True
        while cycle:
            print('START or cycle found')
            # Выбираем каждый раз две новые различные хеш-функции из некоторого множества хеш-функций
            self.ha, self.hb = random.sample(hash_functions, 2)
            self.g.clear()

            edges, left_nodes, right_nodes, cycle, info_check = self.generate_edges(table)
            info.hash += info_check.hash

            if cycle:
                #print(edges)
                print('Cycle in edges found => switching hash func')
                continue

            if len(edges) != len(table):
                print('Double found!!')
                continue

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
            
            # Отрисовка графа
            '''self.draw_graph()'''

            # Проверка графа на циклы
            cycle = self.check_cycle()

        #print(self.g.edges)

        #phase 2. traversal
        # Полный обход всех рёбер и перекраска вершин по правилам
        info_check = self.recolor()
        info.hash += info_check.hash
        info.memory += info_check.memory
        
        # Отрисовка графа
        '''self.draw_graph()'''

        return info


    def insert(self, table, k, v):
        info = Info(type='oth.insert')
        """Insert a key into Othello structure"""
        "Нужно передавать имеющуюся таблицу на случай невозможности добавить ключ и необходимости перестроения всей структуры"
        
        '''print('Current graph')
        self.draw_graph()'''


        # Генерируем номера узлов через хеши
        left_node = int.from_bytes(self.ha(k.encode()).digest()) % self.hash_size
        right_node = int.from_bytes(self.hb(k.encode()).digest()) % self.hash_size
        info.hash += 2

        left_node_sig = f"{left_node}_L"
        right_node_sig = f"{right_node}_R"

        '''print(f'We are gonna add ребро {left_node_sig} - {right_node_sig}, класс = {v}')'''
        left_not_in = False
        right_not_in = False

        # 3. Добавляем вершины в граф (если их ещё нет)
        if left_node_sig not in self.g:
            left_not_in = True
            self.g.add_node(left_node_sig, bipartite=0, color="gray")
        if right_node_sig not in self.g:
            right_not_in = True
            self.g.add_node(right_node_sig, bipartite=1, color="gray")
        
        self.g.add_edge(left_node_sig, right_node_sig, edge_class=v)

        '''self.draw_graph()'''

        #print([self.g.nodes[node] for node in self.g.nodes])

        u_indexes = left_node_sig.split('_')
        v_indexes = right_node_sig.split('_')
        t_k = int(v)
        i, j = int(u_indexes[0]), int(v_indexes[0])

        # case 1 - cycle
        # Или мы добавляем ребро, которое уже есть в графе, значит, возникает цикл длины 2
        if self.check_cycle() or (left_not_in == False and right_not_in == False):
            print('RECONSTRUCT. Oh shit, make it again...')
            info_check = self.construct(table | {k:v})
            info.hash += info_check.hash
            info.memory += info_check.memory
        elif left_not_in and right_not_in: # case - просто новая компонента связности в графе
            self.recolor_both_gray(t_k, left_node_sig, right_node_sig, i, j)
            info.memory += 2
            #print('Case both')
        elif left_not_in or right_not_in: # новая вершина в существующей компоненте связности
            self.recolor_not_gray(t_k, left_node_sig, right_node_sig, i, j)
            info.memory += 2
            #print('Case one')
        #elif int(self.g[right_node_sig][left_node_sig]['edge_class']) != t_k: # Новое ребро в существующей компоненте связности и при этом обе вершины уже существуют и при этом класс ребра некорректный
        else:
            print(f'Oh man, recolor it...')
            print(self.g[right_node_sig][left_node_sig])

            dfs_edges = []
            for component in nx.connected_components(self.g):
                if left_node_sig in component or right_node_sig in component:
                    # Подграф с только этой компонентой
                    subgraph = self.g.subgraph(component)
                    dfs_edges = subgraph.edges()
                    break
                    
            #print(dfs_edges)
            info = self.recolor_dfs(dfs_edges, info)

        '''self.draw_graph()'''

        return info


    def addX(self, k):
        """Input key into X"""
        pass

    def addY(self, k):
        """Input key into Y"""
        pass

    def alter(self, k):
        """Change key value place"""
        pass

    def delete(self, k):
        """Delete key from Othello structure"""
        info = Info('oth.delete')

        '''self.draw_graph()'''

        # Генерируем номера узлов через хеши
        left_node = int.from_bytes(self.ha(k.encode()).digest()) % self.hash_size
        right_node = int.from_bytes(self.hb(k.encode()).digest()) % self.hash_size
        info.hash += 2
        info.memory += 0

        # Узлы без классов
        #print(self.g.edges)
        #print(k)
        left_node_sig = f"{left_node}_L"
        right_node_sig = f"{right_node}_R"
        #print(f'DELETE {left_node_sig} {right_node_sig} with key {k}')
        
        self.g.remove_edge(left_node_sig, right_node_sig)
        
        '''self.draw_graph()'''
        return info