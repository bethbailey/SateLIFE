# AUTHOR: Bethany Bailey
# All code original.

from mpi4py import MPI
import numpy as np
import skimage.external.tifffile as tiff
import util
import pandas as pd

'''
This script takes two years and finds the differences of each pixel in the 
region for each band.
'''

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

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
        # Find the difference between the two years.
        diff = np.diff(x)
        results.append(diff)

    gathered_chunks = comm.gather(results, root=0)

    if rank == 0:
        # Initialize the difference array with the first chunks of differences
        diff_array = gathered_chunks[0]
        for i in range(len(gathered_chunks)):
            # If it is not the first chunk of differences
            if i != 0:
                # And if it is not an empty array
                if gathered_chunks[i]:
                    # Add it to the difference array.
                    diff_array = np.concatenate((diff_array, gathered_chunks[i]))
        # Reshape into shape of geography.
        final_diff_array = np.reshape(diff_array, \
            newshape=(data.shape[0], data.shape[1]))
        # Make it a df and save it to csv.
        df = pd.DataFrame(final_diff_array)
        df.to_csv(path_or_buf="diff_years/{}{}{}.csv".format(band, years[0], years[1]))
    else:
        assert gathered_chunks is None
