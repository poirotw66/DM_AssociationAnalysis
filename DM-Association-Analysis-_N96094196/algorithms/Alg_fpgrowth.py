# /home/rick/anaconda3/bin/python
import numpy as np
import pandas as pd
def test_data():
    data = [['a', 'b', 'c'], 
        ['d', 'b', 'a', 'e'],
        ['d', 'e', 'a'],
        ['b', 'a'],
        ['a', 'b', 'd']]
    return data

def ds_load_groceries(ds):
    '''
    Read itemsets from csv dataset.
    Parameters
    ----------
    ds : string
        data path.

    Returns
    ----------
    dataset : dictionaries of frozenset
    	frozenset containing all transactions
    '''
    data = pd.read_csv(ds, header=0).fillna('')
    _trans = data.values[:, :]
    trans = np.array([np.delete(np.unique(x), 0) for x in _trans])
    num_dataset = len(trans)
    num_item = np.unique(np.hstack(trans)).shape[0]
    dataset = {}
    for ele in trans:
        dataset[frozenset(ele)] = 1
    return dataset, num_dataset, num_item

def ds_load_IBM(ds):
    data = pd.read_csv(ds,
            dtype=object).fillna('-999')
    _trans = data.values[:, 1:]
    trans = np.array([np.delete(
        x, np.where(x=='-999')[0]) for x in _trans])

    num_dataset = len(_trans)
    num_item = len(np.unique(np.hstack(trans)))
    dataset = {}
    for ele in trans:
        dataset[frozenset(ele)] = 1
    return dataset, num_dataset, num_item

def ds_load_lastfm(ds):
    lastfm1 = pd.read_csv(ds)
    lastfm = lastfm1.copy()[['user', 'artist']]
    lastfm = lastfm.drop_duplicates()

    num_dataset = len(lastfm['user'].unique())
    num_item = len(lastfm['artist'].unique())
    dataset = {}
    for i in lastfm['user'].unique():
        dataset[frozenset(list(
            lastfm[lastfm['user'] == i]['artist'].values))] = 1
    return dataset, num_dataset, num_item

def load_ds(ds):
    dataset = {}
    for elem in ds:
        dataset[frozenset(elem)] = 1
    return dataset

class TreeNode:
    def __init__(self, nodeName, count, nodeParent):
        self.nodeName = nodeName
        self.count = count
        self.nodeParent = nodeParent
        self.nextSimilarItem = None
        self.children = {}

    def increaseC(self, count):
        self.count += count

def createFPTree(frozenDataSet, min_sup):
    # scan dataset at the first time, 
    # filter out items which are less than min_sup
    hdr_table = {}
    for items in frozenDataSet:
        for item in items:
            hdr_table[item] = \
             hdr_table.get(item, 0) + frozenDataSet[items]
    hdr_table = \
        {k:v for k,v in hdr_table.items() if v >= min_sup}
    frequentItems = set(hdr_table.keys())
    if len(frequentItems) == 0: return None, None

    for k in hdr_table:
        hdr_table[k] = [hdr_table[k], None]
        
    fptree = TreeNode("null", 1, None)
    #scan dataset at the second time, 
    # filter out items for each record
    for items,count in frozenDataSet.items():
        frequentItemsInRecord = {}
        for item in items:
            if item in frequentItems:
                frequentItemsInRecord[item] = \
                            hdr_table[item][0]
        if len(frequentItemsInRecord) > 0:
            orderedFrequentItems = [v[0] for v in
                sorted(frequentItemsInRecord.items(), 
                key=lambda v:v[1], reverse = True)]
            updateFPTree(fptree, 
                orderedFrequentItems, hdr_table, count)

    return fptree, hdr_table

def updateFPTree(fptree, orderedFrequentItems,
                             hdr_table, count):
    #handle the first item
    if orderedFrequentItems[0] in fptree.children:
        fptree.children[orderedFrequentItems[0]].increaseC(count)
    else:
        fptree.children[orderedFrequentItems[0]] = \
                TreeNode(orderedFrequentItems[0], count, fptree)

        #update hdr_table
        if hdr_table[orderedFrequentItems[0]][1] == None:
            hdr_table[orderedFrequentItems[0]][1] = \
                        fptree.children[orderedFrequentItems[0]]
        else:
            updatehdr_table(
                hdr_table[orderedFrequentItems[0]][1],
                fptree.children[orderedFrequentItems[0]])
    #handle other items except the first item
    if(len(orderedFrequentItems) > 1):
        updateFPTree(fptree.children[orderedFrequentItems[0]], 
                orderedFrequentItems[1::], hdr_table, count)

def updatehdr_table(hdr_BeginNode, targetNode):
    while(hdr_BeginNode.nextSimilarItem != None):
        hdr_BeginNode = hdr_BeginNode.nextSimilarItem
    hdr_BeginNode.nextSimilarItem = targetNode

def mineFPTree(hdr_table, prefix, frequentPatterns, min_sup):
    # for each item in hdr_table, find conditional prefix path, 
    # create conditional fptree,
    #  then iterate until there is only one element in conditional fptree
    hdr_Items = [v[0] for v in 
            sorted(hdr_table.items(), key = lambda v:v[1][0])]
    if(len(hdr_Items) == 0): return

    for hdr_Item in hdr_Items:
        newPrefix = prefix.copy()
        newPrefix.add(hdr_Item)
        support = hdr_table[hdr_Item][0]
        frequentPatterns[frozenset(newPrefix)] = support

        prefixPath = getPrefixPath(hdr_table, hdr_Item)
        if(prefixPath != {}):
            cond_FPtree, cond_hdr_table =\
                 createFPTree(prefixPath, min_sup)
            if cond_hdr_table != None:
                mineFPTree(cond_hdr_table, 
                        newPrefix, frequentPatterns, min_sup)

def getPrefixPath(hdr_table, hdr_Item):
    prefixPath = {}
    beginNode = hdr_table[hdr_Item][1]
    prefixs = ascendTree(beginNode)
    if((prefixs != [])):
        prefixPath[frozenset(prefixs)] = beginNode.count

    while(beginNode.nextSimilarItem != None):
        beginNode = beginNode.nextSimilarItem
        prefixs = ascendTree(beginNode)
        if (prefixs != []):
            prefixPath[frozenset(prefixs)] = beginNode.count
    return prefixPath

def ascendTree(treeNode):
    prefixs = []
    while((treeNode.nodeParent != None) and \
        (treeNode.nodeParent.nodeName != 'null')):
        treeNode = treeNode.nodeParent
        prefixs.append(treeNode.nodeName)
    return prefixs

def rulesGenerator(frequentPatterns, rules, num_dataset):
    for frequentset in frequentPatterns:
        if(len(frequentset) > 1):
            getRules(frequentset, frequentset,
                     rules, frequentPatterns, num_dataset)

def removeStr(set, str):
    tempSet = []
    for elem in set:
        if(elem != str):
            tempSet.append(elem)
    tempFrozenSet = frozenset(tempSet)
    return tempFrozenSet


def getRules(frequentset, currentset, rules,
                         frequentPatterns, num_dataset):
    for frequentElem in currentset:
        subSet = removeStr(currentset, frequentElem)
        confidence = frequentPatterns[frequentset] / \
                            frequentPatterns[subSet]
        lift = confidence / \
            (frequentPatterns[frequentset-subSet]/num_dataset)

        if (confidence >= 0):
            flag = False
            for rule in rules:
                if(rule[0] == subSet and \
                        rule[1] == frequentset - subSet):
                    flag = True
            if(flag == False):
                rules.append(( 
                    subSet, frequentset - subSet, confidence, lift))

            if(len(subSet) >= 2):
                getRules(frequentset, 
                    subSet, rules, frequentPatterns, num_dataset)

if __name__=='__main__':
    print("fptree:")
    dataSet = [ ['a', 'b', 'c'], 
                ['d', 'b', 'a', 'e'],
                ['d', 'e', 'a'],
                ['b', 'a'],
                ['a', 'b', 'd']]
    num_dataset = len(dataSet)
    min_sup = 2
    fptree, hdr_table = createFPTree(dataSet, min_sup)
    #fptree.disp()
    frequentPatterns = {}
    prefix = set([])
    mineFPTree(hdr_table, prefix, frequentPatterns, min_sup)
    print("frequent patterns:")
    print(frequentPatterns)
    minConf = 0.6
    rules = []
    rulesGenerator(frequentPatterns, rules, num_dataset)
    print("association rules:")
    print(rules)