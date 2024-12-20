# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 00:34:57 2024

@author: Li Yuanbiao
"""

import igraph as ig
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections
import powerlaw

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 28
plt.rcParams['xtick.labelsize'] = 28
plt.rcParams['ytick.labelsize'] = 28

# 常量
DATA_PATH = 'data/DualNetwork_Node1/'
GRAPH_FILE_FORMAT = '{}_{}_dual_2.graphml'

Graphs = ['bj', 'shh', 'gzh', 'shzh', 'chdu', 'km']
Colors = ['#334c81', '#008a45', '#70a3c4',  '#df5b3f']
Titles = ['(a) Beijing', '(b) Shanghai', '(c) Guangzhou', '(d) Shenzhen', '(e) Chengdu', '(f) Kunming']
TextLabels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']
Markers = ['o', '^', 'v', 'p']
Labels = ['First layer', 'Second layer', 'Third layer', 'Fourth layer']


# 存储幂指数结果的列表
results = []

fig = plt.figure(figsize=(20, 13))  
  
# 定义子图布局  
for i in range(6):  
    ax = fig.add_subplot(2, 3, i + 1) 
    ax.set_xscale('log')  
    ax.set_yscale('log') 
    
    # 存储当前城市的结果
    city_results = {'City': Graphs[i]}  # Changed: Initialized as a dictionary
    
    for j in range(4):
        graph_path = DATA_PATH + GRAPH_FILE_FORMAT.format(Graphs[i], j + 1)
        G = ig.Graph.Read_GraphML(graph_path)

        # 处理网络：去除自环、孤立节点
        # G.simplify(combine_edges="first")
        # G.delete_vertices(g.vs.select(_degree=0))
        # G = G.as_undirected(mode='mutual')
        
        my_dict = collections.Counter(G.degree())  
        elements = dict(sorted(my_dict.items(), key=lambda x: x[0]))   
        
        # 提取元素名称和个数  
        element_names = np.array(list(elements.keys()))
        element_counts = np.array(list(elements.values()))/np.sum(list(elements.values()))
        #element_counts = list(elements.values())  

        # 绘制柱状图  
        # ax.bar(element_names + 0.2*j-0.3, element_counts, width=0.2,align="center", color= colors[j], label=str(j+1))
        ax.scatter(element_names, element_counts, 
                   color= Colors[j], marker=Markers[j], s=70, label=str(j+1)) 
        
        # 使用 powerlaw 库计算幂指数
        fit = powerlaw.Fit(G.degree(), discrete=True)
        alpha = fit.alpha
        city_results[f'Layer {j+1}'] = alpha  

    # 将当前城市的结果添加到总体结果
    results.append(city_results)
    
    # 设置子图的标题和轴标签  
    ax.set_title(Titles[i], y=-0.40)
    ax.set_xlabel("$k$")  
    ax.set_ylabel("$P$", rotation=0, labelpad=15)
fig.legend(Labels, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=4)
fig.tight_layout()  

plt.savefig('figure/Dual_graph_degree_2_node.eps', dpi=600, bbox_inches='tight')
plt.savefig('figure/Dual_graph_degree_2_node.svg', dpi=600, bbox_inches='tight')

plt.show()

# 将结果保存到表格
columns = ['City', 'Layer 1', 'Layer 2', 'Layer 3', 'Layer 4']
df = pd.DataFrame(results, columns=columns)
df['City'] = Graphs
