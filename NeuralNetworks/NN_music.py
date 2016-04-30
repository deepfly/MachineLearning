########################################################################
# File: NN_music.py
# Version: 27 April 2016 (ZZ)
#
# Description:
#
#
# Usage:
#
#
#
# @author: Ziping Zheng
#
#########################################################################
import sys
import math
import scipy
import random

def sigmoid2D(x):
	x2 = x
	for i in xrange(0, len(x)):
		for j in xrange(0, len(x[i])):
	 		x2[i][j] = 1.0 / (1.0 + math.e ** (0.0 - x2[i][j]))
	return x2

def sigmoid1D(x):
	x2 = x
	for i in xrange(0, len(x)):
	 	x2[i] = 1 / (1 + math.e ** (0.0 - x2[i]))
	return x2

def sigmoid0D(x):
	return 1 / (1 + math.e ** (0.0 - x))

def multiply2D(a, b):
	result = []
	for k in xrange(0, len(b[0])):
		for i in xrange(0, len(a)):
			tempRow = []
			temp = 0.0
			for j in xrange(0, len(a[i])):
				temp = temp + a[i][j] * b[j][k]
			tempRow.append(temp)
		result.append(tempRow)
	return result

def multiply1D(a, b):
	result = []
	for k in xrange(0, len(b[0])):
		temp = 0.0
		for i in xrange(0, len(a)):
			temp = temp + a[i] * b[i][k]
		result.append(temp)
	return result

file = open(sys.argv[1], 'r')
testfile = open(sys.argv[2], 'r')

YesNoMap = {"yes": 1.0, "no": 0.0}

title = []
line = file.readline()
title = line.strip("\r\n").split(',')

learning_rate = 0.1
data2D = []
label = []
hidlen = 2
mean = [0.0, 0.0, 0.0, 0.0]
stddev = [0.0, 0.0, 0.0, 0.0]
mat1 = []
mat2 = []

for x in xrange(0,4):
	temp = []
	for y in xrange(0, hidlen):
		temp.append(random.uniform(-1.0, 1.0))
	mat1.append(temp)

for x in xrange(0, hidlen):
	temp = [random.uniform(-1.0, 1.0)]
	mat2.append(temp)

count = 0

while 1:
	line = file.readline()
	if not line:
		break
	line = line.strip("\r\n").split(',')
	data1 = []
	data1.append(float(line[0]))
	data1.append(float(line[1]))#
	data1.append(YesNoMap[line[2]])
	data1.append(YesNoMap[line[3]])
	data2D.append(data1)
	label.append(YesNoMap[line[4]])
	# print YesNoMap[line[4]]
	count = count + 1
	for i in xrange(0, len(data1)):
		mean[i] = mean[i] + data1[i] 
# print str(data2D)

#normalize
for i in xrange(0, len(mean)):
	mean[i] = mean[i] / count
for d in xrange(0, len(data2D)):
	for i in xrange(0, len(mean)):
		stddev[i] = stddev[i] + (data2D[d][i] - mean[i]) ** 2
for i in xrange(0, len(mean)):
	stddev[i] = stddev[i] / count
	stddev[i] = stddev[i] ** 0.5

# print mean, stddev

for d in xrange(0, len(data2D)):
	for i in xrange(0, len(mean)):
		data2D[d][i] = (data2D[d][i] - mean[i]) / stddev[i]

for it in xrange(0, 2000):
	error = 0.0
	for d in xrange(0, len(data2D)):
		mid = multiply1D(data2D[d], mat1)
		# print mid
		sigmid = sigmoid1D(mid)
		# print sigmid
		output = multiply1D(sigmid, mat2)[0]
		sigout = sigmoid0D(output)
		# print sigout
		delta_o = sigout * (1 - sigout) * (label[d] - sigout)
		error = error + (label[d] - sigout) ** 2
		# print delta_o
		delta_h = []

		for x in xrange(0, len(mat2)):
			sumwd = mat2[x][0] * delta_o
			delta_h.append(sigmid[x] * (1 - sigmid[x]) * sumwd)

		#update the weight
		for x in xrange(0, len(mat2)):
			mat2[x][0] = mat2[x][0] + delta_o * sigmid[x] * learning_rate

		for x in xrange(0, len(mat1)):
			for y in xrange(0, len(mat1[0])):
				mat1[x][y] = mat1[x][y] + delta_h[y] * data2D[d][x] * learning_rate

	sys.stdout.write(str(error) + "\n")
		# if it == 9999:
		# 	print sigout

sys.stdout.write("TRAINING COMPLETED! NOW PREDICTING.\n")
data2D = []
mean = [0.0, 0.0, 0.0, 0.0]
stddev = [0.0, 0.0, 0.0, 0.0]
count = 0

title = []
line = testfile.readline()
title = line.strip("\r\n").split(',')
while 1:
	line = testfile.readline()
	if not line:
		break
	line = line.strip("\r\n").split(',')
	data1 = []
	data1.append(float(line[0]))
	data1.append(float(line[1]))#
	data1.append(YesNoMap[line[2]])
	data1.append(YesNoMap[line[3]])
	data2D.append(data1)
	count = count + 1
	for i in xrange(0, len(data1)):
		mean[i] = mean[i] + data1[i] 

#normalize
for i in xrange(0, len(mean)):
	mean[i] = mean[i] / count
for d in xrange(0, len(data2D)):
	for i in xrange(0, len(mean)):
		stddev[i] = stddev[i] + (data2D[d][i] - mean[i]) ** 2
for i in xrange(0, len(mean)):
	stddev[i] = stddev[i] / count
	stddev[i] = stddev[i] ** 0.5

for d in xrange(0, len(data2D)):
	for i in xrange(0, len(mean)):
		data2D[d][i] = (data2D[d][i] - mean[i]) / stddev[i]

error = 0.0
for d in xrange(0, len(data2D)):
	mid = multiply1D(data2D[d], mat1)
	sigmid = sigmoid1D(mid)
	output = multiply1D(sigmid, mat2)[0]
	sigout = sigmoid0D(output)
	if sigout > 0.5:
		sys.stdout.write("yes\n")
	else:
		sys.stdout.write("no\n")
	# delta_o = sigout * (1 - sigout) * (label[d] - sigout)
	# error = error + (label[d] - sigout) ** 2
# print error
