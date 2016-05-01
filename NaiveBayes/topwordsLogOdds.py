########################################################################
# File: topwordsLogOdds.py
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
logodds = {}
wcountlib = 0
wcountcon = 0
countlib = 0
countcon = 0
isLib = False
#learn naive bayes text
#collect all words that occur in training text
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
#calculate the p(v) and p(w|v) probability terms
for (k, v) in wordlib.items():
	prob = 1.0 * (v + 1) / (wcountlib + len(wordmap))
	wordlib[k] = prob
for (k, v) in wordcon.items():
	prob = 1.0 * (v + 1) / (wcountcon + len(wordmap))
	wordcon[k] = prob
for (k, v) in wordlib.items():
	logodds[k] = math.log(wordlib[k] / wordcon[k])

sortedlo = sorted(logodds.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
for i in xrange(0, 20):
	print sortedlo[i][0] + ' ' + ("%.04f"%(sortedlo[i][1]))
print '\n',
for i in xrange(1, 21):
	print sortedlo[0-i][0] + ' ' + ("%.04f"%(0-sortedlo[0-i][1]))