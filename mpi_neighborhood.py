from mpi4py import MPI
import numpy as np
import skimage.external.tifffile as tiff
import util
import pandas as pd
import pickle

## LOOK AT CORRELATION
## By neighborhood, by region

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, \
   2012]
for year in years:
    if rank == 0:
        SatData_object = util.create_from_files(years=[year], \
            datasets=["night_lights", "lst", "ndvi", "landsat"], \
            include_regions=True)
        data = SatData_object.data
        boundaries = SatData_object.boundaries 
        data_chunks = np.array_split(data, size)
        boundary_chunks = np.array_split(boundaries, size)
    else:
        data_chunks = None
        boundary_chunks = None

    data_chunk = comm.scatter(data_chunks, root=0)
    boundary_chunk = comm.scatter(boundary_chunks, root=0)

    sum_results = {}
    count_results = {}
    max_results = {}
    min_results = {}
    for x in range(len(data_chunk)):
        for i in range(len(data_chunk[x])):
            if str(boundary_chunk[x][i]) in sum_results.keys():
                cur_max = max_results[str(boundary_chunk[x][i])]
                cur_min = min_results[str(boundary_chunk[x][i])]
                max_results[str(boundary_chunk[x][i])] = \
                    np.maximum(cur_max, data_chunk[x][i])
                min_results[str(boundary_chunk[x][i])] = \
                    np.minimum(cur_min, data_chunk[x][i])
                sum_results[str(boundary_chunk[x][i])] += data_chunk[x][i]
                count_results[str(boundary_chunk[x][i])] += 1
            else:
                value = data_chunk[x][i]
                max_results[str(boundary_chunk[x][i])] = value
                min_results[str(boundary_chunk[x][i])] = value
                sum_results[str(boundary_chunk[x][i])] = value
                count_results[str(boundary_chunk[x][i])] = 1

    gathered_sum_chunks = comm.gather(sum_results, root=0)
    gathered_count_chunks = comm.gather(count_results, root=0)
    gathered_max_chunks = comm.gather(max_results, root=0)
    gathered_min_chunks = comm.gather(min_results, root=0)

    if rank == 0:
        # Find mean.
        sum_dict = gathered_sum_chunks[0]
        for res in gathered_sum_chunks[1:]:
            for key, value in res.items():
                if key in sum_dict.keys():
                    sum_dict[key] += value
                else:
                    sum_dict[key] = value
        count_dict = gathered_count_chunks[0]
        for count_res in gathered_count_chunks[1:]:
            for count_key, count_value in count_res.items():
                if count_key in count_dict.keys():
                    count_dict[count_key] += count_value
                else:
                    count_dict[count_key] = count_value
        final_mean_dict = {}    
        for final_sum_key, final_sum_value in sum_dict.items():
            final_mean_dict[final_sum_key] = final_sum_value / count_dict[final_sum_key]

        # Find max.
        max_dict = gathered_max_chunks[0]
        for res2 in gathered_max_chunks[1:]:
            for key, value in res2.items():
                if key in max_dict.keys():
                    max_dict[key] = np.maximum(max_dict[key], value)
                else:
                    max_dict[key] = value

        # Find min
        min_dict = gathered_min_chunks[0]
        for res3 in gathered_min_chunks[1:]:
            for key, value in res3.items():
                if key in min_dict.keys():
                    min_dict[key] = np.minimum(min_dict[key], value)
                else:
                    min_dict[key] = value

        with open('neighborhood_data/means_by_neighborhood{}.cp'.format(year), 'wb') as fp:
            pickle.dump(final_mean_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)
        with open('neighborhood_data/maxs_by_neighborhood{}.cp'.format(year), 'wb') as fp:
            pickle.dump(max_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)
        with open('neighborhood_data/mins_by_neighborhood{}.cp'.format(year), 'wb') as fp:
            pickle.dump(min_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        assert gathered_sum_chunks is None
        assert gathered_count_chunks is None
        assert gathered_max_chunks is None
        assert gathered_min_chunks is None

    # Find std.
    if rank == 0:
        final_mean_dict = final_mean_dict
        data_chunks2 = np.array_split(data, size)
        boundary_chunks2 = np.array_split(boundaries, size)

    else:
        final_mean_dict = None
        data_chunks2 = None
        boundary_chunks2 = None

    means_dict = comm.bcast(final_mean_dict, root=0)
    data_chunk2 = comm.scatter(data_chunks2, root=0)
    boundary_chunk2 = comm.scatter(boundary_chunks2, root=0)

    results_diff = {}
    for x in range(len(data_chunk2)):
        for i in range(len(data_chunk2[x])):
            if str(boundary_chunk2[x][i]) in results_diff.keys():
                results_diff[str(boundary_chunk2[x][i])] += \
                    np.square(data_chunk2[x][i] - means_dict[str(boundary_chunk2[x][i])])
            else:
                value = data_chunk2[x][i]
                results_diff[str(boundary_chunk2[x][i])] = \
                    np.square(data_chunk2[x][i] - means_dict[str(boundary_chunk2[x][i])])

    gathered_std_chunks = comm.gather(results_diff, root=0)

    if rank == 0:
        # Find std.
        diffs_dict = gathered_std_chunks[0]
        for res in gathered_std_chunks[1:]:
            for key, value in res.items():
                if key in diffs_dict.keys():
                    diffs_dict[key] += value
                else:
                    diffs_dict[key] = value
        final_std_dict = {}    
        for final_diff_key, final_diff_value in diffs_dict.items():
            final_std_dict[final_diff_key] = \
                np.sqrt(final_diff_value / count_dict[final_diff_key])

        with open('neighborhood_data/stds_by_neighborhood{}.cp'.format(year), 'wb') as fp:
            pickle.dump(final_std_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        assert gathered_std_chunks is None


### DEV NOTES ####
# # TEST DATA
    # boundaries = np.array([[210,210,112], [999,999,112], [900,900,900],\
    #  [3,7,11], [900,900,900]])
    # data = np.array([[[1,2,3,4],[5,6,7,8],[9,10,11,12]], \
    #     [[2,3,4,5],[6,7,8,9],[10,11,12,13]], [[3,4,5,6],[7,8,9,10],[11,12,13,14]], \
    #     [[3,4,5,6],[7,8,9,10],[11,12,13,14]], [[3,4,5,6],[7,8,9,10],[11,12,13,14]]])