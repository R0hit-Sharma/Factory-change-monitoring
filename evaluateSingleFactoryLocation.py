import imageio
import csv
import numpy as np
from scipy import misc
from scipy import ndimage
from PIL import Image, ImageDraw

#---------------------------------------
#Varbiles
district = 'Pune'
key = 191#3
fileExtn = '.png'
area = '2Kms'
xMin = 73.33284759521484 
xMax = 75.16710662841797 
yMin = 17.891420364379883
yMax = 19.394990921020508
#---------------------------------------
folderName = district.lower()+'District'
year = ['2016', '2019']

'''
Delhi NCR
76.84251403808594
77.34764862060547
28.403051376342773
28.879323959350586

Pune
73.33284759521484
75.16710662841797
17.891420364379883
19.394990921020508
'''


def calcUrbanization(fileName, inX1, inY1, inX2, inY2, yr, stateImage, xd, yd):
	#inY1 = 28.6207843
	#inX1 = 77.1072188
	#inY2 = 28.7207843
	#inX2 = 77.2072188
	pixelX = (inX1 - xMin)/xd
	rangeX = (inX2 - inX1)/xd
	pixelY = stateImage.shape[0] - (inY1 - yMin)/yd
	rangeY = (inY2 - inY1)/yd
	print('Location Dim:'+'x:'+str(pixelX)+' xr:'+str(pixelX+rangeX)+' y:'+str(pixelY)+' yr:'+str(pixelY+rangeY))

	subImage = stateImage[int(pixelY):int(pixelY+rangeY), int(pixelX):int(pixelX+rangeX)]
	colorArray, countArray = np.unique(subImage, return_counts=True)
	#print(str(list(colorArray).index(key)))
	try:
		print(str(float(countArray[list(colorArray).index(key)])*100/float(sum(list(countArray)))))
	except ValueError:
		print(str(colorArray)+', '+ str(countArray))	
	
	imageio.imsave('./'+folderName+'/extras/'+fileName+fileExtn, subImage)
	stateImage1 = Image.open('./'+folderName+'/extras/'+area+'_'+yr+'_marked'+fileExtn)
	img_draw = ImageDraw.Draw(stateImage1)
	img_draw.rectangle((int(pixelX),int(pixelY),int(pixelX+rangeX),int(pixelY+rangeY)), outline = 'red', width = 5)
	stateImage1.save('./'+folderName+'/extras/'+area+'_'+yr+'_marked'+fileExtn)

if __name__== "__main__":
	for yr in year:
		print(str(yr))
		stateImage1 = Image.open('./'+folderName+'/'+district+'_prediction_'+yr+fileExtn)
		stateImage1.save('./'+folderName+'/extras/'+area+'_'+yr+'_marked'+fileExtn)
		stateImage = imageio.imread('./'+folderName+'/'+district+'_prediction_'+yr+fileExtn)
		dims = stateImage.shape
		xs = dims[1]
		ys = dims[0]
		print('Image Dim:'+str(xs)+'x'+str(ys))
		xd = (xMax-xMin)/xs
		yd = (yMax-yMin)/ys
		calcUrbanization('MAHINDRA HOMES PRIVATE LIMITED_2Kms', 73.8734077, 18.552817791,73.8934077, 18.570835809, yr, stateImage, xd, yd)
		print('----------------------------')
