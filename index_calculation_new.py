# python 3
# -*- coding: utf-8 -*-

"""
Created on Thu Jun  6 10:49:31 2019

@author: Prachi Singh
"""
import sys,os
import copy
import numpy as np
from scipy import misc
from scipy import ndimage
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit
import imageio
import numpy as np
import pandas as pd
from pylab import *
from PIL import Image
# from scipy.misc import imsave
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
import csv
# import seaborn as sn
# from sklearn.metrics import confusion_matrix

district = 'Surat'
folderName = district.lower()+'District'
fileExtn = '.tif'
def calculate_thresholds(district, cost_array):
    
    threshold_1=1.95
    return threshold_1
    
all_cities_actual = []
all_cities_predicted = []   
labels = [1,2,3,4]
 


cities = ['Surat']
for district in cities:
    print(district)
    cost_array = np.loadtxt('./'+folderName+'/_conv_gaus_removed_16_24N_cost_array.txt')
    cost_array = cost_array/1000
    threshold1 = calculate_thresholds(district, cost_array)
    
    string_threshold = "threshold 1:",threshold1
    print(string_threshold)
    
    band = imageio.imread('./'+folderName+'/'+district+'_prediction_temporal_'+str(2019)+fileExtn)
    data = band/240
    dims = band.shape
    band1 = band
    print (np.unique(data))
    mask = np.sign(band)
    k = np.array([[1,1,1],[1,1,1],[1,1,1]])
    mask1 = ndimage.convolve(mask, k, mode='constant', cval=0.0)
    
    iter=0
    cbu = 0
    cnbu = 0
    changing = 0

    for j in range(0, dims[0]):
      for k in range(0, dims[1]):
          if (mask1[j][k] == 9):
              if (cost_array[iter]<=threshold1):
                  if data[j][k]==1:
                      band1[j][k] = 255
                      cnbu += 1
                  else:
                      band1[j][k] = 200
                      cbu += 1
              else:
                  changing += 1
                  band1[j][k] = 100        
              iter += 1
          else:
              if(band1[j][k]!=0):
                  band1[j][k]=0

    total = cnbu+cbu+changing
    print((cnbu*100)/total, (cbu*100)/total, (changing*100)/total)
    print(np.unique(band1))
    imageio.imwrite('./'+folderName+'/'+district+'_prediction_temporal_mayank'+str(2019)+fileExtn, band1)
    
    
