# To run this on google could servers, you will have to add the below commands.
# sudo pip install scikit-image
# sudo pip3 install scikit-image

from mpi4py import MPI
import numpy as np
import skimage.external.tifffile as tiff
import util
import pandas as pd

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

# Create list of years to iterate over.
years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, \
    2012]
mean_df = pd.DataFrame(index=years, columns=["night_lights", "lst", "ndvi", "landsat0", \
    "landsat1", "landsat2"])
min_df = pd.DataFrame(index=years, columns=["night_lights", "lst", "ndvi", "landsat0", \
    "landsat1", "landsat2"])
max_df = pd.DataFrame(index=years, columns=["night_lights", "lst", "ndvi", "landsat0", \
    "landsat1", "landsat2"])
std_df = pd.DataFrame(index=years, columns=["night_lights", "lst", "ndvi", "landsat0", \
    "landsat1", "landsat2"])
 
# For each year, use MPI to find summary statistics.
# TO DO: ADD MEDIAN.
for year in years:
    if rank == 0:
        SatData_object = util.create_from_files(years=[year], \
            datasets=["night_lights", "lst", "ndvi", "landsat"], \
            include_regions=False)
        data = SatData_object.data
        array_shape = np.shape(data)
        count = array_shape[0] * array_shape[1]
        bands = array_shape[2]
        chunks = np.array_split(data, size)
    else:
        chunks = None

    chunk = comm.scatter(chunks, root=0)

    results = []

    for x in chunk:
        sums = np.sum(x, axis=(0))
        maxi = np.max(x, axis=(0))
        mini = np.min(x, axis=(0))
        results.append((sums, maxi, mini))

    gathered_chunks = comm.gather(results, root=0)

    if rank == 0:
        # Find mean, max, and min.
        overall_zeros = np.zeros(shape=(bands))
        cur_max = np.zeros(shape=(bands))
        # Find first array of mins to compare future arrays to.
        cur_min = gathered_chunks[0][0][2]
        print("gathered_chunks")
        for chunk1 in gathered_chunks:
            for data in chunk1:
                overall_zeros += data[0]
                np.maximum(data[1], cur_max, out=cur_max)
                np.minimum(data[2], cur_min, out=cur_min)
        avg = overall_zeros / count
        mean_df.loc[year] = avg
        max_df.loc[year] = cur_max
        min_df.loc[year] = cur_min
    else:
        assert gathered_chunks is None

    if rank == 0:
        avg = avg
    else:
        avg = None

    avg = comm.bcast(avg, root=0)

    results_2 = []
    for x in chunk:
        res = x - avg
        res = np.square(res)
        res = np.sum(res, axis=0)
        results_2.append(res)

    gathered_chunks2 = comm.gather(results_2, root=0)

    if rank == 0:
        # Find std.
        sums_diffs_sq = np.zeros(shape=(bands))
        for chunk2 in gathered_chunks2:
            for data2 in chunk2:
                sums_diffs_sq += data2
        std = np.sqrt(sums_diffs_sq / count)
        std_df.loc[year] = std
    else:
        assert gathered_chunks2 is None

# Save dataframes in csv.
mean_df.to_csv(path_or_buf="bands_collapse_data/means_by_year.csv")
max_df.to_csv(path_or_buf="bands_collapse_data/maxs_by_year.csv")
min_df.to_csv(path_or_buf="bands_collapse_data/mins_by_year.csv")
std_df.to_csv(path_or_buf="bands_collapse_data/stds_by_year.csv")



## NOTES FOR DEV
    # Test data:
    # data = np.array([[[1,2,3,4],[2,2,3,4],[1,2,3,4]], [[0,2,3,4],[1,2,3,4],[1,2,3,4]]])
    # data = np.array([[[3,2,3,4],[1,5,3,4],[1,6,10,4]], [[1,2,3,12],[1,2,3,11],[1,2,3,4]]])
    # data = tiff.imread('year2000.tif')