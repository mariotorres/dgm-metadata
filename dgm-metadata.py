#! /usr/bin/python

#### -----------------------------------------
#### Script for mining the contents of ckan
####
#### -----------------------------------------

##------------------------------
## Libraries
##------------------------------
import requests
import sys
import json, urllib, string
import pandas as pd

##------------------------------
## Download list of datasets
##------------------------------
base         = "http://datos.gob.mx/busca/api/3/action/"
url_datasets = base + "package_list"

response = None
all_datasets = None
try:
    response = urllib.request.urlopen(url_datasets)
    all_datasets = json.loads(response.read())
except:
    print("Can't connect to CKAN")
    sys.exit(1)


## printable characters
printable = set(string.printable)

##------------------------------
## Download resources datasets
##------------------------------
## Dataset features.
conj_id    = []
conj_name  = []
conj_title = []
conj_desc  = []
dep        = []
slug       = []
url_conj   = []
fecha_c    = []
fecha_m    = []
## Resource features.
res_name   = []
res_size   = []
res_desc   = []
res_id     = []
res_url    = []


def checkURL(url):
    ## Test for broken links
    try:
        request = requests.get(url, timeout = 1, allow_redirects = False)
    except:
        return -1
    return request.status_code

########################################
# Add Features
########################################
#k = 0
for i in all_datasets['result']:
   # print(k)
    #k = k + 1
    ## Obtain datasets.
    dataset_url = base + "package_show?id=" + str(i) # base + "package_search?q=" + str(i)
    print (i)
    #print(dataset_url)

    try:
        response    = urllib.request.urlopen(dataset_url)
        dataset     = json.loads(response.read())

        ## For all resources.
        dataset_res = dataset['result'] #dataset['result']['results'][0]
        for resource in dataset_res['resources']:
            # Fill in datasets features
            conj_id.append(dataset_res['id'])  # Id del conjunto
            conj_name.append(dataset_res['name'])  # Nombre del conjunto
            conj_title.append(dataset_res['title'])  # Nombre del conjunto
            conj_desc.append(dataset_res['notes'])   # Descripcion del conjunto
            if dataset_res['organization'] is not None:
                dep.append(dataset_res['organization']['title']) # Dependencia
                slug.append(dataset_res['organization']['name']) # Slug
            else:
                dep.append('') # Dependencia
                slug.append('') # Slug
            url_conj.append(dataset_res['url'])  # URL del conjunto
            fecha_c.append(dataset_res['metadata_created']) # Metadata creation
            fecha_m.append(dataset_res['metadata_modified']) # Metadata modification
            # Fill in resources features
            res_name.append(resource['name'])
            res_id.append(resource['id'])
            res_size.append(resource['size'])
            res_desc.append(resource['description'])
            res_url.append(resource['url'])
    except:
        print ("Mamó el dataset \n\t"+ dataset_url)


########################################
## Create data table
########################################
d = {'slug'         :  slug,
     'dep'          :  dep,
     'conj_id'      :  conj_id,
     'conj'         :  conj_name,
     'conj_tit'     :  conj_title,
     'conj_desc'    :  conj_desc,
     'rec'          :  res_name,
     'fecha_m'      :  fecha_m,
     'fecha_c'      :  fecha_c,
     'rec_des'      :  res_desc,
     'rec_url'      :  res_url,
     'rec_id'       :  res_id}

## To DataFrame
mat = pd.DataFrame(data = d)

## Save results
mat.to_csv("./data/MAT.csv", encoding = "utf-8", index = False)
