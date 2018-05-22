from mpi4py import MPI
import numpy as np
import skimage.external.tifffile as tiff
import util

## LOOK AT CORRELATION
## By neighborhood, by region

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

# Should we do a for loop over the years for this?
if rank == 0:
    boundaries = np.array([[210,210,112],[999,999,112],[900,900,900]])
    # print(boundaries)
    data = np.array([[[1,2,3,4],[5,6,7,8],[9,10,11,12]], \
        [[2,3,4,5],[6,7,8,9],[10,11,12,13]], [[3,4,5,6],[7,8,9,10],[11,12,13,14]]])
    # array_shape = np.shape(data)
    # bands = array_shape[2]
    unique, counts = np.unique(boundaries, return_counts=True)
    neighborhood_dict = {}
    for i in range(len(unique)):
        neighborhood_dict[unique[i]] = np.array([])
    for index, line in enumerate(data):
        for index2, line2 in enumerate(line):
            neighborhood_dict[boundaries[index][index2]] = \
                np.append(neighborhood_dict[boundaries[index][index2]], [[line2]])
    print(neighborhood_dict)
    chunks = neighborhood_dict.values()
    print(chunks)
# else:
#     chunks = None

# chunk = comm.scatter(chunks, root=0)

# results = []
# for x in chunk:
#     s = np.sum(x, axis=(0))
#     results.append(s)

# gathered_chunks = comm.gather(results, root=0)

# if rank == 0:

