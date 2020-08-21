"""bench6. Using .tofile, write data with a file-per-rank strategy."""
import os
from mpi4py import MPI
import numpy as np


def bench(nlist, ntests=5, outname='bench6.npz'):
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

        if rank == 0:
            print(f'test {j+1} of {len(nlist)} ({mb:.1f} MB)', flush=True)
            mblist[j] = mb * comm.Get_size()  # mb / process x nproc

        # open / write
        for i in range(ntests):
            fname = f'test-{n}-{i}-{rank}.bin'

            comm.Barrier()
            tstart = MPI.Wtime()
            with open(fname, 'wb') as f:
                avec.tofile(f)
            tend = MPI.Wtime()

            # get max time across ranks
            timeperproc = np.array([tend - tstart])
            maxtime = np.array([0.0])
            comm.Reduce(timeperproc,
                        maxtime,
                        op=MPI.MAX, root=0)
            if rank == 0:
                tlist[i, j] = maxtime[0]

            if os.path.exists(fname):
                os.remove(fname)

    if rank == 0:
        if outname is not None:
            np.savez(outname, tlist=tlist, mblist=mblist)


if __name__ == '__main__':
    # list of sizes in MB
    nlist = [1024 * 128 * int(k) for k in np.logspace(1, 10, 15, base=2.0)]
    ntests = 5
    comm = MPI.COMM_WORLD
    nproc = comm.Get_size()
    outname = f"bench6-{nproc}.npz"
    bench(nlist, ntests, outname)
