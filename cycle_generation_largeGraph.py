# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:53:32 2024

@author: Li Yuanbiao
"""
import igraph as ig
import random

def cycle_detection(G):
    # 探测网络中的圈结构
    # 输出为边序号，需要转换为节点
    cycle_list = ig.GraphBase.minimum_cycle_basis(G)
    # 存储圈节点
    cycle_nodes_list = []
    for cycle in cycle_list:
        c_nodes = []
        for edge in cycle:
#             c_nodes.append(G.es[edge].source)
#             c_nodes.append(G.es[edge].target)            
            c_nodes.append(G.vs[G.es[edge].source]['label'])
            c_nodes.append(G.vs[G.es[edge].target]['label'])

        cycle_nodes_list.append(sorted(list(set(c_nodes))))
    return cycle_nodes_list

graph = 'km_1'
graph_path = 'data/RoadToNetwork/' + graph + '.graphml'
cycle_path = 'data/Cycles/' + graph + '_cycles.txt'


G = ig.Graph.Read_GraphML(graph_path)

# 处理网络：去除自环、孤立节点
G.simplify(combine_edges="first")
G.delete_vertices(G.vs.select(_degree=0))
for v in G.vs:
    G.vs[v.index]['label'] = v.index
node_list = [v.index for v in G.vs]
node_set = set(node_list)
num = 0
selected_node = []
while num < 500:
    # 定义一个变量，用于记录是否满足条件
    flage = False
    while not flage:
        random_node = random.choice(node_list)
        if random_node not in selected_node:
            flage1 = False
            orde = 50
            while not flage1:
                neighborhood = G.neighborhood(random_node, order=orde)
            if len(neighborhood) > 10000 and len(neighborhood) < 15000:
                selected_node.append(random_node)
                flage = True
                num += 1
                # 复制一个新的网络
                G_new = G.copy()
                # 不在邻居节点中的节点删除
                remove_node = node_set - set(neighborhood)
                remove_node = list(remove_node)
                G_new.delete_vertices(remove_node)
                
                cycle_path = 'data/Cycles/' + graph + '_cycles_'+str(num)+'.txt'
                cycle_nodes_list = cycle_detection(G_new)
                with open(cycle_path, 'w') as f:  
                    for sublist in cycle_nodes_list:  
                        f.write(f'{", ".join([str(i) for i in sublist])}\n')
            
