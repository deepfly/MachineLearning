########################################################################
# File: decisionTree.py
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

decisionTree = {}
left_label = {}

def condInfo(pos_map, neg_map, val_set, total):
	info = 0.0
	for val in val_set:
		if pos_map.has_key(val) == False or neg_map.has_key(val) == False:
			continue
		set1 = pos_map[val]
		set2 = neg_map[val]
		if len(set1) == 0 or len(set2) == 0:
			continue
		info = info + 1.0 * len(set1) * math.log(1.0 * (len(set1) + len(set2))/len(set1))/math.log(2) / total
		info = info + 1.0 * len(set2) * math.log(1.0 * (len(set1) + len(set2))/len(set2))/math.log(2) / total
		# print info
	return info

def iniInfo(label_count):
	if label_count[0] == 0 or label_count[1] == 0:
		return 0.0
	length = label_count[0] + label_count[1]
	info = (1.0 * label_count[0] * math.log(1.0 * length/label_count[0])/math.log(2) + 1.0 * label_count[1] * math.log(1.0 * length/label_count[1])/math.log(2)) / length
	return info

def findBest(title, values2D, onlyThese, root):
	best_pos = {}
	best_neg = {}
	val_set = set([])
	min_info = 9999
	for i in xrange(0, len(title)):
		if i == root:
			continue
		pos_map = {}
		neg_map = {}
		pos_row_temp = []
		neg_row_temp = []
		for j in xrange(0, len(values2D)):
			if j not in onlyThese:
				continue
			row = values2D[j]
			val_set.add(row[i])
			if row[len(title)] in postitive_label:
				if pos_map.has_key(row[i]) == False:
					pos_map[row[i]] = [j]
				else:
					row_list = pos_map[row[i]]
					row_list.append(j)
					pos_map[row[i]] = row_list
			else:
				if neg_map.has_key(row[i]) == False:
					neg_map[row[i]] = [j]
				else:
					row_list = neg_map[row[i]]
					row_list.append(j)
					neg_map[row[i]] = row_list
		info = condInfo(pos_map, neg_map, val_set, len(onlyThese))
		if min_info > info:
			root = i
			best_pos = pos_map
			best_neg = neg_map
			min_info = info
	for val in val_set:
		if best_pos.has_key(val) == False:
			best_pos[val] = []
		if best_neg.has_key(val) == False:
			best_neg[val] = []
	return (root, best_pos, best_neg, min_info, val_set)

def errorRatio(values2D1):
	error_pred = 0
	for obs in values2D1:
		node = 1
		# print obs[decisionTree[node]]
		node = node * 2
		if obs[decisionTree[node/2]] != left_label[node/2]:
			node = node + 1

		if decisionTree[node] == 'pos' or decisionTree[node] == 'neg':
			if decisionTree[node] == 'pos' and obs[-1] not in postitive_label:
				error_pred = error_pred + 1
			elif decisionTree[node] == 'neg' and obs[-1] in postitive_label:
				error_pred = error_pred + 1
		else:
			node = node * 2
			if obs[decisionTree[node/2]] != left_label[node/2]:
				node = node + 1

			if decisionTree[node] == 'pos' or decisionTree[node] == 'neg':
				if decisionTree[node] != obs[-1]:
					if decisionTree[node] == 'pos' and obs[-1] not in postitive_label:
						error_pred = error_pred + 1
					elif decisionTree[node] == 'neg' and obs[-1] in postitive_label:
						error_pred = error_pred + 1
	return error_pred

trainFile = open(sys.argv[1], 'r')
testFile = open(sys.argv[2], 'r')

postitive_label = ['A', 'democrat', 'yes']

title = trainFile.readline().split(',')[:-1]

values2D = []
allRow = []
count = 0
label_count = [0, 0]
while 1:
	line = trainFile.readline()
	if not line:
		break
	allRow.append(count)
	count = count + 1

	values = line.strip('\r\n').split(',')
	if values[-1] in postitive_label:
		label_count[0] = label_count[0] + 1
	else:
		label_count[1] = label_count[1] + 1
	values2D.append(values)
sys.stdout.write("[" + str(label_count[0]) + "+/" + str(label_count[1]) + "-]\n")
init_info = iniInfo(label_count)

(root, best_pos_root, best_neg_root, min_info_root, val_set) = findBest(title, values2D, allRow, -1)


if init_info - min_info_root < 0.1:
	exit()
else:
	decisionTree[1] = root
	k = 1
	lvs = list(val_set)
	isLeft = True
	for l in xrange(0, len(lvs)):
		val = lvs[l]
		unionSet = set(best_pos_root[val]) | set(best_neg_root[val])
		if len(best_pos_root[val]) == 0 and len(best_neg_root[val]) == 0:
			continue
		if isLeft == True:
			left_label[k] = lvs[l]
			isLeft = False
		sys.stdout.write(title[root] + " = " + val + ": [" + str(len(best_pos_root[val])) + "+/" + str(len(best_neg_root[val])) + "-]\n")

		onlyThese = set([])
		for row in unionSet:
			onlyThese.add(row)

		label_count2 = []
		label_count2.append(len(best_pos_root[val]))
		label_count2.append(len(best_neg_root[val]))
		init_info2 = iniInfo(label_count2)
		(root2, best_pos2, best_neg2, min_info2, val_set2) = findBest(title, values2D, onlyThese, root)
		k = k + 1
		if len(best_pos_root[val]) > len(best_neg_root[val]):
			decisionTree[k] = 'pos'
		else:
			decisionTree[k] = 'neg'

		# print init_info2
		# print min_info2
		if init_info2 - min_info2 >= 0.1:
			decisionTree[k] = root2
			k2 = k * 2
			lvs2 = list(val_set2)
			isLeft2 = True
			for l2 in xrange(0, len(lvs2)):
				val = lvs2[l2]
				if len(best_pos2[val]) == 0 and len(best_neg2[val]) == 0:
					continue
				if isLeft2 == True:
					left_label[k] = lvs[l2]
					isLeft2 = False
				if len(best_pos2[val]) > len(best_neg2[val]):
					decisionTree[k2] = 'pos'
				else:
					decisionTree[k2] = 'neg'
				k2 = k2 + 1
				sys.stdout.write("| " + title[root2] + " = " + val + ": [" + str(len(best_pos2[val])) + "+/" + str(len(best_neg2[val])) + "-]\n")
		# print decisionTree
		# print left_label

total_obs = len(values2D)
error_pred = errorRatio(values2D)
sys.stdout.write("error(train): " + str(1.0 * error_pred/total_obs) + "\n")

values2D_test = []
while 1:
	line = testFile.readline()
	if not line:
		break
	values = line.strip('\r\n').split(',')
	values2D_test.append(values)
# print values2D_test
total_obs = len(values2D_test) - 1
error_pred = errorRatio(values2D_test[1:])
sys.stdout.write("error(test): " + str(1.0 * error_pred/total_obs) + "\n")



