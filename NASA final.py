import requests
import json
from pprint import pprint
import MySQLdb as db

id_list = []
id_list2 = []
cat8_out =[]
cat10_out =[]
cat14_out =[]

cat_type = []
date_list = []
coord_list = []
title = []
url_list = []
idret_list = []
final = [[],[],[],[],[],[]]

# Create a list of source IDs -
#This makes for more robust and adaptable program, as sources may vary or go offline.

sourceids = requests.get("https://eonet.sci.gsfc.nasa.gov/api/v2.1/sources") 
sout = sourceids.json()
dict_list = (sout["sources"])
num_ids = len(dict_list)

## Parse out id and title values

for i in range (0, num_ids):

      idout = ((dict_list[i])["id"])
      idout2 = ((dict_list[i])["title"])
      str_idout = idout.encode('ascii','ignore')
      str_idout2 = idout2.encode('ascii','ignore') 
      id_list.append(str_idout)
      id_list2.append(str_idout2)
      
## Print sources in use
pprint (id_list)
source_tab_data = zip(id_list2,id_list)

## Get category 8 events

for i in range (0, num_ids):

        paar = (id_list[i])
        cat8_events = requests.get("https://eonet.sci.gsfc.nasa.gov/api/v2.1/categories/8?"                                 
        "&days=30"
        "&source={0}"
        "&status=closed"
        .format(paar))

        g8 = cat8_events.json()
        events = (g8[u'events'])
        cat8_out.append(events)

## Get category 10 events 

for i in range (0, num_ids):

        paar = (id_list[i])
        cat10_events = requests.get("https://eonet.sci.gsfc.nasa.gov/api/v2.1/categories/10?"                                 
        "&days=30"
        "&source={0}"
        "&status=closed"
        .format(paar))

        g10 = cat10_events.json()
        events = (g10[u'events'])
        cat10_out.append(events)

## Get category 14 events 

for i in range (0, num_ids):

        paar = (id_list[i])
        cat14_events = requests.get("https://eonet.sci.gsfc.nasa.gov/api/v2.1/categories/14?"                                 
        "&days=30"
        "&source={0}"
        "&status=closed"
        .format(paar))

        g14 = cat14_events.json()
        events = (g14[u'events'])
        cat14_out.append(events)

## remove empty lists

clean8 = [x for x in cat8_out if x != []]
clean10 = [x for x in cat10_out if x != []]
clean14 = [x for x in cat14_out if x != []]
catout_list = [x for x in [clean8,clean10,clean14] if x != []]

rake = len(catout_list)

## Loop through categories, count active sources

for p in range (0,rake):
      this_cat = catout_list[p]
      cat_length = len(this_cat)

## Loop through active sources and count events
      
      for i in range (0, cat_length):
      
            evento = ((this_cat)[i])
            current = len(evento)

# Extract individual event data 

            for i in range (0, current):
      
                  det1 = ((evento[i])[u'geometries'])
            
                  dets1a = (((det1[0])[u'date']).encode('ascii','ignore'))
                  dets1b = ((det1[0])[u'coordinates'])
      
                  det2 = (((evento[i])[u'title']).encode('ascii','ignore'))
      
                  det3 = ((evento[i])[u'sources'])
                  det3a = (((det3[0])[u'url']).encode('ascii','ignore'))
                  det3b = (((det3[0])[u'id']).encode('ascii','ignore'))

                  det4 = ((evento[i])[u'categories'])
                  det4a = ((det4[0])[u'id'])
                           
                  date_list.append(dets1a)
                  title.append(det2)
                  url_list.append(det3a)
                  idret_list.append(det3b)
                  cat_type.append(det4a)
                           
##                coord_list.append(dets1b)


## combine outputted lists
                  
                  final = zip(cat_type,title,date_list,url_list,idret_list)

## print results
      
pprint(final)

##Connect to local db host

conn = db.connect (host = "localhost", user = "root", passwd = "t9EZPfzQ", db = "nasadb")
cu = conn.cursor ()

cu.execute ("CREATE DATABASE nasadb")
cu.execute ('USE nasadb')

## Create and populate tables 

cu.execute (' CREATE TABLE IF NOT EXISTS source ( id INT unsigned NOT NULL AUTO_INCREMENT, Source_Name VARCHAR(90) NOT NULL, Source_ID VARCHAR(30) NOT NULL, PRIMARY KEY (id) )')

cu.execute ("CREATE TABLE IF NOT EXISTS event_values (id INT unsigned NOT NULL AUTO_INCREMENT, cat_type INT unsigned NOT NULL, title VARCHAR(80) NOT NULL, date VARCHAR(30) NOT NULL, url VARCHAR(120) NOT NULL, source_ID VARCHAR(30) NOT NULL, PRIMARY KEY (id) )")

source_fill = "INSERT INTO source (Source_Name, Source_ID) VALUES (%s, %s)"
cu.executemany(source_fill, source_tab_data)

roos = 'INSERT INTO event_values (cat_type, title, date, url, source_ID) VALUES (%s, %s, %s, %s, %s)'
cu.executemany(roos,final)

