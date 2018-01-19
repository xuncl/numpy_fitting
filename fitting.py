#!/usr/bin/env python
# coding: utf-8

import numpy as np
import MySQLdb
import datetime


daysAgo = (datetime.datetime.now() - datetime.timedelta(days = 7))
agoStr = daysAgo.strftime("%Y-%m-%d %H:%M:%S")
daysNow = (datetime.datetime.now())
nowStr = daysNow.strftime("%Y-%m-%d %H:%M:%S")

# 打开数据库连接
db = MySQLdb.connect("localhost","root","","db")

# 使用cursor()方法操作游标
cursor = db.cursor()

# SQL 获取所有分组
groups = ()
sql = "SELECT DISTINCT group_id FROM ck_fitting_setting \
       WHERE invalid_id = 0 "
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   groups = cursor.fetchall()
except:
   print "Error: unable to fecth data: " + sql

print groups  # tuples in tuple


def getArea(group_id):
	areas = ()
	sql = "SELECT area_start_id, area_end_id FROM ck_fitting_setting \
       WHERE invalid_id = 0 and group_id = %d " % group_id
	try:
	   # 执行SQL语句
	   cursor.execute(sql)
	   # 获取所有记录列表
	   areas = cursor.fetchall()
	except:
	   print "Error: unable to fecth data: " + sql
	print areas
	return areas


def getData(start_id, end_id):
	start4 = start_id / 10000
	end4 = end_id / 10000
	data = ()
	sql = "SELECT distance, freight_price FROM ck_freight WHERE \
		(floor(area_start_id/10000)=%d or floor(area_start_id/100000)=%d) and \
		(floor(area_end_id/10000)=%d or floor(area_end_id/100000)=%d) and \
		record_time<'%s' and record_time>'%s' \
		order by id desc" % (start4, start4, end4, end4, nowStr, agoStr)
	try:
	   cursor.execute(sql)
	   data = cursor.fetchall()
	except:
	   print "Error: unable to fecth data: " + sql
	return data


def insertFitting(group_id, a, b):
	# SQL 更新语句
	sql = "INSERT INTO ck_freight_fitting(group_id, \
		a, b, start_time, end_time) values (%d,%f,%f,'%s','%s')" % \
		(group_id, a, b, agoStr, nowStr)
	try:
	   # 执行SQL语句
	   cursor.execute(sql)
	   # 提交到数据库执行
	   db.commit()
	except:
	   # 发生错误时回滚
	   db.rollback()
	   print "insert error: "+sql


def optimal(A, b):
	B = A.T.dot(b)
	AA = np.linalg.inv(A.T.dot(A))  # 求A.T.dot(A)的逆
	P = AA.dot(B)
	print "P:"
	print P
	return P


def getDist(tup):
	return tup[0]


def getPrice(tup):
	return tup[1]


for row in groups:
	# 一组数据
	group_id = row[0]
	if (not group_id):
		continue
	areas = getArea(group_id)
	a = 0
	b = 0
	distancesAll = []
	pricesAll = []
	for one in areas:
		# 一条市到市的数据
		xAndY = np.array([[1,1],[1,0]])
		start_id = one[0]
		end_id = one[1]
		data = getData(start_id, end_id)
		# 累加这个组下所有的距离和运费
		distancesAll += map(getDist, data)
		pricesAll += map(getPrice, data)
	if (len(distancesAll)<3):
		continue
	x = np.array(distancesAll)
	y1 = np.array(pricesAll)
	print x
	print y1
	print '***'
	if ((not distancesAll) or (not pricesAll)):
		continue
	# main
	one = np.ones((len(x), 1))  # len(x)得到数据量
	# one 是100x1的矩阵，每个元素都是1
	x = x.reshape(x.shape[0], 1)
	# print x
	A = np.hstack((x, one))  # 两个100x1的列向量合并成100x2
	# print A
	# C = y1.reshape(y1.shape[0], 1)
	[a, b] = optimal(A, y1)
	insertFitting(group_id, a, b)

db.close()
