########################################################################
# File: nbStopWords.py
# Version: 4 May 2016 (ZZ)
#
# Description:
#
#      It will take a set of labeled training examples file list
#  (formatted like split.train) and a set of test examples files
#  list(formatted like split.test), and classify them using a 
#  Naive Bayes classifier.
#      The toppest n frequent occurred words will be ignored during
#  counting.
#
# Usage:
#      
#      python nbStopWords.py <split.train> <split.test> <number: top n>
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

# todel stores a list of all the top words to ignore in the text files.
todel = topwords(int(sys.argv[3])) #The param is the number of top words to find.

file = open(sys.argv[1], 'r') #This file is a list of text files.
wordmap = {} #Store the count for each word
wordlib = {} #Store the count for each word appeared in lib file
wordcon = {} #Store the count for each word appeared in con file
wcountlib = 0 #count of words in all lib files
wcountcon = 0 #count of words in all con files
countlib = 0 #count of lib files
countcon = 0 #count of con files
isLib = False

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

# print the accuracy
accuracy = 1.0 * right / total
print ("Accuracy: %.04f"%(accuracy))