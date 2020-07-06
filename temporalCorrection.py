from PIL import Image
from scipy import misc
from scipy import ndimage
import imageio
import numpy as np
import pandas as pd
import unittest


# define color coding used
'''Background=0
Greenery=64
Water=127
BuiltUp=191
BareLand=255'''

Background=0
Greenery=1
Water=2
BuiltUp=3
BareLand=4

#fun to count occurence of x in list
def counter(x,listx):
    listx=np.asarray(listx)
    return(np.where(listx==x)[0].shape[0])

#fun to check pattern of inconsistency
def patterndetected(pixelVals):

    # find the first time a pixel was detected as Builtup
    for i in range(len(pixelVals)):
        if pixelVals[i] == BuiltUp :
            BuiltUpfirstindex = i
            break

    if (BuiltUp in pixelVals) and (not all(val==BuiltUp for val in pixelVals[BuiltUpfirstindex:])):
        #inconsistencies including Builtup pixels
        if(Greenery in pixelVals) and (Water in pixelVals) and (BareLand in pixelVals):
            return 1   #all classes present
        if(Greenery in pixelVals) and (Water in pixelVals):
            return 2
        if(Water in pixelVals) and (BareLand in pixelVals):
            return 3
        if(Greenery in pixelVals) and (BareLand in pixelVals):
            return 4
        if(Greenery in pixelVals):
            return 5
        if(Water in pixelVals):
            return 6
        if(BareLand in pixelVals):
            return 7

    #now either the pixelval doen't contain anu BuiltUp pixel so we need to check for inconsistencies within Non Built Up classes or pixel Val is consistent in respect to BuiltUp class so
    #we need to check for non builtup inconsistencies which could happen before encountering first builtup pixel.

    #inconsistencies within NBU classes
    if(Greenery in pixelVals) and (Water in pixelVals) and (BareLand not in pixelVals):
        return 8
    if(Water in pixelVals) and (BareLand in pixelVals) and (Greenery not in pixelVals):
        return 9

    return 0 #consistent


#defining correction methods for different pattern of inconsistencies
#method names defined upon the pixel values present in pixelVals
#1 denotes greenery, 2 denotes water, 3 denotes BuiltUp, 4 denotes Bareland

def pattern1234(pixelVals):
    bucount=counter(BuiltUp,pixelVals)
    if(counter(Greenery,pixelVals)>=counter(Water,pixelVals)):
        return [Greenery for i in pixelVals]
    else:
        return [Water for i in pixelVals]

def pattern123(pixelVals):
    return pattern1234(pixelVals)

def pattern234(pixelVals):
    bucount=counter(BuiltUp,pixelVals)
    if(counter(Water,pixelVals)>=bucount) and (counter(Water,pixelVals)>=counter(BareLand,pixelVals)):
        return [Water for i in pixelVals]
    if(counter(BareLand,pixelVals)>=bucount):
        return [BareLand for i in pixelVals]
    return [BuiltUp for i in pixelVals]

def pattern134(pixelVals):
    if(counter(BuiltUp,pixelVals)+counter(BareLand,pixelVals)<=counter(Greenery,pixelVals)):
        return [Greenery for i in pixelVals]
    return [BareLand for i in pixelVals]

def pattern13(pixelVals,i,j,dataset):
    if(counter(BuiltUp,pixelVals)>=counter(Greenery,pixelVals)):
        return [BuiltUp for i in pixelVals]
    dims=dataset[0].shape
    BuAreaCounts=0
    for k in range(len(pixelVals)):
        BUcount=0
        TotCount=0
        for row in range(i-2,i+3):
            if (row<0) or (row>=dims[0]):
                continue
            for col in range(j-2,j+3):
                if (col<0) or (col>=dims[1]):
                    continue
                if(dataset[k][row][col]==Background):
                    continue
                TotCount+=1
                if(dataset[k][row][col]==BuiltUp):
                    BUcount+=1
        if(BUcount>=0.5*TotCount):
            BuAreaCounts+=1
    if(BuAreaCounts>0.5*len(pixelVals)):
        return [BuiltUp for i in pixelVals]
    return [Greenery for i in pixelVals]
        

def pattern23(pixelVals):
    if(counter(Water,pixelVals)<=0.25*len(pixelVals)):
        return [BuiltUp for i in pixelVals]
    else:
        return [Water for i in pixelVals]


def pattern34(pixelVals):
    for i in range(len(pixelVals)):
        if pixelVals[i] == BuiltUp :
            BuiltUpfirstindex = i
            break
    if(counter(BuiltUp,pixelVals)>0.5*(len(pixelVals)-BuiltUpfirstindex)):
        return pixelVals[:BuiltUpfirstindex]+[BuiltUp for i in pixelVals[BuiltUpfirstindex:]]
    return [BareLand for i in pixelVals]

def pattern12_3(pixelVals):
    #since there are two possiblities with respect to the presence of BuiltUp class pixel, we need to find the index upto which we need to apply correction method
    correction_end_index=len(pixelVals)
    for i in range(len(pixelVals)):
        if pixelVals[i] == BuiltUp :
            correction_end_index = i
            break
    majority=Greenery if counter(Greenery,pixelVals)>=counter(Water,pixelVals) else Water
    return [majority for i in pixelVals[:correction_end_index]]+pixelVals[correction_end_index:]

    
def pattern24_3(pixelVals):
    #since there are two possiblities with respect to the presence of BuiltUp class pixel, we need to find the index upto which we need to apply correction method
    correction_end_index=len(pixelVals)
    for i in range(len(pixelVals)):
        if pixelVals[i] == BuiltUp :
            correction_end_index = i
            break
    majority=BareLand if counter(BareLand,pixelVals)>=counter(Water,pixelVals) else Water
    return [majority for i in pixelVals[:correction_end_index]]+pixelVals[correction_end_index:]


# list of districts
districts=['Tiruvannamalai']
#districts=['Ghaziabad','Gurgaon','Haora','Jaipur','KamrupMetropolitan','Medak','NorthGoa','Patan','RangaReddy','Rupnagar','Tirunelveli','Visakhapatnam']
for district in districts:
    print()
    print (district)

    year = [2016,2019]
    districtImage = imageio.imread('./'+district.lower()+'District'+'/'+district+'_prediction_'+str(2016)+'.tif')
    print(np.unique(districtImage,return_counts = True))
    #imageio.imwrite('./'+district.lower()+'District'+'/'+district+'_prediction_'+str(2016) + '.png',districtImage[:,:])
    districtImage1 = imageio.imread('./'+district.lower()+'District'+'/'+district+'_prediction_'+str(2019)+'.tif')
    print(np.unique(districtImage1,return_counts = True))
    #imageio.imwrite('./'+district.lower()+'District'+'/'+district+'_prediction_'+str(2019) + '.png',districtImage1[:,:])
    dataset = [imageio.imread('./'+district.lower()+'District'+'/'+district+'_prediction_'+str(i) + '.tif') for i in year]    #read all images

    # verify all images have same number of background pixels
    backgroundPixels = np.unique(dataset[0],return_counts=True)[1][0]
    '''if not all(np.unique(dataset[k],return_counts=True)[1][0]==backgroundPixels for k in range(len(dataset))):
        print("inconsistency in number of background pixels across years\n")
        raise SystemExit'''


    dims=dataset[0].shape
    patterns=[]

    for i in range(dims[0]):
        for j in range(dims[1]):
            if(dataset[0][i][j]==0):
                continue
            pixelVals=[dataset[k][i][j] for k in range(len(dataset))]  #transformation from seperate images to seperate list of values of each pixel across years.
            pattern=patterndetected(pixelVals)
            patterns.append(pattern)

            # callind relevant inconsistency correction method
            if pattern==0:
                newPixelVals=pixelVals
            elif pattern==1:
                newPixelVals=pattern1234(pixelVals)
            elif pattern==2:
                newPixelVals=pattern123(pixelVals)
            elif pattern==3:
                newPixelVals=pattern234(pixelVals)
            elif pattern==4:
                newPixelVals=pattern134(pixelVals)
            elif pattern==5:
                newPixelVals=pattern13(pixelVals,i,j,dataset)
            elif pattern==6:
                newPixelVals=pattern23(pixelVals)
            elif pattern==7:
                newPixelVals=pattern34(pixelVals)
            elif pattern==8:
                newPixelVals=pattern12_3(pixelVals)
            else:
                newPixelVals=pattern24_3(pixelVals)

            # set corrected values over the dataset
            for k in range(len(newPixelVals)):
                dataset[k][i][j] = newPixelVals[k]

    # finding the percentage of incorrect 
    patterns=np.asarray(patterns)
    counts=np.unique(patterns,return_counts=True)[1]
    correct=counts[0]
    incorrect=sum(counts[1:])
    incorrect_percent=incorrect*100/(correct+incorrect)
    print("incorrect percentage= ",incorrect_percent)


    # storing corrected images
    for i in range(len(year)):
	    imageio.imwrite('./'+district.lower()+'District'+'/'+district+'_prediction_temporal_'+str(year[i]) + '.tif',dataset[i])
