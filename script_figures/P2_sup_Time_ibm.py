import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Helvetica'
plt.rcParams['font.size'] = 14

outpath = '../figures'
outfig = os.path.join(outpath, 'fig02_sup_Time_ibm.png')
if not os.path.exists(outpath):
    os.makedirs(outpath)
# groceries dataset
sup = np.array(['Low sup,Low conf','Low sup,High conf','High sup,Low conf','High sup,High conf'])
ap = np.array([7.88, 8.48, 0.93, 0.93])
fp = np.array([0.03, 0.03, 0.02, 0.02,])

fig, ax1 = plt.subplots(figsize=(9, 6))
ax1.plot(sup, ap, color='b', label='Apriori')
ax1.plot(sup, fp, color='k', label='FPGrowth')
ax1.set_xlabel('Support threshold ')
ax1.set_ylabel('Computation time (min_secs)')
ax1.set_title('IBM dataset')
plt.legend()
plt.tight_layout()
plt.savefig(outfig)
plt.show()
