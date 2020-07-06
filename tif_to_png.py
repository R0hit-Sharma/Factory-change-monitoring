import imageio
import csv
import numpy as np
from scipy import misc
from scipy import ndimage
from PIL import Image, ImageDraw
import pandas as pd


fileExtn = '.tif'
fileExtn1 = '.png'
'''
#---------------------------------------

districts=['Ajmer','Bangalore','Bathinda','Bharuch','DadraandNagarHaveli','Dhenkanal','EastGodavari','Hardwar','Kangra','Korba','Nagpur','Prayagraj','Raigad','Shahdol','Surat','Thane','UdhamSinghNagar','Vadodara']
for district in districts:	
	Imagetwo = Image.open('./'+district.lower()+'District'+'/'+district+'_prediction_temporal_2019'+fileExtn)
	print(district + str(np.unique(Imagetwo, return_counts=True))) '''
district = 'Surat'
folderName = district.lower()+'District'
year = ['2016', '2019']
img = imageio.imread('./'+folderName+'/'+district+'_box_shape'+fileExtn)
imageio.imwrite('./'+folderName+'/'+district+'_box_shape'+fileExtn1,img[:,:])
img1 = Image.open('./'+folderName+'/'+district+'_box_shape'+fileExtn1)
print(district + str(np.unique(img1, return_counts=True)))
img1 = img1.convert("RGBA")
pixdata = img1.load()
print(img1.getcolors())
for y in range(img1.size[1]):
    for x in range(img1.size[0]):
        if pixdata[x, y] == (0, 0, 0, 255): #background
            pixdata[x, y] = (0,0,0, 0)
        elif pixdata[x, y] == (64, 64, 64, 255):      #green
            pixdata[x, y] = (34,139,34, 255)
        elif pixdata[x, y] == (76, 76, 76, 255):      #green
            pixdata[x, y] = (34,139,34, 255)
        elif pixdata[x, y] == (127, 127, 127, 255):    #water
            pixdata[x, y] = (2, 4, 251, 255)
        elif pixdata[x, y] == (191, 191, 191, 255):   #buildingd 
            pixdata[x, y] = (255, 255, 102, 255)
        elif pixdata[x, y] == (255, 255, 255, 255):   #bareland
            pixdata[x, y] = (255, 80, 80, 255)
img1.save('./'+folderName+'/'+district+'_box_shape_colored'+fileExtn1)

	



