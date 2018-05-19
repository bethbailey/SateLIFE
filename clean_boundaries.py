import numpy as np 
import skimage.external.tifffile as tiff 
import pandas as pd 

# hardcoded path is temporary
PATH = "/home/cooper/Documents/SateLIFE/data/"


def create_clean_tiff(output_file):
	'''
	There are 3 tiff files output from google earth engine.
	Combine to create 1 file with all necessary geographic
	distinctions

	Cleaning: there is slight erroneous overlap between 
			Kinshasa city borders and the water designation.
			Replace as water.

	'''

	country_file = "country_boundaries.tif"
	kinshasa_file = "boundaries1.tif"
	brazzaville_file = "details_boundaries.tif"

	country_level = tiff.imread(PATH+"boundaries/"+country_file)
	kinshasa_level = tiff.imread(PATH+"boundaries/"+kinshasa_file)
	kinshasa_level[ np.isnan(kinshasa_level) ] = 0
	brazzaville_level = tiff.imread(PATH+"boundaries/"+brazzaville_file)

	assert np.all(~np.isnan(country_level))
	assert np.all(~np.isnan(kinshasa_level))

	# combine country and kinshasa details
	combine1 = country_level + kinshasa_level
	b = combine1 > 900 
	combine1[ b ] = 900

	combine1 = combine1 + brazzaville_level

	# do checks
	assert np.all(~np.isnan(combine1))
	assert np.all( np.isfinite(combine1))

	tiff.imsave(output_file, combine1)




