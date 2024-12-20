# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 22:41:13 2024

@author: Li Yuanbiao
"""

import igraph as ig
import numpy as np
import matplotlib.pyplot as plt
import collections

# Set font and style configurations
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 28
plt.rcParams['xtick.labelsize'] = 28
plt.rcParams['ytick.labelsize'] = 28

# Define constants
DATA_PATH = 'data/'
GRAPH_FILE_FORMAT = '{}_{}.graphml'
CYCLE_FILE_FORMAT = '{}_{}_cycles.txt'

Graphs = ['bj', 'shh', 'gzh', 'shzh', 'chdu', 'km']
Colors = ['#334c81', '#6f8278', '#70a3c4', '#df5b3f']
Titles = ['(a) Beijing', '(b) Shanghai', '(c) Guangzhou', '(d) Shenzhen', '(e) Chengdu', '(f) Kunming']
Labels = ['First layer', 'Second layer', 'Third layer', 'Fourth layer']

def read_graph(graph_name, layer):
    graph_path = DATA_PATH + 'RoadToNetwork/' + GRAPH_FILE_FORMAT.format(graph_name, layer)
    G = ig.Graph.Load(graph_path, format="graphml").simplify()
    # G = ig.Graph.Read_GraphML(graph_path)
    # G.simplify(combine_edges="first")
    # G.delete_vertices(G.vs.select(_degree=0))
    return G

def read_cycles(graph_name, layer):
    cycle_path = DATA_PATH + 'Cycles/' + CYCLE_FILE_FORMAT.format(graph_name, layer)
    cycles = []
    with open(cycle_path, 'r') as f:
        for line in f:
            if line.strip():
                cycles.append(list(map(int, line.strip().split(','))))
    return cycles

def calculate_node_cycles_degree(G, cycles):
    node_cycles_degree = {}
    for node in G.vs: 
        node_cycles_degree[node.index] = 0
        for sub_cycles in cycles:
            if node.index in sub_cycles:
                node_cycles_degree[node.index] += 1
    return node_cycles_degree

def main():
    fig = plt.figure(figsize=(20, 13))
    max_x_value = 0  # 用于存储横坐标的最大值
    for i, graph_name in enumerate(Graphs):
        print(i)
        ax = fig.add_subplot(2, 3, i + 1)
        for j in range(4):
            print(j)
            G = read_graph(graph_name, j + 1)
            cycles = read_cycles(graph_name, j + 1)

            node_cycles_degree = calculate_node_cycles_degree(G, cycles)
            my_dict = collections.Counter(node_cycles_degree.values())  
            elements = dict(sorted(my_dict.items(), key=lambda x: x[0])) 
            
            element_names = np.array(list(elements.keys()))
            element_counts = np.array(list(elements.values()))/np.sum(list(elements.values()))
            
            max_x_value = max(max_x_value, np.max(element_names))
            ax.bar(element_names + 0.2*j-0.3, 
                   element_counts, width=0.2,
                   align="center", color= Colors[j], label=str(j+1))  

        ax.set_title(Titles[i], y=-0.40)
        ax.set_xlabel("Cycle degree of node")
        ax.set_ylabel("Proportion")
        xticks = np.arange(0, int(max_x_value)+1, 1)
        ax.set_xticks(xticks)

    fig.legend(Labels, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=4)
    fig.tight_layout()

    plt.savefig('figure/node_cycles_degree.eps', dpi=600, bbox_inches='tight')
    plt.savefig('figure/node_cycles_degree.svg', dpi=600, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    main()
