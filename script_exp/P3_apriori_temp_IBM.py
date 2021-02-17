#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import sys
import re 
import csv
from collections import defaultdict
import pandas as pd


# In[2]:


class apriori(object):
    def __init__(self,minSupp,minConf):
        self.minSupp = minSupp
        self.minConf = minConf
    def Scan (self,data):
        itemSet =  self.Candidate(data)          #建立candidate集合
        itemSetCountDict = defaultdict(int)      #預設dictionary的key值
        freqSet = dict()
        self.itemSet = itemSet
        
        freq_1_itemset = self.Levelwish(data,itemSet,itemSetCountDict,self.minSupp)
        
        k = 1
        freq_n_itemset = freq_1_itemset
        while freq_n_itemset != set():
            freqSet[k] = freq_n_itemset
            k += 1
            candidateitemSet = self.joined_itemset(freq_n_itemset,k)
            freq_n_itemset = self.Levelwish(data,candidateitemSet,itemSetCountDict,self.minSupp)
        self.itemSetCountDict = itemSetCountDict
        self.freqSet = freqSet
        return itemSetCountDict ,freqSet
               
        
    #建立candidate集合    
    def Candidate(self, dataset):
        itemSet = set()
        for line in dataset:
            for item in line:
                itemSet.add(frozenset([item]))
        return itemSet
    #建立滿足minmum_Support的Ln集合
    def Levelwish(self, transListSet, itemSet, freqSet, minSupp):
        levelwishSet = set()
        localSet = defaultdict(int)
        for item in itemSet:
            freqSet[item] += sum([1 for trans in transListSet if item.issubset(trans)])
            localSet[item] += sum([1 for trans in transListSet if item.issubset(trans)])
        for item ,cnt in localSet.items():
            if float(cnt) >= minSupp:
                levelwishSet.add(item)
            else:
                None
        return levelwishSet
    
    
    def joined_itemset(self, termSet, k):
        return set([term1.union(term2) for term1 in termSet for term2 in termSet
                    if len(term1.union(term2)) == k])
    
    def specrule(self, rhs):
        if rhs not in self.itemSet:
            print('Input a term contanin in the term-set')
            return None

        rules = dict()
        for key , value in self.freqSet.items():
            for itemSet in value:
                if rhs.issubset(itemSet) and len(itemSet)>1:
                    item_supp = self.support(itemSet)
                    itemSet = itemSet.difference(rhs)
                    conf = item_supp / self.support(itemSet)
                    if conf >= self.minConf:
                        rules[itemSet] = conf
        return rules

    def support(self, item):
        return self.itemSetCountDict[item]
    
    def Kaggle(self):
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
    
    
    def Ibm(self):
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

        
        
    


# In[20]:

''' #kaggle dataset
if __name__ == '__main__':
    
    def Kaggle():
        Market_data = pd.read_csv('Market_Basket_Optimisation.csv', encoding='utf-8',header = None)
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
    
    starttime = time.time()
    minSup = 15
    minConf = 0.7
    
    objApriori = apriori(minSup, minConf)
    dataSet = Kaggle()
    itemCountDict, freqSet = objApriori.Scan(dataSet)
    endtime = time.time()
    print("\nTime Taken is: {0:.2f}ms \n".format((endtime - starttime)))
    for key, value in freqSet.items():
        print('{}-Itemsets:{}'.format(key, len(value)))
        print('-' * 20)
        for itemset in value:
            print("Items :{} , Support:{} ".format(list(itemset), itemCountDict[itemset]))
        print()
    print()
    print('List All Rules:')
    print()
    L1 = set(freqSet[1])
    for rhs in L1:
        rules = objApriori.specrule(rhs)
        if len(rules) > 0:
            for key, value in rules.items():
                print('Rule : {} -> {}, confidence = {}'.format(list(key), list(rhs), value))
'''

# In[21]:


 #ibm dataset
if __name__ == '__main__':
    def Ibm():
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
    
    starttime = time.time()
    minSup = 30
    minConf = 0.9
    
    objApriori = apriori(minSup, minConf)
    dataSet = Ibm()
    itemCountDict, freqSet = objApriori.Scan(dataSet)
    endtime = time.time()
    print("\nTime Taken is: {0:.2f}ms \n".format((endtime - starttime)))
    for key, value in freqSet.items():
        print('{}-Itemsets:{}'.format(key, len(value)))
        print('-' * 20)
        for itemset in value:
            print("Items :{} , Support:{} ".format(list(itemset), itemCountDict[itemset]))
        print()
    print()
    print('List All Rules:')
    print()
    L1 = set(freqSet[1])
    for rhs in L1:
        rules = objApriori.specrule(rhs)
        if len(rules) > 0:
            for key, value in rules.items():
                print('Rule : {} -> {}, confidence = {}'.format(list(key), list(rhs), value))


# In[ ]:




