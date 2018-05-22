
from mpi4py import MPI
import numpy as np
import skimage.external.tifffile as tiff
import util

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

# TO DO: Currently, needs to be two bands only - 
# fix to deal with multiple bands in image collection.
years = [2001, 2012]
bands = ["lst"]
for band in bands:
    if rank == 0:
        SatData_object = util.create_from_files(years=years, \
            datasets=bands, include_regions=False)
        data = SatData_object.data
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
                if gathered_chunks[i]:
                # Talk to Cooper about concatenate vs. append.
                    diff_array = np.concatenate((diff_array, gathered_chunks[i]))
        final_diff_array = np.reshape(diff_array, \
            newshape=(data.shape[0], data.shape[1]))
        print(final_diff_array)
        print(final_diff_array.shape)



## DEV NOTES
## TEST DATA
    # data = np.array([[[1,2],[1,2],[1,2],[1,2]], \
    # [[1,3],[1,4],[1,5], [1,6]], [[1,1],[2,2],[3,3], [4,4]]])