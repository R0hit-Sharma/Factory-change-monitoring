import glob
import csv
import os
csv_dir = os.getcwd()

if __name__== "__main__":
 
  csv_output = open('./'+'output.csv',mode='w')
  for filename in glob.glob('./districtUrbanizationcompleted/**/urbanizationData.csv'):
   #print('here')
   with open(filename, newline='') as f_input:
     csv_input = csv.reader(f_input)
     name1,name2,name3,name4 = filename.split('/')
     print(name3[:-8])
     for row in csv_input:
      row.insert(5, name3[:-8])
      csv_output.write(row[0]+','+row[1]+','+row[2]+','+row[3]+','+row[4]+','+row[5]+'\n')
