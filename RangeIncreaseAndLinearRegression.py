#python 2
import findRuralUrbanExtent
import generateRectangularCoords
import imageio
import csv
import copy
import imageio
import numpy as np
import pandas as pd
from pylab import *
from PIL import Image
from scipy import misc
from scipy import ndimage
from scipy.misc import imsave
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
district = 'Tirunelveli'
folderName = district.lower()+'District'
fileExtn = '.tif'
districts = ['Tirunelveli']
for district in districts:
	print (district)
	year = [2016,2019]

	# Perform Smoothing

	matSmooth = []	#matrix after smoothning (convolving and filtering)
	matOriginal = []
	for i in range(len(year)):
		print(i)
		dataset = imageio.imread('./'+folderName+'/'+district+'_prediction_temporal_'+str(year[i])+fileExtn)
		#print('original dataset\n',dataset)
		data = (dataset)/240 # reduce image to 0 for outer area and built up and leaving 2 as 1 for non builtup (modulus2 isn't used)
		print(np.unique(dataset))
		print(np.unique(data))
		#print('data=dataset/2\n',data)

		# Convolution without gaussian, high weight to original pixel and low to other
	# 	k = np.array([[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,48,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1]])
	# 	smooth = ndimage.convolve(data, k, mode='constant', cval=0.0) # [0,1,2,3,4,5,6,7,8,9]
	# 	imsave('/content/gdrive/My Drive/DiseaseSurveillance/images/original/' + district + '_smooth_weighted_removed_16_48N_' + str(i) + '.png', smooth*(255/96))

		
		# Convolution with gaussian filter
		k = np.array([[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]])	# 5*5 matrix
		smooth = ndimage.convolve(data, k, mode='constant', cval=0.0)
		smooth = ndimage.gaussian_filter(smooth, sigma=0.2,truncate=11.0,output=float) 	#standard deviation of gaussian kernel is referred as sigma
		# smooth=[[int(smooth[i][j]*10000000000000000000) for j in range(len(smooth[i]))] for i in range(len(smooth))]
		# imsave('/content/gdrive/My Drive/DiseaseSurveillance/images/original/' + district + '_smooth_conv_gaus_removed_16_24N_' + str(i) + '.png', smooth*(255/25))	
		print (len(np.unique(smooth))) 

		original = dataset.flatten()	#convert 2d matrices to 1d array
		smoothed = smooth.flatten()
		assert(len(original) == len(smoothed))
		smooth_temp = [smoothed[i] for i in range(len(smoothed)) if original[i] > 0]	# remove things outside district in original
		original_temp = [2-i for i in original if i > 0]	#remove things outside district in smoothed
		assert(len(smooth_temp) == len(original_temp))

		matOriginal.append(original_temp)	#appending all 4 year arrays one after another
		matSmooth.append(smooth_temp)

	print("\noverall\n")
	#print (np.unique(matSmooth))
	matOriginal = np.array(matOriginal, copy=False).T	#doing transpose i.e., matrix is now 4*number of pixels in a pic
	matSmooth = np.array(matSmooth, copy=False).T
	#print (matOriginal.shape)
	#print (matSmooth.shape)

	#matorignal never used again


	# Perform Linear Regression (exclude boundary points as well)

	x1 = np.reshape(range(len(year)), (-1,1))	#a matrix of type [[1],[2],[3],...,[len(year)]],-1 refers to unspecified that is to the no. of rows here

	dataset = imageio.imread('./'+folderName+'/'+district+'_prediction_temporal_'+str(year[i])+fileExtn)	#dataset variable is reloaded
	dataset=dataset/120
	dims = dataset.shape
	print(dims)
	slope = []	#these things are found for every pixel using 4 different years 
	intercept = []
	cost_array = []

	mask = np.sign(dataset)	#-1 0 or 1 according to the sign of numbers thus reducing non built up to 1 in our dataset

	k = np.array([[1,1,1],[1,1,1],[1,1,1]])
	mask1 = ndimage.convolve(mask, k, mode='constant', cval=0.0)	#values at border are less than 9, otherwise inside it is 9

	i=0	#refers to the pixel we are working upon in the following loop

	for j in range(dims[0]):
		for k in range(dims[1]):
			if (mask[j][k]):	#comes inside gurgaon leaving outside area bcz matsmooth has internal pixels only
				if (mask1[j][k] == 9):	#ignoring border part
					lm = LinearRegression()
					reg = lm.fit(x1, matSmooth[i])	#we are predicting value of pixel for a given year and then doing best fit of linear regression on it so x1 (year) is our input variable for linear regression
					cost = np.mean((matSmooth[i] - lm.predict(x1))**2)
					cost_array.append(cost)
					slope.append(round(reg.coef_[0], 4))	#coef.shape is (1,1)
					intercept.append(round(reg.intercept_, 4))	#intercept.shape is (1)
				i += 1

	cost_array = np.array(cost_array)
	#print (cost_array.shape)

	# cost_array = (cost_array-np.min(cost_array))/np.ptp(cost_array)
	# Save the cost array
	np.savetxt('./'+folderName+'/_conv_gaus_removed_16_24N_cost_array.txt', cost_array*1000, fmt='%d')	#multiplied be thousand because very small values, otherwise direct storing will convert values to 0

	# np.savetxt('/content/gdrive/My Drive/DiseaseSurveillance/' + district + '_weighted_removed_16_48N_cost_array.txt', cost_array*1000, fmt='%d')

	unique_elements, counts_elements = np.unique(cost_array, return_counts=True)
	total_count_elements = (float) (counts_elements.sum())
	counts_elements = counts_elements/total_count_elements
	cdf = np.cumsum(counts_elements)
	plt.plot(unique_elements,cdf,label = 'data')
	savefig('./'+folderName+'/_conv_gaus_removed_16_24N_cdf')
	plt.clf()
