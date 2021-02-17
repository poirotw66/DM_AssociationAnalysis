import logging
import numpy as np
import pandas as pd
from time import time

def ds_load_groceries(ds):
    '''
    Read itemsets from csv dataset.
    Parameters
    ----------
    ds : string
        data path.

    Returns
    ----------
    trans : numpy.ndarray
    	array containing all transactions
    items : numpy.ndarray
    	list containing all the unique items.
    '''
    data = pd.read_csv(ds, header=0).fillna('')
    _trans = data.values[:, :]
    trans = np.array([np.delete(np.unique(x), 0) for x in _trans])
    num_dataset = len(_trans)
    return trans, num_dataset

def Ibm(ds):
        with open(ds, encoding='utf-8') as f:
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



def ds_load_IBM(ds):
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
    dataset =Ibm(ds)
    num_dataset = len(dataset)
    num_item = np.unique(np.hstack(dataset))
    # data = pd.read_csv(ds,
    #         dtype=object).fillna('-999')
    # _dataset = data.values[:, 1:]
    # dataset = np.array([np.delete(
    #     x, np.where(x=='-999')[0]) for x in _dataset])

    # num_dataset = len(_dataset)
    # num_item = np.unique(np.hstack(dataset))
    return dataset, num_dataset, num_item

def ds_load_lastfm(ds):
    lastfm1 = pd.read_csv(ds)
    lastfm = lastfm1.copy()[['user', 'artist']]
    lastfm = lastfm.drop_duplicates()

    num_dataset = len(lastfm['user'].unique())
    num_item = len(lastfm['artist'].unique())
    dataset = []
    for i in lastfm['user'].unique():
        dataset.append((list(
            lastfm[lastfm['user'] == i]['artist'].values)))
    return np.array(dataset), num_dataset, num_item


def C1_itemset(trans):
    '''
    Create C1 itemset from transaction.
    Parameters
    ----------
    C1 : dataframe
        transaction information.

    Returns
    ----------
    C1_item : list
    	C1 itemset
    '''    
    C1_item = []
    for t in trans:
        for i in t:
            if not [i] in C1_item:
                C1_item.append([i])
    C1_item.sort()
    return list(map(frozenset, C1_item))

def gen_freqset(Ck, trans, min_sup):
    '''
    Estimate candidate frequent itemset (Ck) and its support
    Parameters
    ----------
    Ck : list of frozenset
        candidate frequent itemset
    trans: np.adarray
        transaction informaton
    min_sup: int
        number of minimum support

    Returns
    ----------
    freqset: list of frozenset
        k-th frequent itemset
    
    freqlist: list of frozenset
        list of k-th frequent itemset

    nonfreqlist : list of frozenset
    	list of k-th nonfrequent itemset
    '''    
    # estimate candidate frequent itemset (Ck)
    Cdict_tmp = {}
    for ct, p in enumerate(Ck):
        Cdict_tmp[frozenset(p)]=0

    Cdict_tmp_id = list(Cdict_tmp.keys()) 
    for i in range(len(trans)):
        for tid in Cdict_tmp_id:
            if tid.issubset(trans[i]):
                Cdict_tmp[tid]+=1

    freqset = {}
    freqlist = []
    nonfreqlist = []
    for k in Cdict_tmp_id:
        if Cdict_tmp[k] >= min_sup:
            freqset[k] = Cdict_tmp[k]
            freqlist.append(k)
        else:
            nonfreqlist.append(k) 
    freqlist = list(freqset.keys())
    return freqset, freqlist, nonfreqlist

def gen_candidate(freqlist, nonfreqlist):
    '''
    Generate candidate frequent itemset C(k)
    Parameters
    ----------
    freqlist : list of frozenset 
        frequent itemset C(k)
    nonfreqlist: list of frozenset
        nonfrequent itemset   

    Returns
    ----------
    C(k) : list of frozenset
    	C(k+1)) itemset
    '''    
    Ck = []
    for i in range(len(freqlist)):
        for j in range(i+1, len(freqlist)):
            tmp1 = freqlist[i]
            tmp2 = freqlist[j]
            # for C1
            if len(tmp1)==1: 
                if list(tmp1)[:-1] == list(tmp2)[:-1]:
                    tmp3 = []
                    tmp3.extend(list(tmp1))
                    tmp3.append(list(tmp2)[-1])
                    Ck.append(sorted(tmp3))
            # for {Ck, k>=2}
            else:            
                superset = tmp1|tmp2
                check_subset = np.all(np.array(
                    [i.issubset(superset) for i in nonfreqlist]) == False)
                if check_subset:
                    #print(tmp1|tmp2)
                    Ck.append(tmp1|tmp2)
    return Ck

def Freqsets_brute(trans, min_sup):
    '''
    Main function to generate frequent itemset
    of apriori algorithm by brute-force method
    Parameters
    ----------
    trans: np.adarray
        transaction informaton
    min_sup: int
        number of minimum support

    Returns
    ----------
    freqsets: list of frozenset
        k-th frequent itemset
    
    Cks: list of frozenset
        (k+1)-th candidate frequent itemset
    
    t_res: list
        computation time during each iteration
    '''   

    freqsets = []
    Cks = []
    t_res = []
    k = 1
    Ck = None
    C1 = C1_itemset(trans)
    while True:
        t1 = time()
        if k == 1:
            C = C1
        else:
            C = Ck
        # generate frequent itemset
        freqset, freqlist, nonfreqlist = gen_freqset(C, trans, min_sup)
        # generate Lk
        freqsets.append(freqset)

        # generate Ck
        Ck = gen_candidate(freqlist, nonfreqlist)
        Cks.append(Ck)

        t2 = time()
        t_res.append(t2-t1)
        logging.info(f'C{k} iteration: {t2-t1:.4f} seconds')
        if len(Ck) == 0:
            break
        k+=1
    return freqsets, Cks, t_res

def merge_freqsets(freqsets):
    '''
    Merge all frequent itemsets for confidence estimating
    ----------
    freqsets: list
        lists dictionaries of frequent itemsets

    Returns
    ----------
    db_freqset: dict
        dictionaries of all frequent itemsets
    '''  
    db_freqset = {}
    for i in range(len(freqsets)):
        db_freqset.update(freqsets[i])
    return db_freqset

def subset_freqsets(freqsets):
    subset = []
    x = len(freqsets) 
    for i in range(1, (1 << x)-1): 
        sub = [freqsets[j] for j in range(x) if (i & (1 << j))]
        subset.append(frozenset(sub))
    return subset

def subset_condFPTree(rev_freqsets):
    _subset = []
    x = len(rev_freqsets) 
    for i in range(1, (1 << x)): 
        sub = [rev_freqsets[j] for j in range(x) if (i & (1 << j))]
        _subset.append(frozenset(sub))
    subset = []
    for i in range(len(_subset)):
        if frozenset(rev_freqsets[0]).issubset(_subset[i]):
            subset.append(_subset[i])
    return subset

