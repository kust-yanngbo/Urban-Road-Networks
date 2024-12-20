# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 01:27:51 2024

@author: Li Yuanbiao
"""

import igraph as ig

def cycle_detection(G):
    # 探测网络中的圈结构
    # 输出为边序号，需要转换为节点
    cycle_list = ig.GraphBase.minimum_cycle_basis(G)
    # 存储圈节点
    cycle_nodes_list = []
    for cycle in cycle_list:
        c_nodes = []
        for edge in cycle:
            c_nodes.append(G.es[edge].source)
            c_nodes.append(G.es[edge].target)
        cycle_nodes_list.append(sorted(list(set(c_nodes))))
    return cycle_nodes_list

graph = 'bj_1'
graph_path = 'data/RoadToNetwork/' + graph + '.graphml'
cycle_path = 'data/Cycles/' + graph + '_cycles.txt'

G = ig.Graph.Read_GraphML(graph_path)

# 处理网络：去除自环、孤立节点
G.simplify(combine_edges="first")
G.delete_vertices(G.vs.select(_degree=0))

cycle_nodes_list = cycle_detection(G)
with open(cycle_path, 'w') as f:  
    for sublist in cycle_nodes_list:  
        f.write(f'{", ".join([str(i) for i in sublist])}\n')