# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 01:27:51 2024

@author: Li Yuanbiao
"""

import os

"""
合并多个txt文件
"""

result_file = open('data/Cycles/shh_4_cycles.txt', 'w')

nuique_lines = set()

# 遍历需要合并的文件
for i in range(1, 500):
    filepath = 'data/Cycles/shh_4_cycles_' + str(i) +'.txt'
    for line in open(filepath):
        if line not in nuique_lines:
            nuique_lines.add(line)
            result_file.writelines(line)
    result_file.write('\n')
result_file.close()