########################################################################
# File: topwords.py
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

file = open(sys.argv[1], 'r')
wordmap = {}
wordlib = {}
wordcon = {}
countlib = 0
countcon = 0
isLib = False

while 1:
	line = file.readline()
	if not line:
		break
	line = line.strip('\r\n')
	if line[0] == 'l':
		isLib = True
	else:
		isLib = False
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
		if isLib:
			if wordlib.has_key(line2):
				wordlib[line2] = wordlib[line2] + 1
			else:
				wordlib[line2] = 1
			countlib = countlib + 1
		else:
			if wordcon.has_key(line2):
				wordcon[line2] = wordcon[line2] + 1
			else:
				wordcon[line2] = 1
			countcon = countcon + 1

sortedlib = sorted(wordlib.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
sortedcon = sorted(wordcon.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
for i in xrange(0,20):
	prob = 1.0 * (sortedlib[i][1] + 1) / (countlib + len(wordmap))
	print sortedlib[i][0] + ' ' + ("%.04f"%(prob))
print '\n',
for i in xrange(0,20):
	prob = 1.0 * (sortedcon[i][1] + 1) / (countcon + len(wordmap))
	print sortedcon[i][0] + ' ' + ("%.04f"%(prob))
