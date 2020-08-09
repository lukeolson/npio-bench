"""plot1, plot data from bench1."""

import itertools
import matplotlib.pyplot as plt
import numpy as np

inname = 'bench2.npz'
data = np.load(inname)

tlist = data['tlist']
mblist = data['mblist']

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
fig, ax = plt.subplots(figsize=(8, 4))

for j, color in zip(range(tlist.shape[1]), itertools.cycle(colors)):
    rate = mblist[j] / tlist[:, j]
    rate.sort()
    ax.plot(mblist[j] * np.ones_like(rate), rate, 'o', ms=2, color=color)
    ax.plot(mblist[j], rate.max(), 'v', color=color, ms=2)
    ax.plot(mblist[j], rate.min(), '^', color=color, ms=2)
    ax.plot(mblist[j], rate.mean(), '*', color=color, ms=2)
    ax.plot(mblist[j] * np.ones(2), [rate.min(), rate.max()], '-', lw=0.5, color=color)

ax.semilogx(mblist, mblist / tlist.mean(axis=0), 'k-', lw=1)
ax.set_xlabel('MB')
ax.set_ylabel('MB/sec')
ax.grid(True)

plt.savefig(inname.replace('.npz', '.pdf'))
plt.show()
