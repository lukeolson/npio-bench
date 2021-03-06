"""bench3, Using .write(.tobytes()), write a numpy array of increasing size."""

import os
from time import time
import numpy as np


def bench(nlist, ntests=5, outname='bench3.npz'):
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
            with open(fname, 'wb') as f:
                f.write(avec.tobytes())
            tend = time()
            tlist[i, j] = tend - tstart

            if os.path.exists(fname):
                os.remove(fname)

    if outname is not None:
        np.savez(outname, tlist=tlist, mblist=mblist)


if __name__ == '__main__':
    # list of sizes in MB
    #nlist = [1024 * 128 * int(k) for k in np.logspace(1, 3, 8)]
    nlist = [int(1024 * 128 * k) for k in np.logspace(0, 11, 20, base=2)]
    ntests = 10
    bench(nlist, ntests, 'bench3.npz')
