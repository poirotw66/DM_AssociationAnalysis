import numpy as np
import pandas as pd
import os
import time
import sys

#初始化tree
class tree:
    def __init__(self,nodeName, count, nodeParent):
        self.nodeName = nodeName
        self.next_SilmIer_item = None   
        self.nodeParent = nodeParent
        self.count = count        
        self.children = {}
    def updatec (self, count):
        self.count += count 
#掃描資料庫讀取pattern次數,儲存forzen陣列
def trans2frozen(dataSet):
	frozenDataSet = {}
	for elem in dataSet:
		frozenDataSet[frozenset(elem)] = 1
	return frozenDataSet


#建立FPtree建立FPtree
def createFPtree(frozenDataSet, minSupport):
	freqNode = {}  
	for transactions in frozenDataSet:
		for item in transactions:
			item = str(item)
			freqNode[item] = freqNode.get(item, 0) + frozenDataSet[transactions]


	freqNode = {k: v for k, v in freqNode.items() if v >= minSupport} 
	frequentItemSet = set(freqNode.keys()) 

	if len(frequentItemSet) == 0: return None, None

	for k in freqNode:

		freqNode[k] = [freqNode[k], None]

	fptree = tree("null", 1, None)

	for transactions, count in frozenDataSet.items():
		rec_frqitems = dict()
		for item in transactions:
			if item in frequentItemSet:
				rec_frqitems[item] = freqNode[item][0]
		if len(rec_frqitems) > 0:

			ordFrqitems = [v[0] for v in sorted(rec_frqitems.items(), key=lambda v: v[1],
														 reverse=True)]
			updateTree(fptree, ordFrqitems, freqNode, count)

	return fptree, freqNode

#更新FP tree
def updateTree(fptree, ordFrqitems, freqNode, count):

	firstOrderItem = ordFrqitems[0]
	if firstOrderItem in fptree.children:
		fptree.children[firstOrderItem].updatec(count)
	else:
		fptree.children[firstOrderItem] = tree(firstOrderItem, count,
												   fptree)

		if freqNode[firstOrderItem][1] == None: 
			freqNode[firstOrderItem][1] = fptree.children[
				firstOrderItem]  
		else:
			updatefreqNode(freqNode[firstOrderItem][1],
									 fptree.children[firstOrderItem]) 

	if (len(ordFrqitems) > 1):  
		updateTree(fptree.children[firstOrderItem], ordFrqitems[1:], freqNode, count)
		

def updatefreqNode(headFrequentNode, targetNode):
	while (headFrequentNode.next_SilmIer_item != None):
		headFrequentNode = headFrequentNode.next_SilmIer_item  
	headFrequentNode.next_SilmIer_item = targetNode  

#從FPtree上關聯
def mining_FPtree(freqNode, suffix, freqPat, minSupport):

	if (freqNode == None): return
	frequenctItems = [v[0] for v in sorted(freqNode.items(),
										   key=lambda v: v[1][0])]  
	if (len(frequenctItems) == 0): return

	for frequenctItem in frequenctItems:
		newSuffix = suffix.copy()
		newSuffix.add(frequenctItem)
		support = freqNode[frequenctItem][0]  
		freqPat[frozenset(newSuffix)] = support  
		suffixPath = getSuffixPath(freqNode, frequenctItem)
		if (suffixPath != {}):
			conditionalFPtree, conditionalFNodeTable = createFPtree(suffixPath, minSupport)

			if conditionalFNodeTable != None:  
				mining_FPtree(conditionalFNodeTable, newSuffix, freqPat,
							  minSupport)  
#suffix路徑
def getSuffixPath(freqNode, frequenctItem):
	suffixPath = {}
	beginNode = freqNode[frequenctItem][1]  
	suffixs = ascendNodeList(beginNode) 
	if ((suffixs != [])):
		suffixPath[
			frozenset(suffixs)] = beginNode.count

	while (beginNode.next_SilmIer_item != None):
		beginNode = beginNode.next_SilmIer_item
		suffixs = ascendNodeList(beginNode)
		if (suffixs != []):
			suffixPath[frozenset(suffixs)] = beginNode.count

	return suffixPath


def ascendNodeList(tree):
	suffixs = []
	while ((tree.nodeParent != None) and (tree.nodeParent.nodeName != 'null')):
		tree = tree.nodeParent
		suffixs.append(tree.nodeName)
	return suffixs


def rule_generator(freqPat, minConf, rules):
	for frequentset in freqPat:
		if (len(frequentset) > 1):
			get_rule(frequentset, frequentset, rules, freqPat, minConf)
			


def temstr(set, str):
	tempSet = []
	for elem in set:
		if (elem != str):
			tempSet.append(elem)
	tempFrozenSet = frozenset(tempSet)
	return tempFrozenSet


def get_rule(frequentset, currentset, rules, freqPat, minConf):  
	for frequentElem in currentset:
		subSet = temstr(currentset, frequentElem) 
		confidence = freqPat.get(frequentset) / freqPat.get(subSet, 9999)
		if (confidence >= minConf):
			flag = False
			for rule in rules:
			
				if (rule[0] == subSet and rule[1] == frequentset - subSet):
					flag = True
			if (flag == False):
				rules.append((subSet, frequentset - subSet, confidence))
			

			if (len(subSet) >= 2): 
				get_rule(frequentset, subSet, rules, freqPat, minConf)
			


def get_pat(pattern):
	maxVal = max(pattern.items())[1]
	dictpattern = {}
	for i in range(1, maxVal + 10):
		dictpattern[str(i)] = []

	for key, value in pattern.items():
		dictpattern[str(len(key))].append([key, value])

	for i in range(1, maxVal + 10):
		patterns = dictpattern[str(i)]
		if len(patterns) > 0:
			print("{}-items set :{}".format(str(i),len(patterns)))
			[print("items:{} , support:{} ".format(set(item[0]), item[1])) for item in patterns]
			print()


if __name__ == '__main__':
	def Kaggle():
		Market_data = pd.read_csv('../dataset/marketbasket_kaggle.csv', encoding='utf-8',header = None)
        #進行資料的前處理
		sell_list = []
		for i,items in Market_data.iterrows():
			item_list = []
			for j in items:
				if str(j) != 'nan':
					item_list.append(j)
				else:
					break

			sell_list.append(item_list)
		return sell_list


	def Ibm():
		# read data from Ibm
		with open('../dataset/IBM_dataset.csv', encoding='utf-8') as f:
			content = f.readlines()

		content = [x.strip() for x in content]

		Transaction = {}
		Frequent_items_value = {}



		for i in range(0, len(content)):
			rowd = content[i].split(' ')
			rowd = [r for r in rowd if r != '']
			rowd = rowd[1:]
			if Transaction.get(rowd[0], None) == None:
				Transaction[rowd[0]] = [rowd[1]]
			else:
				Transaction[rowd[0]].append(rowd[1])
		
		return list(Transaction.values())



	fn = str(sys.argv[1])
	minSup = int(sys.argv[2])
	minConf = float(sys.argv[3])
	print('fileName = {} ,minSup= {} , minConf={}'.format(fn, minSup, minConf))

	starttime = time.time()
	if fn == 'kaggle':
		dataSet = Kaggle()
	elif fn == 'ibm':
		dataSet = Ibm()

	frozenDataSet = trans2frozen(dataSet) 
	fptree, freqNode = createFPtree(frozenDataSet, minSup)
	freqPat = {}

	suffix = set([])
	mining_FPtree(freqNode, suffix, freqPat, minSup)

	rules = []
	endtime = time.time()
	print("fptree:")
	print("\nTime Taken is: {0:.2f}ms \n".format((endtime - starttime)))

	print("frequent patterns:")
	get_pat(freqPat)

	print("association rules:")
	rule_generator(freqPat, minConf, rules)
	rules = [rule for rule in rules if rule != None]
	[print('Rules:{}->{}, confidence:{:.3f}'.format(set(r[0]), set(r[1]), r[2])) for r in rules]
