
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[159]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[160]:

import numpy as np

data=pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
data=data.sort_values(by='Date')


# In[161]:

data['Year'], data['Month-Date'] = zip(*data['Date'].apply(lambda x: (x[:4], x[5:])))
data = data[data['Month-Date'] != '02-29']
data_min = data[(data['Element'] == 'TMIN') & (data['Year'] != '2015')].groupby('Month-Date').aggregate({'Data_Value':np.min})
data_max = data[(data['Element'] == 'TMAX') & (data['Year'] != '2015')].groupby('Month-Date').aggregate({'Data_Value':np.max})

data_min_15 = data[(data['Element'] == 'TMIN') & (data['Year'] == '2015')].groupby('Month-Date').aggregate({'Data_Value':np.min})
data_max_15 = data[(data['Element'] == 'TMAX') & (data['Year'] == '2015')].groupby('Month-Date').aggregate({'Data_Value':np.max})


# In[162]:

broken_05_min =np.where(data_min_15['Data_Value']<data_min['Data_Value'])[0]
broken_05_max =np.where(data_max_15['Data_Value']>data_max['Data_Value'])[0]


# In[163]:

plt.figure(figsize=(50,30))
plt.plot(data_min.values,'b',label='Record Low')
plt.plot(data_max.values,'r',label='Record High')
plt.scatter(broken_05_min,data_min_15.iloc[broken_05_min],s=100,c='grey',label='Broken Low')
plt.scatter(broken_05_max,data_max_15.iloc[broken_05_max],s=100,c='purple',label='Broken High')
plt.gca().fill_between(range(len(data_min)),data_min['Data_Value'],data_max['Data_Value'],facecolor='green',alpha=0.25)
plt.legend(prop={'size':50},loc=2,frameon=False)

plt.title('Record Temperature near Ann Arbor, Michigan, United States from 2005-2014 \n Temperature broken in 2015',fontsize=50)
plt.xlabel('Day of the Year',fontsize=50)
plt.ylabel('Temperature (Tenths of Degrees C)',fontsize=50)
plt.xticks(range(0, len(data_min), 30), data_min.index[range(0, len(data_min), 30)], rotation = '45',fontsize=50)
plt.yticks(fontsize=50)
plt.savefig('hw2.png')


# In[ ]:



