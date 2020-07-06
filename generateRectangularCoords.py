'''
i/p: a file named factoriesCoordinates.csv in folder <District>.
	This file is made from companyLocationsForAnalysis.csv by manually selecting the required <District>
'''
from math import sqrt,atan,pi
import csv
#import pyproj
#geod = pyproj.Geod(ellps='WGS84')
district = 'Ahmedabad'
folderName = district.lower()+'District'
areas = [2, 5, 10]

def calcPolyBounds(x, y, distance):
	y1 = y - (1*float(distance))/100
	x1 = x - (1*float(distance))/111
	#point_A = temp_y, temp_x
	y2 = y + (1*float(distance))/100
	x2 = x + (1*float(distance))/111
	#point_B = temp_y, temp_x
	return y1, x1, y2, x2


if __name__== "__main__":
	for area in areas:
		f1 = open('./'+folderName+'/factoriesCoordinates.csv')
		csvFileHandler1 = list(csv.reader(f1))
		csvFile3 = open('./'+folderName+'/factoriesWithAreaCoordinates_'+str(area)+'Kms.csv',mode='w')
		for row1 in csvFileHandler1:
			y1, x1, y2, x2 = calcPolyBounds(float(row1[4]), float(row1[5]), float(area/2))
			name = row1[1]+'_'+str(area)+'Kms'
			csvFile3.write(row1[0]+','+row1[1]+','+str(y1)+','+str(x1)+','+str(y2)+','+str(x2)+','+name+'\n')
