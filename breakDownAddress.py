# importing csv module
import csv
import requests
import time
import json
from pymongo import MongoClient

f2 = open("./companyLocationWithName.csv")
f3 = open("./companyLocationWithDistricts.csv",mode= 'a')

csv_f2 = list(csv.reader(f2))
#csv_f3 = csv.writer(f3,delimiter=',')


GOOGLE_MAPS_API_URL = 'your key goes here'

def getAddressJson(cin, compName, building_type, addr):
    locality = ''
    admAreaLvl1 = ''
    admAreaLvl2 = ''

    params = {
            'address': compName +' '+ addr,
            'sensor': 'false',
            'region': 'India'
            }

        # Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()

    if res['status'] == 'OK':
        #print(res)
        lat = res['results'][0]['geometry']['location']['lat']
        lng = res['results'][0]['geometry']['location']['lng']
        for i in range(len(res['results'][0]['address_components'])):
        	if bool(res['results'][0]['address_components'][i]['types']):
	            if res['results'][0]['address_components'][i]['types'][0] == 'locality':
	                locality = res['results'][0]['address_components'][i]['long_name']
	            elif res['results'][0]['address_components'][i]['types'][0] == 'administrative_area_level_1':
	                admAreaLvl1 = res['results'][0]['address_components'][i]['long_name']
	            elif res['results'][0]['address_components'][i]['types'][0] == 'administrative_area_level_2':
	                admAreaLvl2 = res['results'][0]['address_components'][i]['long_name']
        try:
            f3.write(cin+','+compName+','+building_type+','+addr+','+str(lat)+','+str(lng)+','+locality+','+admAreaLvl2+','+admAreaLvl1+'\n')
            print(compName+'\t'+building_type+'\t'+locality+'\t'+admAreaLvl2+'\t'+admAreaLvl1)
        except UnicodeEncodeError:
            pass
    elif res['status'] == 'REQUEST_DENIED':
        print('Response status was '+res['status']+'. Sleeping for 30 sec.')
        time.sleep(30)
        getAddressJson(cin, compName, building_type, addr)
    elif res['status'] == 'ZERO_RESULTS':
    	print('Response status was '+res['status']+'. Continuing.')
    	pass
    elif res['status'] == 'OVER_QUERY_LIMIT':
    	print('Response status was '+res['status']+'. Sleeping for 1 day.')
    	time.sleep(24*60*60)
    	getAddressJson(cin, compName, building_type, addr)
    else:
        print('Response status was '+res['status']+'. Sleeping for 30 sec.')
        time.sleep(30)
        getAddressJson(cin, compName, building_type, addr)

if __name__ == '__main__':
    for row in csv_f2:
        getAddressJson(row[0], row[1], row[2], row[3])
        time.sleep(2)
    #getAddressJson('123','MURLI INDUSTRIES LIMITED CN','A','Cement Unit Chandrapur District - Maharashtra - India Phone : Fax : Email : Internet :')
