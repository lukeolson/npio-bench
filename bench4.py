"""bench4, Using np.memmap, write a numpy array of increasing size."""

import os
from time import time
import numpy as np


def bench(nlist, ntests=5, outname='bench4.npz'):
    """
    Parameters
    ----------
    nlist : array-like
        List if sizes to tests in MB
    ntests : int
        Number of tests to run
    outname : string
        tlist, mblist are also written to file `outname` or `outname.npz`

    Return
    ------
    tlist : ndarray
        List of times, ntests x len(nlist)
    mblist : ndarray
        List of MB
    """

    tlist = np.zeros((ntests, len(nlist)))
    mblist = np.zeros(len(nlist))

    for j, n in enumerate(nlist):
        # set the array
        avec = np.random.rand(n)
        mb = avec.nbytes / 1024 / 1024

        print(f'test {j+1} of {len(nlist)} ({mb:.1f} MB)')
        mblist[j] = mb

        # open / write
        for i in range(ntests):
            fname = f'test-{n}-{i}.bin'

            tstart = time()
            f = np.memmap(fname, dtype=avec.dtype, mode='w+', shape=avec.shape)
            f[:] = avec[:]
            del f  # flush memory to disk, then delete object
            tend = time()
            tlist[i, j] = tend - tstart

            if os.path.exists(fname):
                os.remove(fname)

    if outname is not None:
        np.savez(outname, tlist=tlist, mblist=mblist)


if __name__ == '__main__':
    # list of sizes in MB
    nlist = [1024 * 128 * int(k) for k in np.logspace(1, 2, 8)]
    ntests = 10
    bench(nlist, ntests, 'bench4.npz')
