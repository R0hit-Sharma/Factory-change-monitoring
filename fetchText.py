import storemeta
import storedata
import sys
import csv
import pprint
import logging
import logging.config
from string import Template
import psycopg2
import psycopg2.extras
import urllib2
from bs4 import BeautifulSoup
import requests
import traceback
count =0
pp = pprint.PrettyPrinter(indent=4)
collName='googleSearch'

csvFile = open('./allCompanies.csv')
csvWriteFile = open('./companyLocation.csv',mode='w')
csvFileHandler = list(csv.reader(csvFile))

def connect():
    conn = psycopg2.connect("dbname=rohit_varun_db user=rohit_varun password=123456 host=10.237.26.159 port=5432")
    return conn

def fetchArticleText(url, cin):
    global count, collName
    #url=urlJson.url.strip()
    #url = "https://www.dynamiclevels.com/en/KESAR-ENTERPRISES-company-location"
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    #print(soup.prettify())
    table = soup.find('table', {'class':'table table-bordered tb'})
    rows = table.findAll('td')[2:]

    for i in range(0,len(rows),2):
	   	t = ' '.join(rows[i+1].text.split()).replace(',','')
	   	print(rows[i].text, t)
	   	temp = str(cin)+','+rows[i].text+','+t+'\n'
		csvWriteFile.write(temp)

def getNextURLs():
    conn = connect()
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    dict_cur.execute("""
                        Select * from urltable
                        where processed is NULL
                        limit 2;
                     """)
    
    urlDataList = dict_cur.fetchall()
    dict_cur.close()
    conn.close()
    return urlDataList

def fetchUrls(compName, cin):
	for i in range(len(compName.split()),0,-1):
		#print('-'.join(compName.split()[0:i]))
		baseAddr = 'https://www.dynamiclevels.com/en/'+'-'.join(compName.split()[0:i]).upper()+'-company-location'
		try:
			fetchArticleText(baseAddr, cin)
		except AttributeError:
			continue
		except:
			traceback.print_exc()
			continue

if __name__ == '__main__':
    #fetchUrls('kesar ENTerpRISES Pvt Ltd', 1234)
    for row in csvFileHandler:
    	fetchUrls(row[1], row[0])
        #fetchArticleText(url)