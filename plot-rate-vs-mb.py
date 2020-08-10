"""plot-rate-vs-mb.py, plot data from bench1.

Usage: python plot-rate-vs-mb.py bench1.npz
"""

import itertools
import matplotlib.pyplot as plt
import numpy as np
import sys
sizes = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']


def whichsize(mb, sizes):
    """
    Find the "size" of mb.
    """
    return sizes[0] if mb < 1024 else whichsize(mb >> 10, sizes[1:])


if len(sys.argv) > 1:
    inname = sys.argv[1]
else:
    inname = 'bench1.npz'
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

# maxsize = whichsize(int(mblist.max()), sizes)
# maxk = sizes.index(maxsize)
# xticks = [n*1024**k for k in (0,1,2) for n in (1,10,100)]
# ax.set_xticks(xticks)

plt.savefig(inname.replace('.npz', '.pdf'))
plt.show()
