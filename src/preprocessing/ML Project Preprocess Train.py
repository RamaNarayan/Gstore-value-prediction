
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import datetime as dt
from urllib.parse import urlparse


# In[2]:


#drop inconsistent columns across chunks
featuresToDrop = ["hits_transaction.localTransactionRevenue",
                      "hits_transaction.localTransactionShipping",
                      "hits_transaction.localTransactionTax",
                      "hits_transaction.transactionId",
                      "hits_transaction.transactionRevenue",
                      "hits_item.transactionId",
                      "hits_transaction.transactionShipping",
                      "hits_transaction.transactionTax",
                      "hits_transaction.affiliation"]
csvs = [5,7, 11, 12, 13, 14]
for i in csvs:
    train_df = pd.read_csv("flatten_train_part_"+str(i-1)+".csv",dtype={'fullVisitorId': 'str'})
    train_df = train_df.drop(featuresToDrop,axis = 1)
    train_df.to_csv("flatten_train_part_"+str(i-1)+".csv",index = False)


# In[3]:


#drop inconsistent column in chunk1
train_df = pd.read_csv("flatten_train_part_1.csv",dtype={'fullVisitorId': 'str'})
train_df = train_df.drop(["trafficSource_campaignCode"],axis = 1)
train_df.to_csv("flatten_train_part_1.csv",index = False)


# In[4]:


#add missing column in chunk5
train_df = pd.read_csv("flatten_train_part_5.csv",dtype={'fullVisitorId': 'str'})
train_df["hits_latencyTracking.redirectionTime"] = np.nan
train_df.to_csv("flatten_train_part_5.csv",index = False)


# In[5]:


#add missing columns in chunk12
train_df = pd.read_csv("flatten_train_part_12.csv",dtype={'fullVisitorId': 'str'})
train_df["hits_latencyTracking.serverConnectionTime"] = np.nan
train_df["hits_latencyTracking.domainLookupTime"] = np.nan
train_df.to_csv("flatten_train_part_12.csv",index = False)


# In[6]:


#add missing column in chunk13
train_df = pd.read_csv("flatten_train_part_13.csv",dtype={'fullVisitorId': 'str'})
train_df["hits_latencyTracking.domainLookupTime"] = np.nan
train_df.to_csv("flatten_train_part_13.csv",index = False)


# In[13]:


#verify all chunks have same features
for i in range(0,16):
    train_df = pd.read_csv("flatten_train_part_"+str(i)+".csv",dtype={'fullVisitorId': 'str'})
    print(train_df.shape)


# In[39]:


#drop constant columns from all chunks
#drop 'hits_social.socialEngagementType' - has only : and unknown and constant
#drop totals_visits - has only 1.0 and nan
for i in range(0,16):
    train_df = pd.read_csv("flatten_train_part_"+str(i)+".csv",dtype={'fullVisitorId': 'str'})
    na_vals = ['unknown.unknown', '(not set)', 'not available in demo dataset',
               '(not provided)', '(none)', '<NA>']
    train_df = train_df.replace(na_vals, np.nan, regex=True)
    for column in train_df.columns:
        if train_df[column].dtype == np.int64 : 
            train_df[column].fillna(0, inplace=True)
        elif train_df[column].dtype == np.float64 : 
            train_df[column].fillna(0.0, inplace=True)
        elif train_df[column].dtype == np.bool : 
            train_df[column].fillna(False, inplace=True)
        else:
            train_df[column].fillna("Unknown", inplace=True)
    #index column for value. We are interested in value so drop it.
    featuresToDrop = ["customDimensions_index"]
    train_df = train_df.drop(featuresToDrop,axis = 1)
    constant_columns = ['device_browserVersion', 'device_browserSize', 'device_operatingSystemVersion', 'device_mobileDeviceBranding', 'device_mobileDeviceModel', 'device_mobileInputSelector', 'device_mobileDeviceInfo', 'device_mobileDeviceMarketingName', 'device_flashVersion', 'device_language', 'device_screenColors', 'device_screenResolution', 'geoNetwork_cityId', 'geoNetwork_latitude', 'geoNetwork_longitude', 'geoNetwork_networkLocation', 'trafficSource_adwordsClickInfo_criteriaParameters', 'hits_appInfo.screenDepth', 'hits_contentGroup.contentGroup4', 'hits_contentGroup.contentGroup5', 'hits_page.searchCategory', 'hits_time']
    constant_columns.append("totals_visits")
    constant_columns.append("socialEngagementType")
    train_df = train_df.drop(constant_columns,axis = 1)
    train_df.to_csv("preprocess_train_part_"+str(i)+".csv",index = False)


# In[40]:


#resolve mixed types
for i in range(0,16):
    train_df = pd.read_csv("preprocess_train_part_"+str(i)+".csv",
                           dtype={'fullVisitorId': 'str',
                                  'date':'str',
                                  'visitStartTime':'str',
                                  'device_isMobile':'str',
                                  'hits_exceptionInfo.isFatal':'str',
                                  'hits_isInteraction':'str',
                                  'hits_isEntrance':'str',
                                  'hits_isExit':'str'
                                 })
    #replace USD with nan and fill nan for visitNumber field
    na_vals = ['USD']
    train_df.visitNumber.replace(na_vals, np.nan, inplace=True)
    train_df.visitNumber.fillna(0, inplace=True)
    #replace No with nan and fill nan for date field
    na_vals = ['No']
    train_df.date.replace(na_vals, np.nan, inplace=True)
    train_df.date.fillna("Unknown", inplace=True)
    #read them in read_csv
    mixedColumnsToStr = ['date','visitStartTime','device_isMobile','hits_exceptionInfo.isFatal','hits_isInteraction','hits_isEntrance','hits_isExit']
    mixedColumnsToNumeric = ['visitNumber']
    for column in mixedColumnsToNumeric:
        train_df[column] = pd.to_numeric(train_df[column])
    train_df.to_csv("no_mixed_train_part_"+str(i)+".csv",index=False)


# In[42]:


#concatenate chunks into single file
concat_df = pd.read_csv("no_mixed_train_part_"+str(0)+".csv",
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
    train_df = pd.read_csv("no_mixed_train_part_"+str(i)+".csv",
                           dtype={'fullVisitorId': 'str',
                                  'date':'str',
                                  'visitStartTime':'str',
                                  'device_isMobile':'str',
                                  'hits_exceptionInfo.isFatal':'str',
                                  'hits_isInteraction':'str',
                                  'hits_isEntrance':'str',
                                  'hits_isExit':'str'
                                 })
    concat_df = pd.concat([concat_df, train_df], ignore_index=True)
concat_df.to_csv("whole.csv",index=False)


# In[43]:


#function to label encode string features
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


# In[44]:


#encode features
train_df = pd.read_csv("whole.csv",
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
nonCategoryColumns = ["date","fullVisitorId","geoNetwork_networkDomain","hits_appInfo.exitScreenName","hits_appInfo.landingScreenName","hits_appInfo.screenName","hits_eventInfo.eventLabel","hits_page.pagePath","hits_page.pagePathLevel1","hits_page.pagePathLevel2","hits_page.pagePathLevel3","hits_page.pagePathLevel4","hits_page.pageTitle","hits_referer","trafficSource_adContent","trafficSource_adwordsClickInfo_gclId","trafficSource_campaign","trafficSource_keyword","trafficSource_referralPath","visitStartTime"]
train_df = preprocess(train_df,labelColumn,nonCategoryColumns)


# In[45]:


#find correlation

corr_df = train_df.corr()

plt.imshow(corr_df.values)
plt.colorbar()
plt.show()


# In[46]:


#drop correlated columns
correlatedColumnsToDrop = ["hits_contentGroup.previousContentGroup1","hits_contentGroup.previousContentGroup2",
"hits_contentGroup.previousContentGroup3","hits_contentGroup.previousContentGroup4",
"hits_contentGroup.previousContentGroup5","hits_social.socialInteractionNetworkAction",
"hits_contentGroup.contentGroupUniqueViews1","hits_contentGroup.contentGroupUniqueViews2",
"totals_pageviews","trafficSource_adwordsClickInfo_page","trafficSource_adwordsClickInfo_adNetworkType",
"trafficSource_adwordsClickInfo_slot","hits_latencyTracking.domContentLoadedTime","hits_eventInfo.eventAction","hits_type",
"hits_contentGroup.contentGroup2","hits_transaction.currencyCode"]
train_df = train_df.drop(correlatedColumnsToDrop,axis = 1)


# In[47]:


#hits_page.pageTitle gives info about the page which is an aggregation of all pagePaths
#trafficSource_referralPath can be removed asits info is covered in trafficSource_source
#screen name and landing screen name are same
#trafficSource_adwordsClickInfo_gclId - not required as its googleCLickId
manualColumnsToDrop = ["hits_page.pagePath","hits_page.pagePathLevel1","hits_page.pagePathLevel2","hits_page.pagePathLevel3","hits_page.pagePathLevel4","trafficSource_referralPath","hits_appInfo.screenName","trafficSource_adwordsClickInfo_gclId"]
train_df = train_df.drop(manualColumnsToDrop,axis = 1)


# In[48]:


#process date field

def processDate(date):
    if date.lower() == 'unknown':
        return np.nan
    else:
        return dt.datetime.strptime(str(date), '%Y%m%d')
train_df["date_datetime"] = train_df['date'].apply(processDate)
train_df = train_df.dropna()
train_df['date_year'] = train_df['date_datetime'].dt.year
train_df['date_month'] = train_df['date_datetime'].dt.month
train_df['date_day'] = train_df['date_datetime'].dt.day


# In[49]:


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

train_df['visitStartTime_date'] = train_df['visitStartTime'].apply(convertPosixToDate)
train_df = train_df.dropna()
train_df['visitStartTime_year'] = train_df['visitStartTime_date'].dt.year
train_df['visitStartTime_month'] = train_df['visitStartTime_date'].dt.month
train_df['visitStartTime_day'] = train_df['visitStartTime_date'].dt.day
train_df['visitStartTime_hour'] = train_df['visitStartTime_date'].dt.hour


    
train_df["visitStartTime_hour"] = train_df['visitStartTime_hour'].apply(categorizeHour)


# In[50]:


#drop the date columns that we processed
columnsToDrop = ["visitStartTime","visitStartTime_date","date","date_datetime"]
train_df = train_df.drop(columnsToDrop,axis = 1)


# In[51]:


#we are interested only in the host name

def hostName(url):
    return urlparse(url).hostname
train_df['hits_referer'] = train_df['hits_referer'].apply(hostName)


# In[52]:


#check whether the landing page is the same as exit page
train_df["isEntryExitSame"] = train_df["hits_appInfo.landingScreenName"] == train_df["hits_appInfo.exitScreenName"]


# In[53]:


#handle null, nan
for column in train_df.columns:
    if train_df[column].dtype == np.int64 : 
        train_df[column].fillna(0, inplace=False)
    elif train_df[column].dtype == np.float64 : 
        train_df[column].fillna(0.0, inplace=False)
    elif train_df[column].dtype == np.bool : 
        train_df[column].fillna(False, inplace=False)
    else:
        train_df[column].fillna("Unknown", inplace=True)


# In[54]:


#encode category features
labelColumn = "totals_transactionRevenue"
nonCategoryColumns = ["fullVisitorId"]
label_df = preprocess(train_df,labelColumn,nonCategoryColumns)
label_df.to_csv("finalEncodedData.csv",index=False)

