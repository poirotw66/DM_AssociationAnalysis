import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Helvetica'
plt.rcParams['font.size'] = 14

outpath = '../figures'
outfig = os.path.join(outpath, 'fig03_speed_length.png')
if not os.path.exists(outpath):
    os.makedirs(outpath)

IBM_dict = {
    'n_dataset':829,
    'n_item':8,
    'min_sup':2,
    'Apriori_time':7.88,
    'FPGrowth_time':0.03
}

groceries_dict = {
    'n_dataset':7501,
    'n_item':139,
    'min_sup':2.02,
    'Apriori_time':203.25,
    'FPGrowth_time':0.95
}


ds = [IBM_dict, groceries_dict]
ap_time = [d['Apriori_time'] for d in ds]
fp_time = [d['FPGrowth_time'] for d in ds]
n_dataset = [d['n_dataset'] for d in ds]
n_item = [d['n_item'] for d in ds]
x_tick = ['IBM', 'Groceries']

fig, ax1 = plt.subplots(figsize=(9, 6))
ax2 = ax1.twinx()
ax2.bar(x_tick, n_dataset, color='r', width=0.1, alpha=0.5)
ax1.plot(x_tick, ap_time,  '-o', color='b', label='Apriori')
ax1.plot(x_tick, fp_time,  '-o', color='k', label='FPGrowth')
ax1.legend()
ax1.set_xlabel('Dataset')
ax1.set_ylabel('Computation time (secs)')
ax2.set_ylabel('Dataset length')
plt.tight_layout()
plt.savefig(outfig, dpi=150)
plt.show()

