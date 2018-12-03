
# coding: utf-8

# In[ ]:


#import required libraries
import pandas as pd
import numpy as np
#read a column as list instead of string
from ast import literal_eval
from pandas.io.json import json_normalize
import json


# In[ ]:


#split file into 16 chunks
in_pd = pd.read_csv("test_v2.csv", dtype={'fullVisitorId': 'str'})
k = 0
count = 0
for i in range(int(in_pd.shape[0]/16), in_pd.shape[0] + int(in_pd.shape[0]/16) , int(in_pd.shape[0]/16)):
    x = in_pd[k:i]
    x.to_csv("test_part_"+str(count)+".csv", index = False)
    k = i
    count = count + 1


# In[ ]:


#parse json data
def jsonParser(data):
    return json.loads(data)


# In[ ]:


#function to flatten json
def json_flatten(df,column):
    column_flatten = df[column].apply(pd.Series)
    column_flatten = column_flatten.add_prefix(column+"_")
    df = pd.concat([df.drop([column], axis=1), column_flatten], axis=1)
    return df


# In[ ]:


for fileNumber in range(16):
    read_csv_path = "test_part_"+str(fileNumber)+".csv"
    raw_data = pd.read_csv(read_csv_path,dtype={'fullVisitorId': 'str'},
                           converters={"hits": literal_eval,"customDimensions":literal_eval,"device":jsonParser,"geoNetwork":jsonParser,"totals":jsonParser,"trafficSource":jsonParser})

    #flatten json column data and concatenate back
    json_columns = ["device","trafficSource","geoNetwork","totals"]
    json_flatten_data = raw_data
    for column in json_columns:
        raw_data = json_flatten(raw_data,column)

    #flatten nested json columns in adwordsClickInfo
    raw_data = json_flatten(raw_data,'trafficSource_adwordsClickInfo')

    #make empty list as None,None
    raw_data["customDimensions"] = raw_data["customDimensions"].apply(lambda y: [{'index': None, 'value': None}] if len(y)==0 else y)

    #flatten custom dimensions
    column = "customDimensions"
    column_as_df = json_normalize(raw_data[column].str[0])
    column_as_df = column_as_df.add_prefix(column+'_')
    raw_data = raw_data.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)

    #make empty list as None
    raw_data["hits"] = raw_data["hits"].apply(lambda y: [{'hitNumber': None}] if len(y)==0 else y)

    #flatten hits
    column = "hits"
    column_as_df = json_normalize(raw_data[column].str[0])
    column_as_df = column_as_df.add_prefix(column+'_')
    raw_data = raw_data.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)

    #check json blobs still present.
    jsonlist=[]
    for i in range(len(raw_data.columns)):
        if (isinstance(raw_data.iloc[1,i], list) ):
            jsonlist.append( raw_data.columns[i] )


    #remove the json blobs present after flattening hits
    flatten_data = raw_data.drop(jsonlist,axis=1)

    save_csv_path = "flatten_test_"+str(fileNumber)+".csv"
    flatten_data.to_csv(save_csv_path,index = False)
    

