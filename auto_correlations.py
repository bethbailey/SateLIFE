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
#YEARS = list(range(2010, 2014))
#kth_order = [1, 2, 3]

DATA = ['ndvi', 'lst', 'night_lights']
YEARS = list(range(2009, 2013))
kth_order = [1]

print("Rank is:", rank)
print("Size is:", size)
print()

# if not os.path.exists("autocorrelation/"):
# 	os.makedirs("autocorrelation/")

root = "autocorrelation/" 

for cur_data in DATA:
	for k in kth_order:
		if rank == 0:
			data = util.create_from_files(YEARS, [cur_data], include_regions=False)
			chunks = data.N_partitions(size)

		else:
			chunks = None

		chunk = comm.scatter(chunks, root=0)
		print("Rank {} has the following SatData instance:".format(rank))
		print(chunk)

		results = chunk.auto_correlation(K=k, mean_vec="pass", std_vec="pass")
		gathered_results = comm.gather(results, root=0)

		if rank == 0:
			print("Rank {} has gathered_results:".format(rank))

			for r in gathered_results:
				print(r)

			weighted_result = util.weighted_combination(gathered_results)
			print("FINAL RESULT IS:")
			print(weighted_result)

			y = weighted_result.data.reshape(weighted_result.data.size)

			plt.plot(weighted_result.years.astype('int'), y)
			plt.title('{} autocorrelations: k={}'.format(cur_data, k))
			plt.xlabel('Year')
			plt.ylabel('Autcorrelation')
			plt.savefig('{}{} - {}.png'.format(root, cur_data, k))

			df = pd.DataFrame({"Year": weighted_result.years.astype('int'), "autocorrelation": y })
			df.to_csv('{}{} - {}.csv'.format(root, cur_data, k))

		else:
			assert gathered_results is None

	


