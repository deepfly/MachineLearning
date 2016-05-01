########################################################################
# File: nb.py
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

#classify naive bayes text
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
	# print postlib
	# print str(postcon) + ","
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