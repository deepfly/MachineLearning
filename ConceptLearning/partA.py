########################################################################
# File: partA.py
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

inputfilepath = sys.argv[1]

file9 = open('./9Cat-Train.labeled', 'r')
a4 = open('./partA4.txt', 'w')
file9dev = open('./9Cat-Dev.labeled', 'r')
inputfile = open(inputfilepath, 'r')

num = 0
count = 0
h = {"Gender":"","Age":"","Student?":"","PreviouslyDeclined?":"",
"HairLength":"","Employed?":"","TypeOfColateral":"",
"FirstLoan":"","LifeInsurance":""}
title = ["Gender" ,"Age" ,"Student?" ,"PreviouslyDeclined?" ,
"HairLength" ,"Employed?" ,"TypeOfColateral" ,
"FirstLoan" ,"LifeInsurance" ]
temp = {}
arr = []
joinlist = []
for line in file9:
	line = line.strip("\r\n")
	arr = line.split('\t')
	for pair in arr:
		pair = pair.split(" ")
		temp[pair[0]] = pair[1]
	# print temp
	if temp["Risk"] == "high":
		for k in h.keys():
			if h[k] == '':
				h[k] = temp[k]
			elif h[k] != temp[k]:
				h[k] = "?"
		#print h
	count = count + 1
	if count%30 == 0:
		del joinlist[:]
		for t in title:
			joinlist.append(h[t])
		joinstr = "\t".join(joinlist)
		a4.write(joinstr + '\n')#4


num = len(arr) - 1
sys.stdout.write(str(2**num) + '\n')#1
sys.stdout.write(str(len(str(2**(2**num)))) + '\n')#2
sys.stdout.write(str(3**num + 1) + '\n')#3

total = 0
mis = 0.0
#print h
for line in file9dev:
	total = total + 1
	line = line.strip("\r\n")
	#print line
	arr = line.split('\t')
	label = ""
	predict = "high"
	for pair in arr:
		pair = pair.split(" ")
		if pair[0] == "Risk":
			label = pair[1]
		elif h[pair[0]] != "?" and h[pair[0]] != pair[1]:
			predict = "low"
	if predict != label:
		mis = mis + 1
		#print "miss"
sys.stdout.write(str(mis/total) + '\n')#5

for line in inputfile:
	total = total + 1
	line = line.strip("\r\n")
	#print line
	arr = line.split('\t')
	label = ""
	predict = "high"
	for pair in arr:
		pair = pair.split(" ")
		# print pair
		if pair[0] == "Risk":
			label = pair[1]
		elif h[pair[0]] != "?" and h[pair[0]] != pair[1]:
			predict = "low"
	sys.stdout.write(predict + '\n')#6

