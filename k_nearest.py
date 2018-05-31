# To run this on google could servers, you will have to add the below commands.
# sudo pip install scikit-image
# sudo pip3 install scikit-image

from mpi4py import MPI
import numpy as np
import skimage.external.tifffile as tiff
import util
import matplotlib.pyplot as plt 
import os 
import pandas as pd 

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

#DATA = ['ndvi', 'lst', 'night_lights']
#YEARS = list(range(2010, 2013))

DATA = ['ndvi']
YEARS = [2012, 2013]
k = 400

print("Rank is:", rank)
print("Size is:", size)
print()

root = "k_nearest/" 

if rank == 0:

	data = util.create_from_files(YEARS, DATA, include_regions=False)

	chunks = data.N_band_partitions(size)

else:
	chunks = None

chunk = comm.scatter(chunks, root=0)
print("Rank {} has the following SatData instance:".format(rank))
print(chunk)

results = chunk.k_nearest_calc(k, util.calc_avg_dev)
gathered_results = comm.gather(results, root=0)

if rank == 0:
	print("Rank {} has gathered_results:".format(rank))

	for r in gathered_results:
		print(r)

	for sat_data in gathered_results:
		band_count = sat_data.data.shape[2]

		for band in range(band_count):
			plt.imshow(sat_data.data[:,:,band])

			cur_year = sat_data.years[band]
			cur_data = sat_data.bands[band]

			plt.savefig('k_nearest/knn{} - {} - {}.png'.format(k, cur_data, cur_year))

else:
	assert gathered_results is None

	










