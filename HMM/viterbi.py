########################################################################
# File: viterbi.py
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
	oldvp = {}
	newvp = {}
	Q = []
	bestStatePath = []
	#init
	for (k, v) in emit.items():
		newvp[k] = log(prior[k] * emit[k][line[0]])
	for i in xrange(1, len(line)):
		oldvp = newvp
		newvp = {}
		Qtemp = {}
		for (k, v) in emit.items():
			toMax = 0.0
			for (k2, v2) in emit.items():
				if toMax == 0.0:
					toMax = oldvp[k2] + log(trans[k2][k])
					Qtemp[k] = k2
				elif oldvp[k2] + log(trans[k2][k]) > toMax:
					toMax = oldvp[k2] + log(trans[k2][k])
					Qtemp[k] = k2
			newvp[k] = toMax + log(emit[k][line[i]])
		Q.append(Qtemp)
		# print Q
	maxLastState = ""
	tempV = 0.0
	for (k, v) in newvp.items():
		# print k, v
		if tempV == 0.0:
			tempV = v
			maxLastState = k
		elif v > tempV:
			tempV = v
			maxLastState = k
	# print maxLastState
	bestStatePath.insert(0, maxLastState)
	for i0 in xrange(0, len(Q)):
		i = len(Q) - 1 - i0
		# print Q[i]
		# print maxLastState
		maxLastState = Q[i][maxLastState]
		bestStatePath.insert(0, maxLastState)
	# print bestStatePath
	print line[0] + "_" + bestStatePath[0],
	for i in xrange(1, len(line)):
		print " " + line[i] + "_" + bestStatePath[i],
	print "\n",

