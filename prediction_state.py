from PIL import Image
import imageio
import numpy as np
from collections import Counter
from collections import OrderedDict
from operator import getitem
import itertools

state='Washim'
fileExtn = '.tif'
folderName = './'+state.lower()+'District/'
year=[2016, 2019]
key = 1#64#1
tiffFolder= folderName+state.lower()+'TiffImages/'
allPrediction = []
months=['01','02','03','04','05','06','07','09','10','11','12']

def getPrediction(state, yr):
	onePrediction = []
	actualMonths = []
	for month in months:
		tif_inputfile= state +'_'+month+yr
		try:
			colorArray, countArray = np.unique(imageio.imread(tiffFolder+"/"+tif_inputfile+fileExtn),return_counts = True)
			resultDict = dict(zip(colorArray, countArray))
			#print(resultDict)
			onePrediction.append(resultDict)
			actualMonths.append(month)
		except FileNotFoundError:
			continue
	monthDict = dict(zip(actualMonths, onePrediction))
	return monthDict

def getMedianPrediction(state, yr):
	onePrediction = []
	tif_inputfile= state +'_median_'+yr
	colorArray, countArray = np.unique(imageio.imread(tiffFolder+"/"+tif_inputfile+fileExtn),return_counts = True)
	resultDict = dict(zip(colorArray, countArray))
	#print(resultDict)
	onePrediction.append(resultDict)
	medianDict = dict(zip('m', onePrediction))
	return medianDict

def is_number_exist(num,listx):
    listx=set(listx)
    if num in listx:
        return True
    
def count(num,listx):
    keys = list(Counter(listx).keys())
    values = list(Counter(listx).values())
    flag = False
    flag = is_number_exist(num,keys)
    if flag == True:
        num_count = values[keys.index(num)]
    else:
        num_count = 0
    return num_count

def merge_prediction(x):
    background_count = count(0,x)
    grass_count = count(1,x)
    water_count = count(2,x)
    buildings_count = count(3,x)
    bareland_count = count(4,x)
    total = len(x)
    if (background_count == total):
        return '0'
    elif (water_count >= 1 and water_count > grass_count):
        return '2'
    elif ( grass_count >=1 ):
        return '1'
    elif((bareland_count > buildings_count) and grass_count==0 and water_count==0 ):
        return '4'
    else:
        return '3'
        

def merge_prediction2(x,median):
    background_count = count(0,x)
    grass_count = count(1,x)
    water_count = count(2,x)
    buildings_count = count(3,x)
    bareland_count = count(4,x)
    total = len(x)
    if (background_count == total):
        return '0'
    elif (water_count >= 1 and water_count > 1.5 * grass_count and grass_count>0):
        return '2'
    elif (water_count >= 0.5 * total):
        return '2'
    elif (water_count >= 1 and water_count <= 1.5 * grass_count and grass_count>0):
        return '1'
    elif (water_count != 0 and grass_count == 0 ):
        return str(median)
#     elif (water_count !=0 and grass_count==0 and water_count >= total/2):
#         return '2'
    elif ( grass_count >=1 ):
        return '1'
    elif((bareland_count > buildings_count) and grass_count==0 and water_count==0 ):
        return '4'
    else:
        return '3'        

def calcMergedPrediction(keyList, medianPrediction, yr, count):
	prediction1 = imageio.imread(tiffFolder+"/"+state +'_'+keyList[0%count]+yr+fileExtn)
	prediction2 = imageio.imread(tiffFolder+"/"+state +'_'+keyList[1%count]+yr+fileExtn)
	prediction3 = imageio.imread(tiffFolder+"/"+state +'_'+keyList[2%count]+yr+fileExtn)
	prediction4 = imageio.imread(tiffFolder+"/"+state +'_'+keyList[3%count]+yr+fileExtn)
	prediction5 = imageio.imread(tiffFolder+"/"+state +'_'+keyList[4%count]+yr+fileExtn)
	prediction_median = imageio.imread(tiffFolder+"/"+state+'_median_'+yr+fileExtn)
	image_dimension = prediction1.shape
	#print(image_dimension)

	final_prediction = np.arange(image_dimension[0] * image_dimension[1]).reshape(image_dimension)
	#print(final_prediction)
	counter = 0
	for i in range(image_dimension[0]):
		if counter == 500:
			print(str(i)+'/'+str(image_dimension[0]))
			counter = 0
		for j in range(image_dimension[1]):
			x=[ prediction1[i][j], prediction2[i][j], prediction3[i][j], prediction4[i][j], prediction5[i][j]]
			final_prediction[i,j] = merge_prediction2(x, prediction_median[i][j])
		counter = counter+1
	
	print("final_prediction ",np.unique(final_prediction,return_counts=True))
	imageio.imwrite(folderName+ state +'_prediction_'+yr+'.tif', final_prediction[:,:])

if __name__ == '__main__':
    for yr in year:
    	oneYrPrediction = getPrediction(state, str(yr))
    	print(oneYrPrediction)
    	sortedOneYrPrediction = OrderedDict(sorted(oneYrPrediction.items(), key = lambda x: getitem(x[1], key), reverse=True))
    	#print(res)
    	oneYrMedianPrediction = getMedianPrediction(state, str(yr))
    	if len(sortedOneYrPrediction) >= 5:
    		top5OneYrPrediction = dict(itertools.islice(sortedOneYrPrediction.items(), 5))
    		calcMergedPrediction(list(top5OneYrPrediction.keys()), oneYrMedianPrediction, str(yr), 5)
    	else:
    		top5OneYrPrediction = dict(itertools.islice(sortedOneYrPrediction.items(), len(sortedOneYrPrediction)))
    		calcMergedPrediction(list(top5OneYrPrediction.keys()), oneYrMedianPrediction, str(yr), len(sortedOneYrPrediction))

    	#print(oneYrMedianPrediction)
    	#top5OneYrPredictionListKeys = list(top5OneYrPrediction.keys())#list(zip(top5OneYrPrediction.keys(), top5OneYrPrediction.values()))
    	#print(list(top5OneYrPrediction.keys()))
    	#print('----------------------------')
