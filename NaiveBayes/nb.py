########################################################################
# File: nb.py
# Version: 3 May 2016 (ZZ)
#
# Description:
#
#      It will take a set of labeled training examples file list
#  (formatted like split.train) and a set of test examples files
#  list(formatted like split.test), and classify them using a 
#  Naive Bayes classifier.
#
# Usage:
#      
#      python nb.py <split.train> <split.test>
#
# @author: Ziping Zheng
#
#########################################################################
import sys
import math

file = open(sys.argv[1], 'r') #This file is a list of text files.
wordmap = {} #Store the count for each word
wordlib = {} #Store the count for each word appeared in lib file
wordcon = {} #Store the count for each word appeared in con file
wcountlib = 0 #count of words in all lib files
wcountcon = 0 #count of words in all con files
countlib = 0 #count of lib files
countcon = 0 #count of con files
isLib = False 

#1. learn naive bayes text
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
	#from each file in the list collect the data from the text.
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
			# if the word does not appear in lib file, 
			# it should also be stored in wordlib with count 0.
			if not wordcon.has_key(line2):
				wordcon[line2] = 0
			wcountlib = wcountlib + 1
		else:
			if wordcon.has_key(line2):
				wordcon[line2] = wordcon[line2] + 1
			else:
				wordcon[line2] = 1
			# if the word does not appear in con file, 
			# it should also be stored in wordcon with count 0.
			if not wordlib.has_key(line2):
				wordlib[line2] = 0
			wcountcon = wcountcon + 1

# calculate p(w|v) probability terms
for (k, v) in wordlib.items():
	prob = 1.0 * (v + 1) / (wcountlib + len(wordmap))
	wordlib[k] = prob
for (k, v) in wordcon.items():
	prob = 1.0 * (v + 1) / (wcountcon + len(wordmap))
	wordcon[k] = prob

# calculate p(v)
plib = 1.0 * countlib / (countcon + countlib)
pcon = 1.0 - plib

#2. classify naive bayes text
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

	# use the MAP to find the more probable classification
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

	# calculate the accuracy using the label
	if postcon > postlib:
		print 'C'
		if not isLib:
			right = right + 1
	else:
		print 'L'
		if isLib:
			right = right + 1

# look at the accuracy
accuracy = 1.0 * right / total
print ("Accuracy: %.04f"%(accuracy))