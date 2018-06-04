# AUTHOR: Cooper Nederhood, all code original
# CODE PURPOSE: 
'''
The image files are essentially just complex hyper-dimensional numpy tensors of different values.
Thus, when thinking about MPI implementation, partitioning a numpy tensor results in simply more 
numpy tensors displaying a similar structure. Thus, the SatData class design loads in the years and 
bands specified by the user and constructs parallel numpy arrays describing each respective band in
tensor. Methods on the class reflect operations that can be performed on a SatData tensor, including
basic properties like min, max, mean and more complex calculations like autocorrelations and Moran's I

Because of the self-similarity of the SatData class there are methods for partitioning the objects
in preparation for MPI-scatter-->gather operations. To facilitate gathering, there are functions which
take a list of SatData objects and aggregate them via a weighted combination of each SatData's observation
count

'''

import numpy as np 
import skimage.external.tifffile as tiff 

RAW_FILE_STRUCTURES = {
	"landsat": ['landsat0', 'landsat1', 'landsat2'],
	"lst": ['lst0'],
	"night_lights": ['night_lights0'],
	"ndvi": ['ndvi0']
}

DECODE = {
 'Congo-Kinshsa (outskirts)': 100,
 'Kasa-Vubu': 101,
 'Nsele': 102,
 'Kintambo': 103,
 'Ngaliema': 104,
 'Bumbu': 105,
 'Mont-Ngafula': 106,
 'Maluku': 107,
 'Masina': 108,
 'Lemba': 109,
 'Gombe': 110,
 'Selembao': 111,
 'Ngiri-Ngiri': 112,
 'Kimbanseke': 113,
 'Ngaba': 114,
 'Kinshasa': 115,
 'Bandalungwa': 116,
 'Makala': 117,
 'Kalamu': 118,
 'Matete': 119,
 'Ndjili': 120,
 'Lingwala': 121,
 'Kisenso': 122,
 'Barumbu': 123,
 'Limete': 124,

 'Congo-Brazzaville (outskirts)': 200,
 'Congo-Brazzaville (city)': 210,

 'River': 900,
 'River (island)': 999
 }

X_SIZE = 4900
Y_SIZE = 5036

class SatData():
	"""
	Class facilitates the flexible manipulation
	of satellite images data stored as a multidimensional
	numpy arry
	""" 

	def __init__(self, data, years, bands, boundaries=None):
		'''
		Constructor method initializes the 3 parallel numpy arrays

		Attributes:
			- self.data: (3D [x_pixels x y_pixels x band_count] np array) of sat data
			- self.years: (1D [band_count] np array) of year of sat data
			- self.bands: (1D [band_count] np array) of band of sat data
			- self.boundaries: (2D [x_pixels x y_pixels] np array) of geographic boundary codes
			- self.weight: (int) before reducing region, set the weight to be the x-y pixel cunt
		'''

		self.data = data
		self.years = years 
		self.bands = bands
		self.boundaries = boundaries
		self.weight = None



	def __str__(self):

		s = "Pixel dimensions: {}\n".format(self.data.shape[0:2])
		s += "Year range: {}-{}\n".format(self.years.min(), self.years.max())
		for i in range(len(self.bands)):
			s += "\tBand: {} | Year: {}\n".format(self.bands[i], self.years[i])

		return s


	def select_year(self, select_years):
		'''
		Returns a new SatData object with only the specified years
		'''

		if not isinstance(select_years, list):
			select_years = [select_years]
		year_bool = np.isin(self.years, select_years)

		return SatData(self.data[:, :, year_bool], self.years[year_bool], 
			self.bands[year_bool], self.boundaries)

	def select_band(self, select_bands):
		'''
		Returns a new SatData object with only the specified bands
		'''

		if not isinstance(select_bands, list):
			select_bands = [select_bands]
		band_bool = np.isin(self.bands, select_bands)

		return SatData(self.data[:,:, band_bool], self.years[band_bool], 
			self.bands[band_bool], self.boundaries)

	def reduce_by(self, operation, keepdims=True):
		'''
		Returns a new SatData instance which has reduced the x_pixel x y_pixel spatial
		dimension to a single point, applying the specified function

		Inputs:
			operation: (str) from options {mean, max, min, std}
			keepdims: (boolean) does rv maintain 3-D structure of SatData types? defaults to True
		'''

		self.weight = self.data.shape[0] * self.data.shape[1] 

		if operation == "mean":
			new_data = self.data.mean(axis=(0,1), keepdims=keepdims)

		elif operation == "max":
			new_data = self.data.max(axis=(0,1), keepdims=keepdims)

		elif operation == "min":
			new_data = self.data.min(axis=(0,1), keepdims=keepdims)

		elif operation == "std":
			new_data = self.data.std(axis=(0,1), keepdims=keepdims)
		else:
			print("Unsupported operation requested")
			return None

		rv = SatData(new_data, self.years, self.bands, self.boundaries)
		rv.weight = self.weight 

		return rv 


	def N_partitions(self, N):
		'''
		Partitions the SatData instance in N mutually exclusive and 
		exhaustive smaller SatData instances. Returns a list which contains
		the partitioned instances. Splits along x-y, maintains band dimension

		Inputs:
			- N (int): partitions to create
		'''

		data_partitions = np.array_split(self.data, N, axis=0)
		sat_partitions = []

		for sub_data in data_partitions:
			sub_sat = SatData(sub_data, self.years, self.bands, self.boundaries)

			sat_partitions.append(sub_sat)

		return sat_partitions

	def N_band_partitions(self, N):
		'''
		Partitions the SatData instance in N mutually exclusive and 
		exhaustive smaller SatData instances. Returns a list which contains
		the partitioned instances. SPLITS ALONG BAND DIMENSION

		Inputs:
			- N (int): partitions to create
		'''

		data_partitions = np.array_split(self.data, N, axis=2)
		sat_partitions = []

		for sub_data in data_partitions:
			sub_sat = SatData(sub_data, self.years, self.bands, self.boundaries)

			sat_partitions.append(sub_sat)

		return sat_partitions



	def auto_correlation(self, K, mean_df, std_df):
		'''
		Returns a new SatData instance of
		the K-th order autocorrelation. The calculation requires
		mean and std deviation of each year which is input as a parameter

		Inputs:
			- K (int): autocorrelation lag level
			- mean_df (pandas DF): dataframe for mean of each year
			- std_df (pandas DF): dataframe for std dev of each year

		Returns: 
			- SatData instance with autocorrelation
		'''

		#################################################################
		mean_vec = np.empty( self.data.shape[2] )
		std_vec = np.empty( self.data.shape[2] )

		for i in range(self.data.shape[2]):
			cur_year = self.years[i]
			cur_band = self.bands[i]

			mean_vec[i] = mean_df[mean_df.year==cur_year][cur_band].values[0]
			std_vec[i] = std_df[std_df.year==cur_year][cur_band].values[0]

		#################################################################
		
		normalized_data = (self.data - mean_vec) / std_vec
		corr_data = np.empty(self.data.shape)

		for i in range( self.data.shape[2] ):
			if i - K < 0:
				continue

			corr_data[:, :, i] = normalized_data[:, :, i] - normalized_data[:, :, i-K]

		temp_sat = SatData(corr_data, self.years, self.bands, self.boundaries)

		return temp_sat.reduce_by(operation='mean', keepdims=True) 

	def k_nearest_calc(self, K, function):
		'''
		Applies the specified function to the K-nearest neighbors
		over each of the bands in the SatData object. Returns a new SatData
		object

		Inputs:
			- K (int): consider the KxK neighborhood surrounding each pixel
			- function (function): function to apply to k-nearest neighborhoods

		Returns:
			- SatData instance with surface of the k-nearest calc for the bands
		'''

		cur_x = self.data.shape[0]
		cur_y = self.data.shape[1]
		band_count = self.data.shape[2]

		new_x = cur_x - K + 1
		new_y = cur_y - K + 1
		print("x dim changes from {} to {}".format(cur_x, new_x))
		print("y dim changes from {} to {}".format(cur_y, new_y))


		new_data = np.full( (new_x, new_y, band_count), -100000000 )

		for h in range(band_count):
			band_mean = np.mean( self.data[:,:,h] )
			print("Band mean: ", band_mean)
			for i in range(K, cur_x+1):
				print("Updating row i={}, from band h={}".format(i-K, h))
				for j in range(K, cur_y+1):

					cur_section = self.data[i-K:i, j-K:j, h].reshape( (K,K) )
					function_calc = function(cur_section, band_mean)

				
					new_data[i-K, j-K, h] = function_calc 

		rv_SatData = SatData(new_data, self.years, self.bands, self.boundaries)

		return rv_SatData



def calc_morans(np_array, global_mean):
	'''
	Given a square numpy array, calculates the Moran's I for
	the square, a measure of spatial autocorrelation.

	Inputs:
		- np_array (np array): represents a spatial region

	Returns:
		- moran (float): captures spatial dependence
	'''

	moran_num = 0
	moran_den = 0

	data = np_array.reshape(np_array.size)
	data = data - global_mean

	for i in range(data.shape[0]):
		moran_den += data[i]**2
		moran_num += np.sum(data*data[i])
		


	return moran_num, moran_den

def calc_avg_dev(np_array, global_mean):
	'''
	Given a square numpy array, calculates the average
	deviation from the mean in the neighborhood. Should identify
	regions that significantly differ from the general band average.

	Inputs:
		- np_array (np array): represents a spatial region

	Returns:
		- avg_dev (float): captures spatial deviation from average
	
	'''

	d = np_array.reshape(np_array.size) - global_mean
	avg_dev = np.mean(d)
	assert not np.isnan(avg_dev)

	return avg_dev 



def weighted_combination(SatData_collection):
	'''
	Given a collection of SatData instances which have been reduced
	to a single x-y dimension and the weight has been set, do a weighted
	combination to form a single series

	Inputs:
		- SatData_collection (list of SatData instances): to combine

	Returns:
		- weighted (SatData): weighted calcualtion of series
	'''

	new_data = np.zeros( SatData_collection[0].data.shape )
	weight_denom = 0

	for sat_data in SatData_collection:
		new_data = new_data + sat_data.data * sat_data.weight
		weight_denom = weight_denom + sat_data.weight 


	return SatData(new_data, SatData_collection[0].years, 
		SatData_collection[0].bands, SatData_collection[0].boundaries)




def create_from_files(years, datasets, include_regions=True):
	'''
	The raw files are stored by dataset-year. This function assembles a
	SatData object according to the specified years and datasets.

	Inputs:
		- years: (list) of desired data years
		- datasets: (list) of datasets from "landsat", "night_lights", "lst", "ndvi"
		- include_regions: (boolean) whether to include a regions indicator

	Returns: rv_SatData: SatData instance

	Ex. create_from_files([2007, 2008], ['landsat']) returns a SatData of 2007
		and 2008 Landsat imagery
	'''

	bands = 0
	for data_source in datasets:

		cur_band_count = len(RAW_FILE_STRUCTURES[data_source])
		bands += cur_band_count * len(years)

	rv_data = np.empty( (X_SIZE, Y_SIZE, bands) )
	rv_bands = ['']*bands
	rv_years = np.empty( bands)

	print("Putting data into final shape:", rv_data.shape)


	cur_band_height = 0

	for y in years:
		for d in datasets:
			file = {"landsat": "landsat", "night_lights": "DMSPNL", "lst":"LST", "ndvi":"ndvi"}
			ext = "data/{}/{}_{}.tif".format(d, file[d], str(y))
			print("Adding file ", ext)

			new_data = tiff.imread(ext)
			if new_data.ndim == 2:
				new_data = new_data.reshape( (new_data.shape[0], new_data.shape[1], 1)  )
			assert new_data.ndim == 3

			h = new_data.shape[2]

			new_bands = np.array( RAW_FILE_STRUCTURES[d] )
			new_years = np.full(len(new_bands), y)

			print("Loading data of shape:", new_data.shape)
			rv_data[:, :, cur_band_height:cur_band_height+h ] = new_data
			rv_bands[ cur_band_height:cur_band_height+h ] = new_bands
			rv_years[ cur_band_height:cur_band_height+h ] = new_years

			print(rv_data.shape)
			print(len(rv_bands))
			assert rv_data.shape[2] == len(rv_bands)

			cur_band_height += h

	rv_years = np.array(rv_years)
	if include_regions:
		rv_boundaries = tiff.imread('data/boundaries/final_boundaries.tif')
		rv_SatData = SatData(rv_data, rv_years, rv_bands, rv_boundaries)

	else:
		rv_SatData = SatData(rv_data, rv_years, rv_bands)

	return rv_SatData


def test():

	y = [2001, 2010]
	d = ['landsat', 'lst', 'ndvi', 'night_lights']

	s_d = create_from_files(y, d)
	print(s_d.years)
	print(s_d.bands)
	print(s_d)

if __name__ == '__main__':

	test = create_from_files([2010], ['lst'], False)
	test.data = test.data[:, 0:4900, :]

	mean = np.mean(test.data)
	m = test.k_nearest_calc(4880, calc_avg_dev)
