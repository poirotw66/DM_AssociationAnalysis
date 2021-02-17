import os
import sys
sys.path.append('../')
import logging
import numpy as np
import pandas as pd
from time import time
from algorithms.Alg_apriori import *
logging.basicConfig(level=logging.INFO,
            format='%(levelname)s : %(asctime)s : %(message)s')
t_start = time()
## basic information
ds = '../dataset/marketbasket_kaggle.csv'
outpath = '../output/marketbasket_apriori'
if not os.path.exists(outpath):
    os.makedirs(outpath)

## 1. Generate frequent itemset
dataset, num_dataset = ds_load_groceries(ds)
min_sup = 75
min_conf = 0.4
min_lift = 1
sup = min_sup/num_dataset
out_rule = os.path.join(outpath, 
        f'apiori_rules_basket_sup{sup:.2f}_conf{min_conf}.csv')
out_pattern = os.path.join(outpath, 
        f'apiori_pattern_basket_sup{sup:.2f}.csv')

freqsets, Cks, t_res = Freqsets_brute(dataset, min_sup)
db_freqset = merge_freqsets(freqsets)
# remove {}
if {} in freqsets:
    freqsets.remove({})
fqset_dict = merge_freqsets(freqsets[1:])

fq_pattern = []
for k, v in enumerate(fqset_dict):
    fq_pattern.append(
        {
            'pattern': set(v),
            'count':fqset_dict[v]
        }
    )
pattern_df = pd.DataFrame(fq_pattern)

## 2. Generate association rules
rules = []
fqsets_item = list(map(list, fqset_dict.keys()))
for i in range(len(fqsets_item)):
    fqset_item = fqsets_item[i]
    mother_sup = db_freqset[frozenset(fqset_item)]
    subsets = subset_freqsets(fqset_item)

    fqset_info = []
    for j in range(len(subsets)):
        antecdent = subsets[j]
        consequent = frozenset(fqset_item)-antecdent
        subset_sup = db_freqset[antecdent]
        res_sup = db_freqset[consequent]

        conf = mother_sup/subset_sup
        lift = conf / (res_sup/num_dataset)

        rule_dict = {
            "rule": f"{set(antecdent)} --> {set(consequent)}",
            "confidence": conf,
            "lift": lift
        }
        rules.append(rule_dict)

## 3. Generate output
rules_df = pd.DataFrame(rules)
rules_final = rules_df[np.logical_and(
                rules_df['confidence']>=min_conf, 
                rules_df['lift']>=min_lift
                )]
#print(rules_final)
pattern_df.to_csv(out_pattern, index=False)
logging.info(f"Created: {out_rule}")
rules_final.to_csv(out_rule, index=False)
logging.info(f"Created: {out_pattern}")

t_end = time()
logging.info(f"End of FPGrowth: {t_end-t_start:.2f}")