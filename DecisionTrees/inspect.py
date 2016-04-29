########################################################################
# File: inspect.py
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

label_count = [0, 0]
values2D_test = []
pos_label = None
line = file.readline()
while 1:
	line = file.readline()
	if not line:
		break
	values = line.strip('\r\n').split(',')
	if pos_label == None:
		pos_label = values[-1]
		label_count[0] = label_count[0] + 1
	else:
		if values[-1] == pos_label:
			label_count[0] = label_count[0] + 1
		else:
			label_count[1] = label_count[1] + 1

minLabel = label_count[0]
if label_count[1] < minLabel:
	minLabel = label_count[1]
error = 1.0 * minLabel / (label_count[0] + label_count[1])
entropy = 1.0 * label_count[0] * math.log(1.0 * (label_count[0] + label_count[1]) / label_count[0]) / math.log(2) / (label_count[0] + label_count[1])
entropy = entropy + 1.0 * label_count[1] * math.log(1.0 * (label_count[0] + label_count[1]) / label_count[1]) / math.log(2) / (label_count[0] + label_count[1])
sys.stdout.write("entropy: " + str(entropy) + "\n")
sys.stdout.write("error: " + str(error))