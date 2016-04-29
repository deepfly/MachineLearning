########################################################################
# File: partB.py
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

def toIndex(line):
	index = 0
	for i in xrange(0, 4):
		x = line[i].split(' ')[1]
		if x == "Male":
			index = index + 8
		elif x == "Young":
			index = index + 4
		elif x == "Yes":
			if i == 2:
				index = index + 2
			elif i == 3:
				index = index + 1
	return index

versionSpace = []
def generateVS(remainingH, begin):
	if begin == 16:
		versionSpace.append(remainingH)
	for i in xrange(begin,16):
		if remainingH[i] == 0:
			newH1 = list(remainingH)
			newH1[i] = 1
			generateVS(newH1, i + 1)
			newH2 = list(remainingH)
			newH2[i] = -1
			generateVS(newH2, i + 1)
			break

			

inputfilepath = sys.argv[1]
label4 = open('./4Cat-Train.labeled', 'r')
testfile = open(inputfilepath, 'r')

num = 4
sys.stdout.write(str(2**num) + '\n')#1
sys.stdout.write(str(2**(2**num)) + '\n')#2

S = [["!", "!", "!", "!"]]# most specific hypotheses
G = [["?", "?", "?", "?"]]# most general hypotheses

remainingH = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
count = 16
# 'List-Then-Eliminate' algorithm
for line in label4:
	line = line.split('\t')
	label = line[4].split(' ')[1].replace("\r\n", "")# high or low
	
	index = toIndex(line)

	if label == "high":
		remainingH[index] = 1
		count = count - 1
	else:
		remainingH[index] = -1
		count = count - 1

# print remainingH
generateVS(remainingH, 0)
# print versionSpace
	
sys.stdout.write(str(2**count) + "\n")#3 size of version space

for line in testfile:
	line = line.split('\t')
	d = []
	# remove from G any hypothesis inconsistent with d
	index = toIndex(line)
	high = 0
	low = 0
	for hp in versionSpace:
		if hp[index] == -1:
			low = low + 1
		else:
			high = high + 1
	sys.stdout.write(str(high) + " " + str(low) + "\n")
# sys.stdout.write('\n')#3 the size of that version space