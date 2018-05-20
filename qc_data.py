import numpy as np 
import skimage.external.tifffile as tiff 
import os

SAT_FOLDERS = ['landsat', 'lst', 'night_lights']

def check_data(root, folders):
	'''
	Checks the subfolders listed in folders
	located at the root path. Prints the dimensions
	of the sat data there

	Inputs:
		-root (str) of root directory to search
	'''

	print("Reviewing folders at: ", root)
	for folder in folders:
		files = os.listdir(root+"/"+folder)
		print("\twithin subdirectory: ", folder)

		for file in files:
			img = tiff.imread(root+"/"+folder+"/"+file)

			print("\t\tfile {} has shape {}".format(file, img.shape))

