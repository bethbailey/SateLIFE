
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
bands = ["night_lights", "lst", "ndvi", "landsat"]
for band in bands:
    if rank == 0:
        SatData_object = util.create_from_files(years=years, datasets=[band], \
            include_regions=False)
        if band == "landsat":
            data1 = SatData_object.data[:, [0,3]]
            data2 = SatData_object.data[:, [1,4]]
            data3 = SatData_object.data[:, [2,5]]
            chunks1 = np.array_split(data1, size)
            chunks2 = np.array_split(data2, size)
            chunks3 = np.array_split(data3, size)          
        else:
            data = SatData_object.data
            chunks = np.array_split(data, size)
    else:
        if band == "landsat":
            chunks1 = None
            chunks2 = None
            chunks3 = None
        else:
            chunks = None

    if band == "landsat":
        chunk1 = comm.scatter(chunks1, root=0)
        chunk2 = comm.scatter(chunks2, root=0)
        chunk3 = comm.scatter(chunks3, root=0)
    else:
        chunk = comm.scatter(chunks, root=0)

    if band == "landsat":
        results1 = []
        results2 = []
        results3 = []
        for x1 in chunk1:
            diff1 = np.diff(x1)
            results1.append(diff1)
        for x2 in chunk2:
            diff2 = np.diff(x2)
            results2.append(diff2)
        for x3 in chunk3:
            diff3 = np.diff(x3)
            results3.append(diff3)
    else:
        results = []
        for x in chunk:
            diff = np.diff(x)
            results.append(diff)

    if band == "landsat":
        gathered_chunks1 = comm.gather(results1, root=0)
        gathered_chunks2 = comm.gather(results2, root=0)
        gathered_chunks3 = comm.gather(results3, root=0)
    else:
        gathered_chunks = comm.gather(results, root=0)

    if rank == 0:
        if band == "landsat":
            # Landsat 0
            diff_array1 = gathered_chunks1[0]
            for i1 in range(len(gathered_chunks1)):
                if i1 != 0:
                    if gathered_chunks1[i]:
                        diff_array1 = np.concatenate((diff_array1, gathered_chunks1[i]))
            final_diff_array1 = np.reshape(diff_array1, \
                newshape=(data1.shape[0], data1.shape[1]))
            df1 = pd.DataFrame(final_diff_array1)
            df1.to_csv(path_or_buf="diff_years/landsat0{}{}.csv".format(years[0], years[1]))
            # Landsat 1
            diff_array2 = gathered_chunks2[0]
            for i2 in range(len(gathered_chunks2)):
                if i2 != 0:
                    if gathered_chunks2[i]:
                        diff_array2 = np.concatenate((diff_array2, gathered_chunks2[i]))
            final_diff_array2 = np.reshape(diff_array2, \
                newshape=(data2.shape[0], data2.shape[1]))
            df2 = pd.DataFrame(final_diff_array2)
            df2.to_csv(path_or_buf="diff_years/landsat1{}{}.csv".format(years[0], years[1]))
            # Landsat 2
            diff_array3 = gathered_chunks3[0]
            for i3 in range(len(gathered_chunks3)):
                if i3 != 0:
                    if gathered_chunks3[i]:
                        diff_array3 = np.concatenate((diff_array3, gathered_chunks3[i]))
            final_diff_array3 = np.reshape(diff_array3, \
                newshape=(data3.shape[0], data3.shape[1]))
            df3 = pd.DataFrame(final_diff_array3)
            df3.to_csv(path_or_buf="diff_years/landsat2{}{}.csv".format(years[0], years[1]))
        else:
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
        if band == "landsat":
            assert gathered_chunks1 is None
            assert gathered_chunks2 is None
            assert gathered_chunks3 is None
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