########################################################################
# File: alpha.py
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
from math import *
from logsum import *
import sys

dev = open(sys.argv[1], 'r')
hmmtrans = open(sys.argv[2], 'r')
hmmemit = open(sys.argv[3], 'r')
hmmprior = open(sys.argv[4], 'r')

dev_prob = open('devprobs.txt', 'w')

prior = {}
trans = {}
emit = {}

while 1:
	line = hmmprior.readline()
	if not line:
		break
	line = line.strip('\r\n').split(' ')
	prior[line[0]] = float(line[1])
# print prior

while 1:
	line = hmmtrans.readline()
	if not line:
		break
	line = line.strip(' \r\n').split(' ')
	key = line[0]
	value = {}
	for i in xrange(1, len(line)):
		temp = line[i].split(':')
		value[temp[0]] = float(temp[1])
	trans[key] = value
# print trans

while 1:
	line = hmmemit.readline()
	if not line:
		break
	line = line.strip(' \r\n').split(' ')
	key = line[0]
	value = {}
	for i in xrange(1, len(line)):
		temp = line[i].split(':')
		value[temp[0]] = float(temp[1])
	emit[key] = value
# print emit

while 1:
	line = dev.readline()
	if not line:
		break
	line = line.strip('\r\n').strip(' ').split(' ')
	olda = {}
	newa = {}
	#init
	for (k, v) in emit.items():
		newa[k] = log(prior[k] * emit[k][line[0]])
		# newa[k] = prior[k] * emit[k][line[0]]
	for i in xrange(1, len(line)):
		olda = newa
		newa = {}
		for (k, v) in emit.items():
			sigma = 0.0
			for (k2, v2) in emit.items():
				if sigma == 0.0:
					sigma = olda[k2] + log(trans[k2][k])
				else:
					sigma = log_sum(sigma, olda[k2] + log(trans[k2][k]))
				# sigma = sigma + olda[k] * trans[k2][k]
			# print sigma
			newa[k] = sigma + log(emit[k][line[i]])
			# newa[k] = sigma * emit[k][line[i]]
	prob = 0.0
	for (k, v) in newa.items():
		if prob == 0.0:
			prob = v
		else:
			prob = log_sum(prob, v)
		# prob = prob + v

	print str(prob)

