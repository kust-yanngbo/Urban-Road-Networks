# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 02:43:12 2024

@author: Li Yuanbiao
"""

import igraph as ig
import pandas as pd

# 存储网络指标的列表
network_data = []

Graph = ['bj', 'shh', 'gzh', 'shzh', 'chdu', 'km']
for i in range(6):  
    for j in range(4):
        # graph_file =  Graph[i] +'_'+ str(j+1)
        graph_file =  Graph[i] +'_'+ str(j+1)+ '_dual_2'
        # 计算度分布
        file_path = 'data/DualNetwork_Node2/' + Graph[i] +'_'+ str(j+1) + '_dual_2.graphml'

        g = ig.Graph.Read_GraphML(file_path)
        
        clusters = g.clusters()
        num_clusters = clusters.__len__()

        # 将结果添加到列表
        network_data.append({
            'Num_clusters': num_clusters

        })

# 将列表转换为 DataFrame
df = pd.DataFrame(network_data)

# 将结果保存为 CSV 文件
df.to_csv('data/NetworkMetrics/Num_clusters_dual_igraph_2_node.csv', index=False)

# 显示结果
print(df)
