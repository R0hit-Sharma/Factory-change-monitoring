import imageio
import numpy as np
#import matplotlib.pyplot as plt
from matplotlib import colors
import subprocess
import glob
import csv
'''
#--------------------------------------
district = 'Bangalore'
keyPostProcessing = 2
fileExtn = '.tif'
if fileExtn == '.png':
    keyPreProcessing = 191
    keyMode = 0
elif fileExtn == '.tif':
    keyPreProcessing = 3
    keyMode = 1
#--------------------------------------
folderName = district.lower()+'District'
files = glob.glob("./"+folderName+"/factoryImages/*"+fileExtn)
csvFile1 = open("./"+folderName+'/ruralUrbanExtent.csv',mode='w')
file2 = open("./"+folderName+'/couldNotFindRuralUrbanExtent.csv', mode='w')
cmap = colors.ListedColormap({0:'black',
                                    1:'darkred',
                                    2:'darkorange',
                                    3:'white'})
'''
def processImage(mat, folderName, keyMode):
    np.savetxt("./"+folderName+"/tempIn.txt",mat,'%d')
    unique_elements, counts_elements = np.unique(mat, return_counts=True)
    cmap = colors.ListedColormap(['black','green','blue','darkorange','white'])
    image = np.loadtxt("./"+folderName+"/tempIn.txt", dtype=np.int64, delimiter=' ')
    unique_elements, counts_elements = np.unique(image, return_counts=True)
    image = np.array(image, dtype='float64')
    cmd = ["./a.out",str(keyMode), "./"+folderName]
    tmp=subprocess.call(cmd)
    cmap = colors.ListedColormap(['black','darkred','darkorange','white'])
    image = np.loadtxt("./"+folderName+"/tempOut.txt", dtype=np.int64, delimiter=' ')
    unique_elements, counts_elements = np.unique(image, return_counts=True)
    print(unique_elements)
    print('------------------------------------------------------------------------------')
    print(counts_elements)
    print('Values for Rural Extent (0: background, 2 (1,2,4): non builtup, 3: builtup)')
    print(np.unique(image, return_counts=True))
    print('------------------------------------------------------------------------------')
    image = np.array(image, dtype='float64')
    if 2 in list(unique_elements) and 0 in list(unique_elements):
        REPer = str(float(counts_elements[list(unique_elements).index(2)])*100/float(sum(list(counts_elements))-counts_elements[list(unique_elements).index(0)]))
    elif 2 in list(unique_elements) and 0 not in list(unique_elements):
        REPer = (float(counts_elements[list(unique_elements).index(2)])*100/float(sum(list(counts_elements))))
    elif 2 not in list(unique_elements):
        REPer = 0.0
    return REPer
'''
if __name__== "__main__":
    for f in files:
        if f.startswith('./'):
            f = f[2:]
        if f.endswith(fileExtn):
            f = f[:-4]
        fileName = f.replace(folderName+'/factoryImages/','')
        mat = imageio.imread(f+fileExtn)
        REPerVal = processImage(mat)
        csvFile1.write(f+','+REPerVal+'\n')
'''
