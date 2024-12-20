# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 23:27:44 2024

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
        # file_path = '城市道路数据分析/道路转网络数据/' + Graph[i] +'_'+ str(j+1) + '.graphml'
        file_path = 'data/DualNetwork_Node2/' + Graph[i] +'_'+ str(j+1) + '_dual_2.graphml'
        # g = ig.Graph.Load(file_path, format="graphml").simplify()
        g = ig.Graph.Read_GraphML(file_path)

        # 处理网络：去除自环、孤立节点
        # g.simplify(combine_edges="first")
        # g.delete_vertices(g.vs.select(_degree=0))
        # g = g.as_undirected(mode='mutual')

        # 计算整个网络的指标
        num_nodes = g.vcount()
        num_edges = g.ecount()
        average_degree = sum(g.degree()) / num_nodes

        # 计算最大连通子图的平均路径长度
        largest_connected_component = g.clusters().giant()
        l_num_nodes = largest_connected_component.vcount()
        l_num_edges = largest_connected_component.ecount()
        average_path_length = largest_connected_component.average_path_length(directed=False)

        clustering_coefficient = g.transitivity_undirected()
        diameter = largest_connected_component.diameter(directed=False)
        density = g.density()

        # 将结果添加到列表
        network_data.append({
            'Network': graph_file,
            'Nodes': num_nodes,
            'Edges': num_edges,
            'Average Degree': average_degree,
            'Largest Nodes': l_num_nodes,
            'Largest Edges': l_num_edges,
            'Average Path Length': average_path_length,
            'Clustering Coefficient': clustering_coefficient,
            'Diameter': diameter,
            'Density': density
        })

# 将列表转换为 DataFrame
df = pd.DataFrame(network_data)

# 将结果保存为 CSV 文件
# df.to_csv('城市道路数据分析/网络指标/city_network_metrics_igraph.csv', index=False)
df.to_csv('data/NetworkMetrics/dual_network_metrics_igraph_2_node.csv', index=False)

# 显示结果
print(df)