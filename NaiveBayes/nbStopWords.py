########################################################################
# File: nbStopWords.py
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

def topwords(n):
	file = open(sys.argv[1], 'r')
	wordmap = {}
	topn = []

	while 1:
		line = file.readline()
		if not line:
			break
		line = line.strip('\r\n')
		file2 = open(line, 'r')
		while 1:
			line2 = file2.readline()
			if not line2:
				break
			line2 = line2.strip('\r\n').lower()
			if wordmap.has_key(line2):
				wordmap[line2] = wordmap[line2] + 1
			else:
				wordmap[line2] = 1

	sortedmap = sorted(wordmap.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
	for i in xrange(0,n):
		topn.append(sortedmap[i][0])
	return topn

todel = topwords(int(sys.argv[3]))
# print libtodel
# print contodel
file = open(sys.argv[1], 'r')
wordmap = {}
wordlib = {}
wordcon = {}
wcountlib = 0
wcountcon = 0
countlib = 0
countcon = 0
isLib = False
# st = set([])
while 1:
	line = file.readline()
	if not line:
		break
	line = line.strip('\r\n')
	if line[0] == 'l':
		isLib = True
		countlib = countlib + 1
	else:
		isLib = False
		countcon = countcon + 1
	file2 = open(line, 'r')
	while 1:
		line2 = file2.readline()
		if not line2:
			break
		line2 = line2.strip('\r\n').lower()
		if line2 in todel:
			continue
		if wordmap.has_key(line2):
			wordmap[line2] = wordmap[line2] + 1
		else:
			wordmap[line2] = 1
		if isLib:
			if wordlib.has_key(line2):
				wordlib[line2] = wordlib[line2] + 1
			else:
				wordlib[line2] = 1

			if not wordcon.has_key(line2):
				wordcon[line2] = 0
			wcountlib = wcountlib + 1
		else:
			if wordcon.has_key(line2):
				wordcon[line2] = wordcon[line2] + 1
			else:
				wordcon[line2] = 1

			if not wordlib.has_key(line2):
				wordlib[line2] = 0
			wcountcon = wcountcon + 1

# print st
for (k, v) in wordlib.items():
	prob = 1.0 * (v + 1) / (wcountlib + len(wordmap))
	wordlib[k] = prob
for (k, v) in wordcon.items():
	prob = 1.0 * (v + 1) / (wcountcon + len(wordmap))
	wordcon[k] = prob

plib = 1.0 * countlib / (countcon + countlib)
pcon = 1.0 - plib

right = 0
total = 0
file = open(sys.argv[2], 'r')
while 1:
	line = file.readline()
	if not line:
		break
	line = line.strip('\r\n')
	total = total + 1
	if line[0] == 'l':
		isLib = True
	else:
		isLib = False
	file2 = open(line, 'r')
	postlib = math.log(plib)
	postcon = math.log(pcon)
	while 1:
		line2 = file2.readline()
		if not line2:
			break
		line2 = line2.strip('\r\n').lower()
		if wordlib.has_key(line2):
			postlib = postlib + math.log(wordlib[line2])
		if wordcon.has_key(line2):
			postcon = postcon + math.log(wordcon[line2])
	# print "l" + str(postlib)
	# print "c" + str(postcon) + ","
	if postcon > postlib:
		print 'C'
		if not isLib:
			right = right + 1
	else:
		print 'L'
		if isLib:
			right = right + 1

accuracy = 1.0 * right / total
# print right
# print total
print ("Accuracy: %.04f"%(accuracy))