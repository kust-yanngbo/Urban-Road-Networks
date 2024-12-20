# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:50:54 2024

@author: Li Yuanbiao
"""

import numpy as np
from scipy.optimize import curve_fit

# 定义幂律分布函数
def power_law(x, alpha, c):
    return c * x**(-alpha)

# 生成示例数据
data = np.random.pareto(2.5, 1000)  # 生成幂律分布的示例数据

# 对数据进行排序
sorted_data = np.sort(data)

# 计算概率密度函数
pdf = 1.0 / (sorted_data * np.log(sorted_data[-1]/sorted_data[0]))

# 初始参数猜测
initial_guess = [2.0, 1.0]

# 使用最小二乘法拟合幂律分布
params, covariance = curve_fit(power_law, sorted_data, pdf, p0=initial_guess)

# 输出拟合结果
alpha_fit, c_fit = params
print("拟合的幂指数 (alpha):", alpha_fit)
