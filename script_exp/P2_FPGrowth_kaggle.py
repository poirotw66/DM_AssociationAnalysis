import os
import sys
sys.path.append('../')
import logging
import numpy as np
import pandas as pd
from time import time
from algorithms.Alg_fpgrowth import *
logging.basicConfig(level=logging.INFO,
            format='%(levelname)s : %(asctime)s : %(message)s')
t_start = time()
## basic information
ds = '../dataset/marketbasket_kaggle.csv'
outpath = '../output/marketbasket_FPGrowth'
if not os.path.exists(outpath):
    os.makedirs(outpath)

## 1. Generate frequent itemset
dataset, num_dataset, num_item = ds_load_groceries(ds)
min_sup = 225
min_conf = 0.5
min_lift = 1
sup = min_sup/num_dataset
out_rule = os.path.join(outpath, 
        f'FPGrowth_rules_basket_sup{sup:.2f}_conf{min_conf}.csv')
out_pattern = os.path.join(outpath, 
        f'FPGrowth_pattern_basket_sup{sup:.2f}.csv')
fptree, headPointTable = createFPTree(dataset, min_sup)
fqset_dict = {}
prefix = set([])
mineFPTree(headPointTable, prefix, fqset_dict, min_sup)

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
rulesGenerator(fqset_dict, rules, num_dataset)

final_rule = []
for r in rules:
    ant = set(r[0])
    cons = set(r[1])
    confidence = r[2]
    lift = r[3]
    rule_dict = {
        "rule": f"{ant} --> {cons}",
        "confidence": confidence,
        "lift": lift
    }
    final_rule.append(rule_dict)

## 3. Generate output
rules_df = pd.DataFrame(final_rule)
rules_final = rules_df[np.logical_and(
                rules_df['confidence']>=min_conf, 
                rules_df['lift']>=min_lift
                )]
print(rules_final)
rules_final.to_csv(out_rule, index=False)
logging.info(f"Created: {out_rule}")
pattern_df.to_csv(out_pattern, index=False)
logging.info(f"Created: {out_pattern}")

t_end = time()
logging.info(f"End of FPGrowth: {t_end-t_start:.2f}")