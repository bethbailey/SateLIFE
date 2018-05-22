
from mpi4py import MPI
import numpy as np
import skimage.external.tifffile as tiff
# import util.py

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

# Needs to be two bands only.
# Do a for loop over the bands we want?
if rank == 0:
    data = np.array([[[1,2],[1,2],[1,2]], [[1,3],[1,4],[1,5]], [[1,1],[2,2],[3,3]]])
    chunks = np.array_split(data, size)
else:
    chunks = None

chunk = comm.scatter(chunks, root=0)

results = []
for x in chunk:
    diff = np.diff(x)
    results.append(diff)

gathered_chunks = comm.gather(results, root=0)

if rank == 0:
    diff_array = gathered_chunks[0]
    for i in range(len(gathered_chunks)):
        if i != 0:
            # Talk to Cooper about concatenate vs. append.
            diff_array = np.concatenate((diff_array, gathered_chunks[i]))
    print(diff_array)