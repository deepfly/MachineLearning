import scipy
import math

def multiply1D(a, b):
	result = []
	for k in xrange(0, len(b[0])):
		temp = 0.0
		for i in xrange(0, len(a)):
			temp = temp + a[i] * b[i][k]
		result.append(temp)
	return result

def sigmoid1D(x):
	x2 = x
	for i in xrange(0, len(x)):
	 	x2[i] = 1 / (1 + math.e ** (0.0 - x2[i]))
	return x2

a = [1, 0.1, 1]
b = [[1,2], [2, 1], [3, 4]]
c = multiply1D(a, b)
print sigmoid1D(c)