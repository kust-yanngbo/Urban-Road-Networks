# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 23:27:44 2024

@author: Li Yuanbiao
"""

import igraph as ig
import numpy as np

# 常量
DATA_PATH = 'data/'
GRAPH_FILE_FORMAT = '{}_{}.graphml'
CYCLE_FILE_FORMAT = '{}_{}_cycles.txt'
CYCLE_DUAL_FILE_FORMAT = '{}_{}_dual_3.graphml'

# Graphs = ['bj', 'shh', 'gzh', 'shzh', 'chdu', 'km']
Graphs = ['km']
# 生成对偶网络
# 将每一个环看成是一个网络中的节点，故新网络中节点的数量=环的数量
# 1.构造一个邻接矩阵
def weightAdjacency(cycles):
    adjacency  = np.zeros((len(cycles), len(cycles)))  # 先构造一个全零矩阵

    for i in range(len(cycles)-1):
        for j in range(i+1, len(cycles)):
            intersection = len(set(cycles[i]) & set(cycles[j]))
            if intersection >= 3:
                adjacency[i][j] = intersection
                adjacency[j][i] = intersection

    return adjacency

# 2.计算新网络中每一个新节点的地理坐标（lng, lat）构造一个邻接矩阵
def geographicalCoor(G, cycles):
    geographical = []
    for sub in cycles:
        lng = 0
        lat = 0
        for i in sub:
            data = G.vs[i]["id"]
            x, y = data[1:-1].split(',')  
            x = float(x.strip())  
            y = float(y.strip())
            lng += x
            lat += y
        geographical.append((lng/len(sub), lat/len(sub)))
        
    return geographical

# 3.根据邻接矩阵生成新的网络
def buildNet(adjacency, geographical):
    G_new = ig.Graph.Weighted_Adjacency(adjacency, mode='undirected')

    # 4.为每一个新的节点重新标记新的坐标
    for node in G_new.vs:
        G_new.vs[node.index]["lng"] = geographical[node.index][0]
        G_new.vs[node.index]["lat"] = geographical[node.index][1]
        #G_new.vs[node.index]["weight"] = np.sum(adjacency[node.index, :])
    return G_new

def read_graph(graph_name, layer):
    graph_path = DATA_PATH + "RoadToNetwork/" + GRAPH_FILE_FORMAT.format(graph_name, layer)
    G = ig.Graph.Read_GraphML(graph_path)
    G.simplify(combine_edges="first")
    G.delete_vertices(G.vs.select(_degree=0))
    return G

def read_cycles(graph_name, layer):
    cycle_path = DATA_PATH + "Cycles/" + CYCLE_FILE_FORMAT.format(graph_name, layer)
    cycles = []
    with open(cycle_path, 'r') as f:
        for line in f:
            if line.strip():
                cycles.append(list(map(int, line.strip().split(','))))
    return cycles


def main():

    for i, graph_name in enumerate(Graphs):
        for j in range(4):
            G = read_graph(graph_name, j + 1)
            cycles = read_cycles(graph_name, j + 1)
            adjacency = weightAdjacency(cycles)
            geographical = geographicalCoor(G, cycles)
            G_new = buildNet(adjacency, geographical)
            dual_graph_path = DATA_PATH + "DualNetwork_Node3/" + CYCLE_DUAL_FILE_FORMAT.format(graph_name, j+1)
            ig.Graph.write_graphml(G_new, dual_graph_path)

if __name__ == "__main__":
    main()
