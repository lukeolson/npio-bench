import numpy as np
from time import time
import os

nlist = [1024*128*int(k) for k in np.logspace(1,4,20)] # sizes, in MB
ntests = 5

tlist = np.zeros((ntests, len(nlist)))
mblist = np.zeros(len(nlist))

for j, n in enumerate(nlist):
    print(f'{j} of {len(nlist)}')
    a = np.random.rand(n)

    # open / write
    for i in range(ntests):
        tstart = time()
        fname = f'test-{n}-{i}.bin'
        with open(fname, 'wb') as f:
            a.tofile(f)
        tend = time()
        tlist[i, j] = tend - tstart

        if os.path.exists(fname):
          os.remove(fname)

    mblist[j] = a.nbytes / 1024 / 1024

np.savez('bench1.npz', tlist=tlist, mblist=mblist)
