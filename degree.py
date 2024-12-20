# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 23:27:44 2024

@author: Li Yuanbiao
"""

import igraph as ig
import numpy as np
import matplotlib.pyplot as plt
import collections


plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 28
plt.rcParams['xtick.labelsize'] = 28
plt.rcParams['ytick.labelsize'] = 28


Graph = ['bj', 'shh', 'gzh', 'shzh', 'chdu', 'km']  
colors = ['#334c81', '#6f8278', '#70a3c4',  '#df5b3f']

titles = ['(a) Beijing', '(b) Shanghai', '(c) Guangzhou', '(d) Shenzhen', '(e) Chengdu', '(f) Kunming']
labels = ['First layer', 'Second layer', 'Third layer', 'Fourth layer']

fig = plt.figure(figsize=(20, 13))  
  
# 定义子图布局  
for i in range(6):  
    # ax = fig.add_subplot(2, 2, i + 1)  
    ax = fig.add_subplot(2, 3, i + 1) 
    
    for j in range(4):
        # 计算度分布
        graphPath = 'data/RoadToNetwork/' + Graph[i] +'_'+ str(j+1) + '.graphml'
        G = ig.Graph.Read_GraphML(graphPath)
        G.simplify(combine_edges="first")
        G.delete_vertices(G.vs.select(_degree=0))
        
        my_dict = collections.Counter(G.degree())  
        elements = dict(sorted(my_dict.items(), key=lambda x: x[0]))  

        # 提取元素名称和个数  
        element_names = np.array(list(elements.keys()))
        element_counts = np.array(list(elements.values()))/np.sum(list(elements.values()))
        #element_counts = list(elements.values())  

        # 绘制柱状图  
        ax.bar(element_names + 0.2*j-0.3, element_counts, width=0.2,align="center", color= colors[j], label=str(j+1))  
      
    # 设置子图的标题和轴标签  
    ax.set_title(titles[i], y=-0.40) 
    ax.set_xlabel("Degree")  
    # ax.set_ylabel("Frequency")
    ax.set_ylabel("Proportion")
    # ax.grid()
    ax.set_xticks(range(1, 7, 1))
fig.legend(labels, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=4)
fig.tight_layout()  # 调整子图布局，使之不会重叠 

# 保存图像
plt.savefig('figure/degree.eps', dpi=600, bbox_inches='tight')
plt.savefig('figure/degree.svg', dpi=600, bbox_inches='tight')