import imageio
import generateRectangularCoords
from PIL import Image
import csv
import numpy as np
from scipy import misc
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
#---------------------------------------
#Varbiles
district = 'Surat'
key = 3#191#3
fileExtn = '.tif'
fileExtnOut = '.png'

DfIn = pd.read_csv('./min_max_coord.csv')
xMin = DfIn.loc[DfIn['District'] == district]['xMin'] 
xMax = DfIn.loc[DfIn['District'] == district]['xMax'] 
yMin = DfIn.loc[DfIn['District'] == district]['yMin']
yMax = DfIn.loc[DfIn['District'] == district]['yMax']

#xMin = 71.6202697753906 
#xMax = 72.8503570556641 
#yMin = 22.0120811462402
#yMax = 23.505931854248
#---------------------------------------
folderName = district.lower()+'District'
year = ['2016','2019']

def calcUrbanization1(fileName, inX1, inY1, inX2, inY2, yr, stateImage, xd, yd):
	#X represents longitude
	#Y represents latitude
	#print('xd:'+str(xd))
	#print('yd:'+str(yd))
	print(str(stateImage.shape))
	pixelX = (inX1 - xMin)/xd
	rangeX = (inX2 - inX1)/xd
	pixelY = stateImage.shape[0] - ((inY1 - yMin)/yd)
	rangeY = (inY2 - inY1)/yd
	print('Location Dim:'+'x:'+str(pixelX)+' xr:'+str(pixelX+rangeX)+' y:'+str(pixelY-rangeY)+' yr:'+str(pixelY))

	subImage = stateImage[int(pixelY-rangeY):int(pixelY), int(pixelX):int(pixelX+rangeX)]
	colorArray, countArray = np.unique(subImage, return_counts=True)
	print('----------------------------------------------------------')
	print(str(np.unique(stateImage, return_counts=True)))
	print('----------------------------------------------------------')
	print(str(np.unique(subImage, return_counts=True)))
	print('----------------------------------------------------------')
	try:
		if 0 in list(colorArray):
			print(str(float(countArray[list(colorArray).index(key)])*100/float(sum(list(countArray))-countArray[list(colorArray).index(0)])))
		else:
			print(str(float(countArray[list(colorArray).index(key)])*100/float(sum(list(countArray)))))
	except ValueError:
		print(str(colorArray)+', '+ str(countArray))	
	
	imageio.imsave('./'+folderName+'/'+'subImage_'+yr+fileExtnOut, subImage)
	stateImage1 = Image.open('./'+folderName+'/'+district+'_marked_'+yr+fileExtnOut)
	img_draw = ImageDraw.Draw(stateImage1)

	for i in range(int(stateImage.shape[1]/100)+1):
		#draw blue longitude lines
		x = 100*i
		y = 100
		#img_draw.rectangle((int(x-5),int(y-5),int(x+5),int(y+5)), outline = colors[i], width = 10)
		img_draw.text((x,y), str(x), font=ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40), fill='blue')
		img_draw.line((x,0,x,stateImage.shape[0]), fill='blue', width = 1)

	for i in range(int(stateImage.shape[0]/100)+1):
		#draw violet latitude lines
		x = 100
		y = 100*i
		#img_draw.rectangle((int(x-5),int(y-5),int(x+5),int(y+5)), outline = colors[i], width = 10)
		img_draw.text((x,y), str(y), font=ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40), fill='violet')
		img_draw.line((0,y,stateImage.shape[1],y), fill='violet', width = 1)
	img_draw.rectangle((int(pixelX),int(pixelY),int(pixelX+rangeX),int(pixelY-rangeY)), outline = 'red', width = 10)
	stateImage1.save('./'+folderName+'/'+district+'_marked_'+yr+fileExtnOut)

if __name__== "__main__":

	f1 = open('./'+folderName+'/trial.csv')
	csvFileHandler1 = list(csv.reader(f1))
	for row1 in csvFileHandler1:
		for yr in year:
			print(str(yr))
			#stateImage1 = Image.open('./'+folderName+'/'+district+'_prediction_'+yr+'.tif')
			#stateImage1.save('./'+folderName+'subImage_'+yr+'_marked'+fileExtn)
			#stateImage1.save('./'+folderName+'/'+district+'_prediction_'+yr+fileExtn)
			img = imageio.imread('./'+folderName+'/'+district+'_prediction_'+yr+fileExtn)
			print('Original Image in TIF')
			print(str(np.unique(img, return_counts=True)))
			imageio.imwrite('./'+folderName+'/'+district+'_prediction_'+yr+'_colored'+fileExtnOut,img[:,:])
			stateImage1 = Image.open('./'+folderName+'/'+district+'_prediction_'+yr+'_colored'+fileExtnOut)
			stateImage1 = stateImage1.convert("RGBA")
			pixdata = stateImage1.load()
			print('Converted Colored Image in PNG')
			print(str(np.unique(stateImage1, return_counts=True)))
			#print(stateImage1.getcolors())
			for y in range(stateImage1.size[1]):
				for x in range(stateImage1.size[0]):
				  if pixdata[x, y] == (0, 0, 0, 255):
				    pixdata[x, y] = (0,0,0, 0)
				  elif pixdata[x, y] == (64, 64, 64, 255):
				    pixdata[x, y] = (34,139,34, 255)
				  elif pixdata[x, y] == (127, 127, 127, 255):
				    pixdata[x, y] = (2, 4, 251, 255)
				  elif pixdata[x, y] == (191, 191, 191, 255):
				    pixdata[x, y] = (255, 255, 102, 255)
				  elif pixdata[x, y] == (255, 255, 255, 255):
				    pixdata[x, y] = (255, 80, 80, 255)
			stateImage1.save('./'+folderName+'/'+district+'_prediction_'+yr+'_colored'+fileExtnOut)
			imageio.imwrite('./'+folderName+'/'+district+'_marked_'+yr+fileExtnOut, stateImage1)
			#stateImage = imageio.imread('./'+folderName+'/'+district+'_prediction_'+yr+'_colored'+fileExtnOut)
			stateImage = imageio.imread('./'+folderName+'/'+district+'_prediction_'+yr+fileExtn)
			print('Reading Converted Colored Image in PNG')
			print(str(np.unique(stateImage, return_counts=True)))
			dims = stateImage.shape
			xs = dims[1]
			ys = dims[0]
			print('Image Dim:'+str(xs)+'x'+str(ys))
			xd = (xMax-xMin)/xs
			yd = (yMax-yMin)/ys
			area=10
			y1, x1, y2, x2 = generateRectangularCoords.calcPolyBounds(float(row1[4]), float(row1[5]), float(area/2))
			print(str(y1)+','+str(x1)+','+str(y2)+','+str(x2))
			calcUrbanization1('trial', y1, x1, y2, x2, yr, stateImage, xd, yd)
			print('----------------------------')	
