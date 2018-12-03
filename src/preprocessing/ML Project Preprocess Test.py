
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import datetime as dt
from urllib.parse import urlparse


# In[2]:


csv_path = "finalEncodedData.csv"
raw_df = pd.read_csv(csv_path,dtype={'fullVisitorId': 'str'})


# In[ ]:


excludeList = ['date_year','date_month','date_day','visitStartTime_year','visitStartTime_month','visitStartTime_day','isEntryExitSame','visitStartTime_hour']
train_columns = raw_df.columns.values.tolist()
final_columns = []
for column in train_columns:
    if column not in excludeList:
        final_columns.append(column)
final_columns.append("date")
final_columns.append("visitStartTime")


# In[129]:


#for sheet 0 - solve inconsistent columns
i = 0
test_csv_path = "flatten_test_"+str(i)+".csv"
test_raw_df = pd.read_csv(test_csv_path,dtype={'fullVisitorId': 'str'})
test_raw_df["hits_latencyTracking.serverConnectionTime"] = np.nan
test_raw_df["hits_latencyTracking.domainLookupTime"] = np.nan
test_raw_df["hits_latencyTracking.redirectionTime"] = np.nan
test_df = test_raw_df[final_columns]
test_df.to_csv("correctColumns_"+str(i)+".csv",index=False)


# In[195]:


#for sheet 1,2,3,7,11,12,14,15 - solve inconsistent columns
sheets = [1,2,3,7,11,12,14,15]
for i in sheets:
    test_csv_path = "flatten_test_"+str(i)+".csv"
    test_raw_df = pd.read_csv(test_csv_path,dtype={'fullVisitorId': 'str'})
    test_df = test_raw_df[final_columns]
    test_df.to_csv("correctColumns_"+str(i)+".csv",index=False)


# In[145]:


#for sheet 4 - solve inconsistent columns
i = 4
test_csv_path = "flatten_test_"+str(i)+".csv"
test_raw_df = pd.read_csv(test_csv_path,dtype={'fullVisitorId': 'str'})
test_raw_df['hits_eCommerceAction.option'] = np.nan
test_raw_df["hits_latencyTracking.redirectionTime"] = np.nan
test_df = test_raw_df[final_columns]
test_df.to_csv("correctColumns_"+str(i)+".csv",index=False)


# In[150]:


#for sheet 5 - solve inconsistent columns
i = 5
test_csv_path = "flatten_test_"+str(i)+".csv"
test_raw_df = pd.read_csv(test_csv_path,dtype={'fullVisitorId': 'str'})
test_raw_df["hits_latencyTracking.domainLookupTime"] = np.nan
test_df = test_raw_df[final_columns]
test_df.to_csv("correctColumns_"+str(i)+".csv",index=False)


# In[155]:


#for sheet 6 - solve inconsistent columns
i = 6
test_csv_path = "flatten_test_"+str(i)+".csv"
test_raw_df = pd.read_csv(test_csv_path,dtype={'fullVisitorId': 'str'})
test_raw_df["hits_latencyTracking.serverConnectionTime"] = np.nan
test_df.to_csv("correctColumns_"+str(i)+".csv",index=False)


# In[164]:


#for sheet 8 - solve inconsistent columns
i = 8
test_csv_path = "flatten_test_"+str(i)+".csv"
test_raw_df = pd.read_csv(test_csv_path,dtype={'fullVisitorId': 'str'})
test_raw_df["hits_latencyTracking.serverConnectionTime"] = np.nan
test_raw_df["hits_latencyTracking.domainLookupTime"] = np.nan
test_df = test_raw_df[final_columns]
test_df.to_csv("correctColumns_"+str(i)+".csv",index=False)


# In[169]:


#for sheet 9 - solve inconsistent columns
i = 9
test_csv_path = "flatten_test_"+str(i)+".csv"
test_raw_df = pd.read_csv(test_csv_path,dtype={'fullVisitorId': 'str'})
test_raw_df["hits_latencyTracking.serverConnectionTime"] = np.nan
test_raw_df["hits_latencyTracking.domainLookupTime"] = np.nan
test_raw_df["hits_latencyTracking.redirectionTime"] = np.nan
test_raw_df["hits_latencyTracking.serverResponseTime"] = np.nan
test_df = test_raw_df[final_columns]
test_df.to_csv("correctColumns_"+str(i)+".csv",index=False)


# In[187]:


#for sheet 10,13 - solve inconsistent columns
sheets = [10,13]
for i in sheets:
    test_csv_path = "flatten_test_"+str(i)+".csv"
    test_raw_df = pd.read_csv(test_csv_path,dtype={'fullVisitorId': 'str'})
    test_raw_df['hits_eCommerceAction.option'] = np.nan
    test_df = test_raw_df[final_columns]
    test_df.to_csv("correctColumns_"+str(i)+".csv",index=False)


# In[196]:


#check whether all chunks have same shape
for i in range(0,16):
    test_csv_path = "correctColumns_"+str(i)+".csv"
    test_df = pd.read_csv(test_csv_path,dtype={'fullVisitorId': 'str'})
    print(test_df.shape)


# In[ ]:


#function to handle NaN and mixed types
def correctNanAndMixedTypes(test_df):
    na_vals = ['unknown.unknown', '(not set)', 'not available in demo dataset',
                   '(not provided)', '(none)', '<NA>']

    test_df = test_df.replace(na_vals, np.nan, regex=True)
    for column in test_df.columns:
        if test_df[column].dtype == np.int64 : 
            test_df[column].fillna(0, inplace=True)
        elif test_df[column].dtype == np.float64 : 
            test_df[column].fillna(0.0, inplace=True)
        elif test_df[column].dtype == np.bool : 
            test_df[column].fillna(False, inplace=True)
        else:
            test_df[column].fillna("Unknown", inplace=True)
    #replace USD with nan and fill nan for visitNumber field
    na_vals = ['USD']
    test_df.visitNumber.replace(na_vals, np.nan, inplace=True)
    test_df.visitNumber.fillna(0, inplace=True)
    #replace No with nan and fill nan for date field
    na_vals = ['No']
    test_df.date.replace(na_vals, np.nan, inplace=True)
    test_df.date.fillna("Unknown", inplace=True)
    #read them in read_csv
    mixedColumnsToNumeric = ['visitNumber']
    for column in mixedColumnsToNumeric:
        test_df[column] = pd.to_numeric(test_df[column])
    save_csv_path = "noMixed_part_"+str(i)+".csv"
    test_df.to_csv(save_csv_path,index=False)


# In[ ]:


for i in range(0,16):
    test_csv_path = "correctColumns_"+str(i)+".csv"
    test_df = pd.read_csv(test_csv_path,dtype={'fullVisitorId': 'str'})
    correctNanAndMixedTypes(test_df)


# In[ ]:


#concatenate chunks into single part
concat_df = pd.read_csv("noMixed_part_"+str(0)+".csv",
                           dtype={'fullVisitorId': 'str',
                                  'date':'str',
                                  'visitStartTime':'str',
                                  'device_isMobile':'str',
                                  'hits_exceptionInfo.isFatal':'str',
                                  'hits_isInteraction':'str',
                                  'hits_isEntrance':'str',
                                  'hits_isExit':'str'
                                 })
for i in range(1,16):
    test_df = pd.read_csv("noMixed_part_"+str(i)+".csv",
                           dtype={'fullVisitorId': 'str',
                                  'date':'str',
                                  'visitStartTime':'str',
                                  'device_isMobile':'str',
                                  'hits_exceptionInfo.isFatal':'str',
                                  'hits_isInteraction':'str',
                                  'hits_isEntrance':'str',
                                  'hits_isExit':'str'
                                 })
    concat_df = pd.concat([concat_df, test_df], ignore_index=True)
concat_df.to_csv("wholeTest.csv",index=False)


# In[ ]:


df = pd.read_csv("wholeTest.csv",
                           dtype={'fullVisitorId': 'str',
                                  'date':'str',
                                  'visitStartTime':'str',
                                  'device_isMobile':'str',
                                  'hits_exceptionInfo.isFatal':'str',
                                  'hits_isInteraction':'str',
                                  'hits_isEntrance':'str',
                                  'hits_isExit':'str',
                                  'hits_eCommerceAction.option':'str'
                                 })


# In[ ]:


def correctOption(value):
    if value == '0.0':
        return 'Unknown'
    else:
        return value


# In[ ]:


#correct mixed types in hits_eCommerceAction.option
df['hits_eCommerceAction.option'] = df['hits_eCommerceAction.option'].apply(correctOption)
df.to_csv("whole_corrected.csv",index=False)


# In[197]:


#function to encode category columns
def preprocess(X,labelColumn,nonCategoryColumns):
        nonNullData = X
        dataWithoutClass = nonNullData.iloc[:,nonNullData.columns != labelColumn ]
        classDf = nonNullData.iloc[:, nonNullData.columns==labelColumn]       
        
        stringColumnsIncl = dataWithoutClass.select_dtypes(exclude=['number','bool']).columns 
        stringColumns = []
        for column in stringColumnsIncl:
            if column not in nonCategoryColumns:
                stringColumns.append(column)
        numericColumns = dataWithoutClass.select_dtypes(include=['number','bool']).columns  
        labeledData = nonNullData
        labeledDataWithoutClass = dataWithoutClass
       
        if(len(stringColumns)!=0):
            if(len(stringColumns)==len(dataWithoutClass.columns)):                
                labeledDataWithoutClass = dataWithoutClass.apply(preprocessing.LabelEncoder().fit_transform)
            else:
                labeledDataWithoutClass = pd.concat([dataWithoutClass[numericColumns],dataWithoutClass[nonCategoryColumns],dataWithoutClass[stringColumns].apply(preprocessing.LabelEncoder().fit_transform)],axis=1)
        
   
        labeledData = pd.concat([labeledDataWithoutClass,nonNullData.iloc[:, nonNullData.columns==labelColumn]],axis=1)
        
        return labeledData


# In[ ]:


#encode category columns
test_df = pd.read_csv("whole_corrected.csv",
                           dtype={'fullVisitorId': 'str',
                                  'date':'str',
                                  'visitStartTime':'str',
                                  'device_isMobile':'str',
                                  'hits_exceptionInfo.isFatal':'str',
                                  'hits_isInteraction':'str',
                                  'hits_isEntrance':'str',
                                  'hits_isExit':'str'
                                 })
labelColumn = "totals_transactionRevenue"
nonCategoryColumns = ["date","fullVisitorId","geoNetwork_networkDomain","hits_appInfo.exitScreenName","hits_appInfo.landingScreenName","hits_eventInfo.eventLabel","hits_page.pageTitle","hits_referer","trafficSource_adContent","trafficSource_campaign","trafficSource_keyword","visitStartTime"]
test_df = preprocess(test_df,labelColumn,nonCategoryColumns)


# In[ ]:


#process date field

def processDate(date):
    if date.lower() == 'unknown':
        return dt.datetime.now()
    else:
        return dt.datetime.strptime(str(date), '%Y%m%d')
test_df["date_datetime"] = test_df['date'].apply(processDate)
test_df = test_df.dropna()
test_df['date_year'] = test_df['date_datetime'].dt.year
test_df['date_month'] = test_df['date_datetime'].dt.month
test_df['date_day'] = test_df['date_datetime'].dt.day


# In[ ]:


#process visitStartTime field

def convertPosixToDate(epoch):   
    if(epoch.isdigit()):
        return dt.datetime.utcfromtimestamp(int(epoch))
    else:
        return np.nan
    
def categorizeHour(hour):
    if hour >= 0.0 and hour < 4.0:
        return "midnight"
    if hour >= 4.0 and hour < 6.0:
        return "earlyMorning"
    if hour >= 6.0 and hour < 12.0:
        return "morning"
    if hour >= 12.0 and hour < 16.0:
        return "afternoon"
    if hour >= 16.0 and hour < 19.0:
        return "evening"
    if hour >= 19.0 and hour < 0.0:
        return "night"

test_df['visitStartTime_date'] = test_df['visitStartTime'].apply(convertPosixToDate)
test_df = test_df.dropna()
test_df['visitStartTime_year'] = test_df['visitStartTime_date'].dt.year
test_df['visitStartTime_month'] = test_df['visitStartTime_date'].dt.month
test_df['visitStartTime_day'] = test_df['visitStartTime_date'].dt.day
test_df['visitStartTime_hour'] = test_df['visitStartTime_date'].dt.hour


    
test_df["visitStartTime_hour"] = test_df['visitStartTime_hour'].apply(categorizeHour)


# In[ ]:


#drop the date columns that we processed
columnsToDrop = ["visitStartTime","visitStartTime_date","date","date_datetime"]
test_df = test_df.drop(columnsToDrop,axis = 1)


# In[ ]:


#we are interested only in the host name
def hostName(url):
    return urlparse(url).hostname
test_df['hits_referer'] = test_df['hits_referer'].apply(hostName)


# In[ ]:


#check whether the landing page is the same as exit page
test_df["isEntryExitSame"] = test_df["hits_appInfo.landingScreenName"] == test_df["hits_appInfo.exitScreenName"]


# In[ ]:


for column in test_df.columns:
    if test_df[column].dtype == np.int64 : 
        test_df[column].fillna(0, inplace=False)
    elif test_df[column].dtype == np.float64 : 
        test_df[column].fillna(0.0, inplace=False)
    elif test_df[column].dtype == np.bool : 
        test_df[column].fillna(False, inplace=False)
    else:
        test_df[column].fillna("Unknown", inplace=True)


# In[ ]:


#encode category data
labelColumn = "totals_transactionRevenue"
nonCategoryColumns = ["fullVisitorId"]
label_df = preprocess(test_df,labelColumn,nonCategoryColumns)
label_df.to_csv("finalEncodedTestData.csv",index=False)

