import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

f1 = "XPRO INDIA LIMITED_5Kms"

mat = cv2.imread(f1+".png",cv2.IMREAD_GRAYSCALE)
np.savetxt(f1+".txt",mat,'%d')

unique_elements, counts_elements = np.unique(mat, return_counts=True)
print(unique_elements,counts_elements)
cmap = colors.ListedColormap(['black','green','blue','darkorange','white'])
image = np.loadtxt(f1+".txt", dtype=np.int64, delimiter=' ')
print(image.shape)
unique_elements, counts_elements = np.unique(image, return_counts=True)
print(unique_elements,counts_elements)
image = np.array(image, dtype='float64')
plt.imshow(image,cmap=cmap)
plt.show()
cmap = colors.ListedColormap(['black','darkred','darkorange','white'])
image = np.loadtxt(f1+"_urban_extent.txt", dtype=np.int64, delimiter=' ')
print(image.shape)
unique_elements, counts_elements = np.unique(image, return_counts=True)
print(unique_elements,counts_elements)
image = np.array(image, dtype='float64')
# 3 = Discarded ||  2 = Rural || 1 = Peri-Urban || 0 = Urban
plt.imshow(image,cmap=cmap)
plt.show()
cmap = colors.ListedColormap({0:'black',
                              1:'darkred',
                              2:'darkorange',
                              3:'white'})
                              
