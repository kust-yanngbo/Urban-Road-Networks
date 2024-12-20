# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:18:02 2024

@author: Li Yuanbiao
"""

import igraph as ig
import numpy as np
import pandas as pd
import random
import collections

# 静态攻击
def staticAttack(G, attack_rate, attack_type):
    node_number = G.vcount()             # 节点数量
    sorted_nodes = sorted(attack_type.keys(), key=lambda x: attack_type[x], reverse=True)  # 排序好的节点
    average_cycles_size = np.array([])    # 环的平均大小
    cycles_number = np.array([])          # 环的平均大小
    max_components = np.array([])
    for i in np.arange(0, 1, attack_rate):
        G_re = G.copy()
        node_to_remove = sorted_nodes[: min(int(i*node_number), node_number)]
        G_re.delete_vertices(node_to_remove)
        
        # 计算网络的连通性
        largest_cc = max(G_re.components(mode="weak"), key=len)
        components = len(largest_cc)/node_number
        max_components = np.append(max_components, components)
        
        # 计算网络的最大环大小和环数量
        # 调用环探测函数
        cycle_nodes_list = cycle_detection(G_re)
        sorted_cycles = sorted(cycle_nodes_list, key=len, reverse=True)
        cycles_size = [len(i) for i in sorted_cycles]
        if len(sorted_cycles)==0:
            average_cycles_size = np.append(average_cycles_size, 0)
            cycles_number = np.append(cycles_number, 0)
        else:
            average_cycles_size = np.append(average_cycles_size, sum(cycles_size)/len(sorted_cycles))
            cycles_number = np.append(cycles_number, len(sorted_cycles))
        
    return max_components, average_cycles_size, cycles_number

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
    for i in range(G.vcount()-1):
        # 找到含有节点i的环
        cycles_i = []
        for sub_cycles in cycles:
            if i in sub_cycles:
                cycles_i.append(sub_cycles)
        #cycles_number_matrix[i][i] = len(cycles_i)
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

#随机攻击
def RandomAttack(G, attack_rate, iteration_num):
    node_list = [v.index for v in G.vs]
    node_number = G.vcount()
    average_cycles_size = np.array([])    # 环的平均大小
    cycles_number = np.array([])
    max_components = np.array([])
    for i in np.arange(0, 1, attack_rate):
        num = 0
        components_remove = np.array([])
        cycles_remove = np.array([])
        cycles_number_remove = np.array([])
        while num < iteration_num:
            G_re = G.copy()
            num += 1
            node_to_remove = random.sample(node_list, min(int(i*node_number), node_number))
            G_re.delete_vertices(node_to_remove)
            
            # 计算网络的连通性
            largest_cc = max(G_re.components(mode="weak"), key=len)
            components = len(largest_cc)/node_number
            #motif = ig.Graph.motifs_randesu_no(G_re, 3)
            components_remove = np.append(components_remove, components)
            
            # 计算网络的最大环大小和环数量
            # 调用环探测函数
            cycle_nodes_list = cycle_detection(G_re)
            sorted_cycles = sorted(cycle_nodes_list, key=len, reverse=True)
            cycles_size = [len(i) for i in sorted_cycles]
            if len(sorted_cycles)==0:
                cycles_remove = np.append(cycles_remove, 0)
                cycles_number_remove = np.append(cycles_number_remove, 0)
            else:
                cycles_remove = np.append(cycles_remove, sum(cycles_size)/len(sorted_cycles))
                cycles_number_remove = np.append(cycles_number_remove, len(sorted_cycles))
            
        max_components = np.append(max_components, np.mean(components_remove))
        average_cycles_size = np.append(average_cycles_size, np.mean(cycles_remove))
        cycles_number = np.append(cycles_number, np.mean(cycles_number_remove))
        
    return max_components, average_cycles_size, cycles_number


if __name__ == "__main__":
    path = 'data/RoadToNetwork/'
    graph = 'bj_1'
    graph_path = path+graph+'.graphml'
    
    G = ig.Graph.Read_GraphML(graph_path)
    G.simplify(combine_edges="first")
    G.delete_vertices(G.vs.select(_degree=0))

    attack_rate = 0.05
    
    # 随机攻击
    iteration_num = 100
    max_random = RandomAttack(G.copy(), attack_rate, iteration_num)
    
    # 介数攻击
    betweenness = G.betweenness()  
    nodes_bet = {}
    for v in G.vs:
        nodes_bet[v.index] = betweenness[v.index]
    max_betweenness = staticAttack(G.copy(), attack_rate, nodes_bet)    # 环度攻击
    
    # 度攻击
    degree = G.degree()  
    nodes_deg = {}
    for v in G.vs:
        nodes_deg[v.index] =  degree[v.index] 
    max_degree = staticAttack(G.copy(), attack_rate, nodes_deg)    # 环度攻击
    
    # 进行环探测，得到网络中的环结构信息
    cycles = cycle_detection(G)
    # 根据网络结构和环的分布情况计算环度和环率
    cycles_degree, cycles_ratio = cyclesFeature(G, cycles)
    # 实际网络攻击
    max_cycles_degree = staticAttack(G.copy(), attack_rate, cycles_degree)    # 环度攻击
    max_cycles_ratio = staticAttack(G.copy(), attack_rate, cycles_ratio)    # 环率攻击
    
    data = pd.DataFrame()
    data['random'] = max_random[0]
    data['betweenness'] = max_betweenness[0]
    data['degree'] = max_degree[0]
    data['cycles degree'] = max_cycles_degree[0]
    data['cycles ratio'] = max_cycles_ratio[0]
    data.to_csv(path+graph+'_attack_components.csv')
    
    data1 = pd.DataFrame()
    data1['random'] = max_random[1]
    data1['betweenness'] = max_betweenness[1]
    data1['degree'] = max_degree[1]
    data1['cycles degree'] = max_cycles_degree[1]
    data1['cycles ratio'] = max_cycles_ratio[1]
    data1.to_csv(path+graph+'_attack_cycles.csv')

    data2 = pd.DataFrame()
    data2['random'] = max_random[2]
    data2['betweenness'] = max_betweenness[2]
    data2['degree'] = max_degree[2]
    data2['cycles degree'] = max_cycles_degree[2]
    data2['cycles ratio'] = max_cycles_ratio[2]
    data2.to_csv(path+graph+'_attack_cycles_number.csv')