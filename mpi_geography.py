
from mpi4py import MPI
import numpy as np
import skimage.external.tifffile as tiff
import util
import pandas as pd

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

# TO DO: Currently, needs to be two bands only - 
# fix to deal with multiple bands in image collection.
years = [2001, 2012]
bands = ["night_lights", "lst", "ndvi"]
for band in bands:
    if rank == 0:
        SatData_object = util.create_from_files(years=years, datasets=[band], \
            include_regions=False)
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
                    diff_array = np.concatenate((diff_array, gathered_chunks[i]))
        final_diff_array = np.reshape(diff_array, \
            newshape=(data.shape[0], data.shape[1]))
        df = pd.DataFrame(final_diff_array)
        df.to_csv(path_or_buf="diff_years/{}{}{}.csv".format(band, years[0], years[1]))
    else:
        assert gathered_chunks is None


    ## DEV NOTES
    ## TEST DATA
        # data = np.array([[[1,2],[1,2],[1,2],[1,2]], \
        # [[1,3],[1,4],[1,5], [1,6]], [[1,1],[2,2],[3,3], [4,4]]])

                # l, w = np.shape(x)
        # for row in range(int(l)):
        #     start_index = 0
        #     for i in range(int(w/2)):
        #         second_index = int(start_index + w/2)
        #         print(x[row][second_index] - x[row][start_index])
        #         start_index+=1