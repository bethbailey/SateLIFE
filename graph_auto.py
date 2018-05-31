import matplotlib.pyplot as plt 
import pandas as pd 

bands = ['lst', 'ndvi', 'night_lights']
k_s = [1, 2, 3]

color_tt = {1:'r', 2:'b', 3:'g'}

for b in bands:
	plt.clf()
	for k in k_s:
		df = pd.read_csv('autocorrelation/{} - {}.csv'.format(b, k))

		df = df[df.autocorrelation != 0]

		c = color_tt[k]

		plt.plot(df.Year, df.autocorrelation, color = c, label = '{} order'.format(k))

	plt.xlabel('Year')
	plt.ylabel('Autocorrelation across band')
	plt.title('Autocorrelation by year and order: {}'.format(b))
	plt.legend()
	plt.savefig('autocorrelation {}.jpg'.format(b))