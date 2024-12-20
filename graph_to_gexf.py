# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:18:02 2024

@author: Li Yuanbiao
"""

import igraph as ig
import networkx as nx
import numpy as np
import collections

# 进行环探测
def cycle_detection(G):
    # 探测网络中的圈结构
    # 输出为边序号，需要转换为节点
    cycle_list = ig.GraphBase.minimum_cycle_basis(G)
    # 存储环节点
    cycle_nodes_list = []
    for cycle in cycle_list:
        c_nodes = []
        for edge in cycle:
            c_nodes.append(G.es[edge].source)
            c_nodes.append(G.es[edge].target)
        cycle_nodes_list.append(sorted(list(set(c_nodes))))
        
    return cycle_nodes_list

# 根据网络结构和环的分布情况计算环度和环率
def cyclesFeature(G, cycles):
    # 生成一个环数量矩阵
    cycles_number_matrix = np.zeros((G.vcount(),G.vcount()))
    for i in range(G.vcount()):
        # 找到含有节点i的环
        cycles_i = []
        for sub_cycles in cycles:
            if i in sub_cycles:
                cycles_i.append(sub_cycles)
        cycles_number_matrix[i][i] = len(cycles_i)
        # 含有节点i的环中其他节点j的数量
        cycles_node = [node for sub_cycles in cycles_i for node in sub_cycles]
        cycles_dict = collections.Counter(cycles_node)
        cycles_num = dict(sorted(cycles_dict.items(), key=lambda x: x[0]))
        for j in cycles_num.keys():
            cycles_number_matrix[i][j] = cycles_num[j]
            cycles_number_matrix[j][i] = cycles_num[j]
        
    # 节点节点的环度
    cycles_degree = {}
    for i in range(G.vcount()):
        cycles_degree[i] = cycles_number_matrix[i][i]
        
    # 计算各个节点的环率
    cycles_ratio = {}
    for i in range(G.vcount()):
        cycles_ratio[i] = 0
        ratio = 0
        for j in range(G.vcount()):
            if cycles_number_matrix[i][i] > 0 and cycles_number_matrix[i][j] > 0 and cycles_number_matrix[j][j] > 0:
                ratio += cycles_number_matrix[i][j] / cycles_number_matrix[j][j]
        cycles_ratio[i] = ratio
    
    return cycles_degree, cycles_ratio

def cycle_contribution_rate(G, cycles):
    cycle_cont_rate = {node.index: 0 for node in G.vs}
    for node in G.vs:
        for cycle in cycles:
            if node.index in cycle:
                cycle_cont_rate[node.index] += 1/len(cycle)
    return cycle_cont_rate


# 导入网络G
graph_path = r'data/RoadToNetwork/km_2.graphml'
cycle_path = r'data/Cycles/km_2_cycles.txt'


G = ig.Graph.Read_GraphML(graph_path)

# 处理网络：去除自环、孤立节点
G.simplify(combine_edges="first")
G.delete_vertices(G.vs.select(_degree=0))

cycles = []
with open(cycle_path, 'r') as f:
    for line in f:
        if line.strip():
            cycles.append(list(map(int, line.strip().split(','))))
            
for v in G.vs:
    G.vs[v.index]["label"] = 0
    # G.vs[v.index]["label1"] = 0
    attribute = G.vs[v.index]["id"]
    x, y = attribute[1:-1].split(',')  
    x = float(x.strip())  
    y = float(y.strip())
    G.vs[v.index]["lng"] = x
    G.vs[v.index]["lat"] = y

degree = G.degree()  
nodes_deg = {}
for v in G.vs:
    nodes_deg[v.index] =  degree[v.index]
cycles = cycle_detection(G)
cycles_degree, cycles_ratio = cyclesFeature(G, cycles)
cycle_cont_rate = cycle_contribution_rate(G, cycles)

for node in G.vs:
    G.vs[node.index]['degree'] = float(nodes_deg[node.index])/float(max(nodes_deg.values()))
    G.vs[node.index]['cycle degree'] = float(cycles_degree[node.index])/float(max(cycles_degree.values()))
    G.vs[node.index]['cycle ratio'] = float(cycles_ratio[node.index])/float(max(cycles_ratio.values()))
    G.vs[node.index]['cycle contribute ratio'] = float(cycle_cont_rate[node.index])/float(max(cycle_cont_rate.values()))
    
            
net = G.to_networkx()
nx.write_gexf(net, "figure/km_2.gexf")