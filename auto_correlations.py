# To run this on google could servers, you will have to add the below commands.
# sudo pip install scikit-image
# sudo pip3 install scikit-image

from mpi4py import MPI
import numpy as np
import skimage.external.tifffile as tiff
import util

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()



# print("Rank is:", rank)
# print("Size is:", size)
# print()

if rank == 0:
	data = util.create_from_files([2011, 2010, 2009], ['lst'], include_regions=False)
	chunks = data.N_partitions(size)

else:
	chunks = None

chunk = comm.scatter(chunks, root=0)
print("Rank {} has the following SatData instance:".format(rank))
print(chunk)

results = chunk.auto_correlation(K=1, mean_vec="pass", std_vec="pass")
gathered_results = comm.gather(results, root=0)

if rank == 0:
	print("Rank {} has gathered_results:".format(rank))

	for r in gathered_results:
		print(r)

	weighted_result = util.weighted_combination(gathered_results)
	print("FINAL RESULT IS:")
	print(weighted_result)

else:
	assert gathered_results is None

	



