import numpy as np
import matplotlib.pyplot as plt
import itertools

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

data = np.load('bench1.npz')
tlist = data['tlist']
mblist = data['mblist']

fig, ax = plt.subplots(figsize=(10,10))
#ax.semilogy(mblist, mblist / tlist[0,:])
for j, color in zip(range(tlist.shape[1]), itertools.cycle(colors)):
    rate = mblist[j] / tlist[:, j]
    rate.sort()
    ax.plot(mblist[j]*np.ones_like(rate), rate, 'o', ms=2, color=color)
    ax.plot(mblist[j], rate.max(), 'v', color=color, ms=2)
    ax.plot(mblist[j], rate.min(), '^', color=color, ms=2)
    ax.plot(mblist[j], rate.mean(), '*', color=color, ms=2)
    ax.plot(mblist[j]*np.ones(2), [rate.min(), rate.max()], '-', lw=0.5, color=color)

ax.plot(mblist, mblist / tlist.mean(axis=0), 'k-', lw=1)


plt.show()
