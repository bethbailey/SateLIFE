# To run this on google could servers, you will have to add the below commands.
# sudo pip install scikit-image
# sudo pip3 install scikit-image

from mpi4py import MPI
import numpy as np
import skimage.external.tifffile as tiff

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

# Should we do a for loop over the years for this?
if rank == 0:
    # data = np.array([[[1,2,3,4],[1,2,3,4],[1,2,3,4]], [[1,2,3,4],[1,2,3,5],[1,2,3,4]]])
    data = tiff.imread('year2000.tif')
    # Need to figure out methods for splitting chunks by neighborhood.
    array_shape = np.shape(data)
    print(data[0][0])
    count = array_shape[0] * array_shape[1]
    bands = array_shape[2]
    chunks = np.array_split(data, size)
else:
    chunks = None

chunk = comm.scatter(chunks, root=0)

results = []
# results2 = [] # For another calculation.
for x in chunk:
    s = np.sum(x, axis=(0))
    results.append(s)

gathered_chunks = comm.gather(results, root=0)

if rank == 0:
    overall_zeros = np.zeros(shape=(1, bands))
    overall_counts = np.ones(shape=(1, bands)) * count
    for sums in gathered_chunks:
        for subsum in sums:
            overall_zeros += subsum
    m = overall_zeros / overall_counts
    print(m)

# How to find standard deviation without mean? Or scatter/gather again?