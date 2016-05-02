########################################################################
# File: beta.py
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
	oldb = {}
	newb = {}
	#init
	for (k, v) in emit.items():
		newb[k] = log(1.0)
		# newa[k] = prior[k] * emit[k][line[0]]
	for i0 in xrange(1, len(line)):
		i = len(line) - i0
		oldb = newb
		newb = {}
		for (k, v) in emit.items():
			newb[k] = 0.0
			for (k2, v2) in emit.items():
				if newb[k] == 0.0:
					newb[k]= oldb[k2] + log(trans[k][k2]) + log(emit[k2][line[i]])
				else:
					newb[k] = log_sum(newb[k], oldb[k2] + log(trans[k][k2])+ log(emit[k2][line[i]]))
		
	prob = 0.0
	for (k, v) in newb.items():
		if prob == 0.0:
			prob = log(prior[k]) + log(emit[k][line[0]]) + v
		else:
			prob = log_sum(prob, log(prior[k]) + log(emit[k][line[0]]) + v)
		# prob = prob + v

	print str(prob)

