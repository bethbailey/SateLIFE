from mpi4py import MPI
import numpy as np
from PIL import Image
import skimage.external.tifffile as tiff

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

if rank == 0:
	data = tiff.imread('year2000.tif')
	# Methods for splitting chunks by neighborhood
    chunks = np.array_split(data, size)
else:
    chunks = None

chunk = comm.Scatter(chunks, root=0)

results = []
for x in chunk:
	results.append((np.sum(x), shape(x))) # replace shape

gathered_chunks = comm.gather(results, root=0)

overall_sum = 0
overall_count = 0

for i in gathered_chunks:
	overall_sum += i[0]
	overall_count += i[1] # replace with count
	mean = overall_sum / overall_count

