# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 01:27:51 2024

@author: Li Yuanbiao
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 28
plt.rcParams['xtick.labelsize'] = 28
plt.rcParams['ytick.labelsize'] = 28

Graph = ['bj', 'shh', 'gzh', 'shzh', 'chdu', 'km']  
titles = ['(a) Beijing', '(b) Shanghai', '(c) Guangzhou', '(d) Shenzhen', '(e) Chengdu', '(f) Kunming']
ylabel = ['Maximum components', 'Average size of cycles', 'Number of cycles ']
labels = ['random', 'betweenness', 'degree', 'cycles degree', 'cycles ratio', 'cycle contribution rate']
labels1 = ['Random', 'Betweenness', 'Degree', 'Cycle degree', 'Cycle ratio', 'Cycle contribution rate']
markers = ['p', 'd', 'v', 'o', 's','<']
linestyles = ['-', '--', '-.', ':', '-', '--']
colors = ['royalblue', 'darkgoldenrod', 'forestgreen', 'brown', 'darkorchid', 'navy']
attack = ['attack_components', 'attack_cycles', 'attack_cycles_number'] # 最大团大小，最大环大小，环的数量
fig = plt.figure(figsize=(20, 13))  
  
# 定义子图布局  
for i in range(6):  
    ax = fig.add_subplot(2, 3, i + 1)  
      
    # 计算各个环的数量
    file_path = r'data\\Robustness\\' + Graph[i] +'_2_' + attack[1] + '.csv'
    attack_data = pd.read_csv(file_path)
    for j in range(6):
        ax.plot(np.arange(0, 1, 0.05), attack_data[labels[j]].values, color=colors[j], marker=markers[j], markersize=8, linestyle=linestyles[j], label=labels1[j])
    ax.set_title(titles[i], y=-0.40)
    ax.set_xlabel("$p$") 
    ax.set_ylabel(r"$\left \langle L^{c} \right \rangle$", rotation=0, labelpad=23)
    ax.set_xticks(np.arange(0, 1.2, 0.2))

fig.legend(labels1, loc='lower center', bbox_to_anchor=(0.5, -0.07), ncol=3)
fig.tight_layout()  # 调整子图布局，使之不会重叠 
plt.savefig('figure/Stability_average_size.eps', dpi=600, bbox_inches='tight')
plt.savefig('figure/Stability_average_size.svg', dpi=600, bbox_inches='tight')
plt.show()