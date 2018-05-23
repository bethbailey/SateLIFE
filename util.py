import numpy as np 
import skimage.external.tifffile as tiff 

RAW_FILE_STRUCTURES = {
	"landsat": ['landsat0', 'landsat1', 'landsat2'],
	"lst": ['lst0'],
	"night_lights": ['night_lights0'],
	"ndvi": ['ndvi0']
}

DECODE = {
 'Kasa-Vubu': 1,
 'Nsele': 2,
 'Kintambo': 3,
 'Ngaliema': 4,
 'Bumbu': 5,
 'Mont-Ngafula': 6,
 'Maluku': 7,
 'Masina': 8,
 'Lemba': 9,
 'Gombe': 10,
 'Selembao': 11,
 'Ngiri-Ngiri': 12,
 'Kimbanseke': 13,
 'Ngaba': 14,
 'Kinshasa': 15,
 'Bandalungwa': 16,
 'Makala': 17,
 'Kalamu': 18,
 'Matete': 19,
 'Ndjili': 20,
 'Lingwala': 21,
 'Kisenso': 22,
 'Barumbu': 23,
 'Limete': 24,

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
		'''

		self.data = data
		self.years = years 
		self.bands = bands
		self.boundaries = boundaries



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

		return SatData(new_data, self.years, self.bands)




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

	print("test")

