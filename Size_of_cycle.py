# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 00:20:00 2024

@author: Li Yuanbiao
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import collections
import powerlaw

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 28
plt.rcParams['xtick.labelsize'] = 28
plt.rcParams['ytick.labelsize'] = 28


Graphs = ['bj', 'shh', 'gzh', 'shzh', 'chdu', 'km']
colors = ['#334c81', '#008a45', '#70a3c4',  '#df5b3f']
titles = ['(a) Beijing', '(b) Shanghai', '(c) Guangzhou', '(d) Shenzhen', '(e) Chengdu', '(f) Kunming']
text_label = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']
markers = ['o', '^', 'v', 'p']
labels = ['First layer', 'Second layer', 'Third layer', 'Fourth layer']

path = 'data/'
# 存储结果的列表
results = []

fig = plt.figure(figsize=(20, 13))

# 定义子图布局
for i in range(6):
    ax = fig.add_subplot(2, 3, i + 1)
    ax.set_xscale('log')
    ax.set_yscale('log')

    # 存储当前城市的结果
    city_results = {'City': Graphs[i]}  

    for j in range(4):
        file_path = path + 'Cycles/' + Graphs[i] + '_' + str(j + 1) + '_cycles.txt'
        with open(file_path, 'r') as f:
            cycles = []
            for line in f:
                if line.strip():
                    cycles.append(list(map(int, line.strip().split(','))))

        length = []
        for sublist in cycles:
            length.append(len(sublist))
        my_dict = collections.Counter(length)
        elements = dict(sorted(my_dict.items(), key=lambda x: x[0]))

        # 提取元素名称和个数
        element_names = np.array(list(elements.keys()))
        element_counts = np.array(list(elements.values())) / np.sum(list(elements.values()))

        # 绘制散点图
        ax.scatter(element_names, element_counts, marker=markers[j], color=colors[j], s=70, label=str(j + 1))

        # 使用 powerlaw 库计算幂指数
        fit = powerlaw.Fit(length, discrete=True)
        alpha = fit.alpha
        city_results[f'Layer {j+1}'] = alpha  # Changed: Appended to the dictionary

    # 将当前城市的结果添加到总体结果
    results.append(city_results)

    ax.set_title(titles[i], y=-0.40)
    ax.set_xlabel("Size of cycle")
    ax.set_ylabel("Proportion")

fig.legend(labels, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=4)
fig.tight_layout()

plt.savefig('figure/Size_of_cycle.eps', dpi=600, bbox_inches='tight')
plt.savefig('figure/Size_of_cycle.svg', dpi=600, bbox_inches='tight')
plt.show()

# 将结果保存到表格
columns = ['City', 'Layer 1', 'Layer 2', 'Layer 3', 'Layer 4']
df = pd.DataFrame(results, columns=columns)
df['City'] = Graphs
df.to_csv(path+'NetworkMetrics/cycle_size_powerlaw_results.csv', index=False)