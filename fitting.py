#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

# x 的个数决定了样本量
x = np.arange(-1, 1, 0.02)
print x
# y 为理想函数
y = 2 * np.sin(x * 2.3) + 0.5 * x**3
# y1 为离散的拟合数据
y1 = y + 0.5 * (np.random.rand(len(x)) - 0.5)

####################
# main
one = np.ones((len(x), 1))  # len(x)得到数据量
x = x.reshape(x.shape[0], 1)
A = np.hstack((x, one))  # 两个100x1的列向量合并成100x2
#C = y1.reshape(y1.shape[0], 1)
C = y1
# print x
# 等同于C = y1.reshape(100,1)
# 虽然知道y1的个数为100，但是程序中不应该出现人工读取的数据


def optimal(A, b):
    B = A.T.dot(b)
    AA = np.linalg.inv(A.T.dot(A))  # 求A.T.dot(A)的逆
    P = AA.dot(B)
    print P
    return A.dot(P)


# 求得的[a,b]=P=[[2.8878][-1.4006]]
yy = optimal(A, C)
# yy = P[0]*x+P[1]
##################
plt.plot(x, y, color='g', linestyle='-', marker='', label=u'real')
plt.plot(x, y1, color='m', linestyle='', marker='o', label=u'data')
plt.plot(x, yy, color='b', linestyle='-', marker='.', label=u'fitting')
# ploting
plt.legend(loc='upper left')
plt.show()


print '***'*3
Z = [[1,2],[3,4]]
Z = Z.reshape(4,1)
Y = [[1,1],[0,1]]
Y = Y.reshape(4,1)
print Z.dot(Y)