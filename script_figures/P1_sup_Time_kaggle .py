import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Helvetica'
plt.rcParams['font.size'] = 14

outpath = '../figures'
outfig = os.path.join(outpath, 'fig01_sup_Time_kaggle.png')
if not os.path.exists(outpath):
    os.makedirs(outpath)
# groceries dataset
sup = np.array(['Low sup,Low conf','Low sup,High conf','High sup,Low conf','High sup,High conf'])
ap = np.array([203.25, 215.62, 83.26, 80.79])
fp = np.array([0.95, 0.95, 0.84, 0.84,])

fig, ax1 = plt.subplots(figsize=(9, 6))
ax1.plot(sup, ap, color='b', label='Apriori')
ax1.plot(sup, fp, color='k', label='FPGrowth')
ax1.set_xlabel('Support threshold ')
ax1.set_ylabel('Computation time (min_secs)')
ax1.set_title('Marketbasket dataset')
plt.legend()
plt.tight_layout()
plt.savefig(outfig)
plt.show()
