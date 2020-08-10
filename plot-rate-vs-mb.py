"""plot-rate-vs-mb.py, plot data from bench1.

Usage: python plot-rate-vs-mb.py bench1.npz
"""

import sys
import itertools
import matplotlib.pyplot as plt
import numpy as np

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

# plot some helpful ticks up top
xticks = np.array([n * 1024**k for k in (0, 1, 2) for n in (1, 10, 100)])
xticklabels = []
for x in xticks:
    if x < 1024:
        xticklabels.append(f'{x} MB')
        continue
    if x < 1024 * 1024:
        xticklabels.append(f'{int(x/1024)} GB')
        continue
    xticklabels.append(f'{int(x/1024/1024)} TB')
xticklabels = np.array(xticklabels)
J = np.where((xticks <= mblist.max()) & (xticks >= mblist.min()))[0]
xticks = xticks[J]
xticklabels = xticklabels[J]

ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
ax2.set_xscale('log')
ax2.set_xticks(list(xticks))
ax2.set_xticklabels(list(xticklabels))
ax2.minorticks_off()

plt.savefig(inname.replace('.npz', '.pdf'))
plt.show()
