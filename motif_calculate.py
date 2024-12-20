# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:49:42 2024

@author: Li Yuanbiao
"""

import igraph as ig
import pandas as pd
import numpy as np

# 常量
DATA_PATH = r'data/'
GRAPH_FILE_FORMAT = '{}_{}.graphml'
Graphs = ['bj', 'shh', 'gzh', 'shzh', 'chdu', 'km']

def read_graph(graph_name, layer):
    graph_path = DATA_PATH + 'RoadToNetwork/' + GRAPH_FILE_FORMAT.format(graph_name, layer)
    G = ig.Graph.Read_GraphML(graph_path)
    G.simplify(combine_edges="first")
    G.delete_vertices(G.vs.select(_degree=0))
    return G

def Z_score(G, motif_new):
    #计算原始网络的度序列
    degree_sequence = G.degree()

    # 生成随机网络
    # 计算每一个随机网络中的模体结构特征
    num = 100
    motif_no_random = {}
    for i in range(num):
        random_graph = ig.Graph.Degree_Sequence(degree_sequence, method="fast_heur_simple")
        motif_ = []
        for j in range(3, 5):
            mt = ig.Graph.motifs_randesu(random_graph, j)
            mt_new = []
            for mt_i in mt:
                if str(mt_i) != 'nan':
                    mt_new.append(mt_i)
            motif_.append(mt_new)
        motif_no_random[i]=motif_

    # 计算Z分数
    motif_num_3 = [[] for i in range(2)]
    motif_num_4 = [[] for i in range(6)]
    for v in motif_no_random.values():
        motif_num_3[0].append(v[0][0])
        motif_num_3[1].append(v[0][1])
        for index in range(6):
            motif_num_4[index].append(v[1][index])

    motif_num_3_array = np.array(motif_num_3)
    motif_num_4_array = np.array(motif_num_4)
    
    motif_mean_3 = [np.mean(i) for i in motif_num_3_array]
    motif_mean_4 = [np.mean(i) for i in motif_num_4_array]
    motif_std_3 = [np.std(i) for i in motif_num_3_array]
    motif_std_4 = [np.std(i) for i in motif_num_4_array]

    motif_Z_3 = (np.array(motif_new[:2]) - motif_mean_3) / motif_std_3
    motif_Z_4 = (np.array(motif_new[2:]) - motif_mean_4) / motif_std_4
    
    z_score = []
    for i in motif_Z_3:
        z_score.append(i)
    for j in motif_Z_4:
        z_score.append(j)
    
    return z_score


def main():
    df = pd.DataFrame()
    for i, graph_name in enumerate(Graphs):
        mt = []
        G = read_graph(graph_name, 4)
        motif = [ig.Graph.motifs_randesu(G, i) for i in range(3, 5)]
        for i in motif:
            for j in i:
                if str(j) != 'nan':
                    mt.append(j)
                    
        z_score = Z_score(G, mt)
        df[graph_name +'_'+ str(2)] = mt
        df[graph_name +'_z-score'+ str(2)] = z_score
    
    df.to_csv('data\\NetworkMetrics\\motif4.csv', index=False)


if __name__ == "__main__":
    main()