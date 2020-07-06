import findRuralUrbanExtent
import generateRectangularCoords
import imageio
import csv
import numpy as np
from scipy import misc
from scipy import ndimage
from PIL import Image, ImageDraw
import pandas as pd

#---------------------------------------
#Varbiles
district = 'Washim'
fileExtn = '.tif'
#---------------------------------------
areas = [2,5,10]
#folderName = 'districtUrbanizationcompleted/'+district.lower()+'District'
folderName = district.lower()+'District'
year = ['2016', '2019']
bgIndex = 0

if fileExtn == '.png':
    key = 191
    keyMode = 0
elif fileExtn == '.tif':
    key = 3
    keyMode = 1
DfIn = pd.read_csv('./min_max_coord.csv')
xMin = DfIn.loc[DfIn['District'] == district]['xMin'] 
xMax = DfIn.loc[DfIn['District'] == district]['xMax'] 
yMin = DfIn.loc[DfIn['District'] == district]['yMin']
yMax = DfIn.loc[DfIn['District'] == district]['yMax']

def calcUrbanization(cin, fileName, inX1, inY1, inX2, inY2, stateImage, xd, yd):
	pixelX = ((inX1 - xMin)/xd)
	rangeX = ((inX2 - inX1)/xd)
	pixelY = stateImage.shape[0] - ((inY1 - yMin)/yd)
	rangeY = ((inY2 - inY1)/yd)
	subImage = stateImage[int(pixelY-rangeY):int(pixelY), int(pixelX):int(pixelX+rangeX)]
	colorArray, countArray = np.unique(subImage, return_counts=True)
	print('------------------------------------------------------------------------------')
	print('Extracted sub image')
	print(np.unique(subImage, return_counts=True))
	'''
	Code to calculate Rural Urban Extent
	'''
	try:
		#imageio.imsave('./'+folderName+'/factoryImages/'+fileName+fileExtn, subImage)
		REPer = findRuralUrbanExtent.processImage(subImage, folderName, keyMode) 
		if key in list(colorArray):
			if bgIndex in list(colorArray):
				urbanVal = (float(countArray[list(colorArray).index(key)])*100/(float(sum(list(countArray)-(countArray[list(colorArray).index(bgIndex)])))))
			else:
				urbanVal = (float(countArray[list(colorArray).index(key)])*100/(float(sum(list(countArray)))))
			valExist = 1
		else:
			urbanVal = 0.0
			valExist = 0
	except ValueError:
		REPer = 0.0
		urbanVal = 0.0
		valExist = 0
	'''
	Code to bypass Rural Urban Extent
	REPer = 'Rural Extent Not Calculated'
	try:
		if bgIndex in list(colorArray):
			urbanVal = (float(countArray[list(colorArray).index(key)])*100/(float(sum(list(countArray)-(countArray[list(colorArray).index(bgIndex)])))))
		else:
			urbanVal = (float(countArray[list(colorArray).index(key)])*100/(float(sum(list(countArray)))))
		valExist = 1
	except ValueError:
		urbanVal = 0.0
		valExist = 0
	'''
	return REPer, urbanVal, valExist

if __name__== "__main__":
	f1 = open('./'+folderName+'/factoriesCoordinates.csv')
	csvFileHandler1 = list(csv.reader(f1))
	csvFile2 = open('./'+folderName+'/urbanizationData.csv',mode='w')
	csvFile3 = open('./'+folderName+'/factoriesCouldNotExtractFactoryImage.csv',mode='w')
	stateImage = []
	for i in range(len(year)):
		stateImage.append(imageio.imread('./'+folderName+'/'+district+'_prediction_temporal_'+year[i]+fileExtn))
	
	for row1 in csvFileHandler1:
		print(row1[1])
		for area in areas:
			combinedREPer = []
			combinedUrbanVal = []
			combinedValExist = []
			for yr in year:
				print(str(area)+' Kms, Year'+str(yr))
				dims = stateImage[list(year).index(yr)].shape
				xs = dims[1]
				ys = dims[0]
				xd = (xMax-xMin)/xs
				yd = (yMax-yMin)/ys
				y1, x1, y2, x2 = generateRectangularCoords.calcPolyBounds(float(row1[4]), float(row1[5]), float(area/2))
				#print(str(y1)+'\t'+str(x1)+'\t'+str(y2)+'\t'+str(x2))				
				name = row1[1]+'_'+str(area)+'Kms'+'_'+yr
				REPer, urbanVal, valExist = calcUrbanization(row1[0], name, float(y1), float(x1), float(y2), float(x2), stateImage[list(year).index(yr)], xd, yd)
				combinedREPer.append(REPer)
				combinedUrbanVal.append(urbanVal)
				combinedValExist.append(valExist)
			
			try:
				if sum(list(combinedValExist)) == len(combinedValExist):
					urbanValDiff = combinedUrbanVal[1]-combinedUrbanVal[0]
					csvFile2.write(row1[0]+','+row1[1]+','+str(area)+','+str(urbanValDiff)+','+str(max(combinedREPer))+'\n')
				else:
					csvFile3.write(row1[0]+','+row1[1]+','+row1[2]+','+row1[3]+','+row1[4]+','+row1[5]+','+row1[6]+','+row1[7]+','+row1[8]+','+str(area)+','+'urbanIndex (png:191/tif:3) not available'+'\n')
			except Exception as e:
				csvFile3.write(row1[0]+','+row1[1]+','+row1[2]+','+row1[3]+','+row1[4]+','+row1[5]+','+row1[6]+','+row1[7]+','+row1[8]+','+str(area)+','+str(e)+'\n')
