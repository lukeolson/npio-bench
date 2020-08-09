"""bench2. Using MPI-IO, write a numpy array of increasing size."""
from mpi4py import MPI
import numpy as np

import os
import numpy as np


def bench(nlist, ntests=5, outname='bench2.npz'):
    """
    Parameters
    ----------
    nlist : array-like
        List if sizes to tests in MB per process
    ntests : int
        Number of tests to run
    outname : string
        tlist, mblist are also written to file `outname` or `outname.npz`
    """

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        tlist = np.zeros((ntests, len(nlist)))
        mblist = np.zeros(len(nlist))

    for j, n in enumerate(nlist):
        # set the array
        avec = np.random.rand(n)
        mb = avec.nbytes / 1024 / 1024

        print(f'test {j+1} of {len(nlist)} ({mb:.1f} MB)')
        if rank == 0:
            mblist[j] = mb * comm.Get_size()  # mb / process x nproc

        # open / write
        for i in range(ntests):
            fname = f'test-{n}-{i}.bin'

            # sync the timers
            comm.Barrier()
            tstart = MPI.Wtime()

            f = MPI.File.Open(comm, fname, MPI.MODE_WRONLY | MPI.MODE_CREATE)
            offset = comm.Get_rank() * avec.nbytes
            f.Write_at_all(offset, avec)
            f.Close()
            tend = MPI.Wtime()

            # grab the time that took the longest (instead of timing an end barrier)
            timeperproc = np.array([tend - tstart])
            maxtime = np.array([0.0])
            comm.Reduce(timeperproc,
                        maxtime,
                        op=MPI.MAX, root=0)
            if rank == 0:
                tlist[i, j] = maxtime[0]

            comm.Barrier()
            if rank == 0:
                if os.path.exists(fname):
                    os.remove(fname)

    if rank == 0:
        if outname is not None:
            np.savez(outname, tlist=tlist, mblist=mblist)


if __name__ == '__main__':
    # list of sizes in MB
    nlist = [1024 * 128 * int(k) for k in np.logspace(1, 2, 8)]
    ntests = 5
    bench(nlist, ntests, 'bench2.npz')
