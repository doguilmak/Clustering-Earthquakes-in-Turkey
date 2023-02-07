# -*- coding: utf-8 -*-
"""earthquake_boun.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_dYFaR_ADPK-gQLXwLVaznXtnW1ZsQr_

<h1 align=center><font size = 5>Clustering Earthquakes in Turkey with DBSCAN</font></h1>

<br>

<img src="https://raw.githubusercontent.com/doguilmak/Clustering-Earthquakes-in-Turkey/main/assets/boun_earthquake.jpg" width=1000 height=500 alt="https://github.com/doguilmak/Clustering-Earthquakes-in-Turkey">

<small>Picture Source: <a href="https://github.com/doguilmak/Clustering-Earthquakes-in-Turkey">Doğu İlmak Github</a>

<br>

<h2>Keywords</h2>
<ul>
  <li>Geology</li>
  <li>Earth Science</li>
  <li>Earthquake</li>
  <li>Turkey</li>
  <li>BeautifulSoup</li>
  <li>DBSCAN</li>
</ul>

<br>

<h2>Definition of Earthquake</h2>

<p>An earthquake is the shaking of the surface of the Earth resulting from a sudden release of energy in the Earth's <i>lithosphere</i> that creates <i>seismic waves</i>. People can scale <i>seismic waves</i> as <i>The Richter scale</i>.</p>

<br>

<h2>Definition of the Richter Scale</h2>

<p>The Richter scale —also called the Richter magnitude scale, Richter's magnitude scale, and the <i>Gutenberg–Richter</i> scale—is a measure of the strength of earthquakes, developed by <i>Charles Francis Richter</i> and presented in his landmark <i>1935</i> paper, where he called it the "magnitude scale".This was later revised and renamed the local magnitude scale, denoted as $ML$ or $M_{L}$.</p>

<br>

$$M_{L} = log_{10} A - log_{10} A_{0}(δ) = log_{10} [A/A_{0}(δ)]$$

<br>

<p>$A$ is the maximum excursion of the Wood–Anderson seismograph</p>

<p>The empirical function $A_{0}$ depends only on the epicentral distance of the station, $δ$. In practice, readings from all observing stations are averaged after adjustment with station-specific corrections to obtain the $M_{L}$ value.</p>

<br>

<h2>Kandilli Observatory and Earthquake Research Instıtute (KOERI)</h2>

<p>Kandilli Observatory and Earthquake Research Instıtute (KOERI) determines the location and size of all <i>earthquakes</i> that occur in Turkey and disseminates this information immediately to national and international agencies, scientists, critical facilities, and the general public. <b>This project was created based on data obtained by the Kandilli Observatory and Earthquake Research Institute (KOERI).</b></p>

<h3>Data Link</h3>

You can take a look at original website of <a href='http://www.koeri.boun.edu.tr/scripts/lasteq.asp'>Kandilli Observatory and Earthquake Research Instıtute (KOERI).</a>

<br>

<h2>License</h2>

<p>MIT License</p>

<br>

<h3>Sources</h3>
<ul>
    <li><a href="https://en.wikipedia.org/wiki/Richter_magnitude_scale">Wikipedia</a></li>
    <li><a href="http://www.koeri.boun.edu.tr/scripts/lst6.asp">Kandilli Observatory and Earthquake Research Instıtute (KOERI)</a></li>
</ul>

<br>

<h2>Table of Contents</h2>

<p>The <i>magnitude</i> of the <i>earthquakes</i> has been visualized on the plot and clustered by <i>DBSCAN</i> in Turkey.</p>

<div class="alert alert-block alert-info" style="margin-top: 20px">
<li><a href="https://#import">Import Libraries and Building Functions for Model</a></li>
<li><a href="https://#data_preparation">Dataset Preparation (Data Preprocessing)</a></li>
<li><a href="https://#dbscan">Clustering with DBSCAN</a></li>

<br>

<p>Estimated Time Needed: <strong>20 min</strong></p>

</div>

<br>
<h2 align=center id="import">Import Libraries and Building Functions for Model</h2>
<p>The following are the libraries we are going to use for this lab:</p>
"""

!pip3 install basemap -q

!pip3 install basemap-data-hires -q

import requests
from bs4 import BeautifulSoup
import csv

from datetime import date
from datetime import timedelta
import datetime

import pandas as pd
import numpy as np

from sklearn.cluster import DBSCAN 
import sklearn.utils
from sklearn.preprocessing import StandardScaler

# Commented out IPython magic to ensure Python compatibility.
from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt
from pylab import rcParams
# %matplotlib inline
rcParams['figure.figsize'] = (20, 20)

def split(delimiters, string, maxsplit=0):
    import re
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, string, maxsplit)

"""<br>
<h2 align=center id="data_preparation">Dataset Preparation (Data Preprocessing)</h2>


<p>The data in the Kandilli Observatory and Earthquake Research Institute (KOERI) web page were accessed through the BeautifulSoup library.</p>
"""

URL = "http://www.koeri.boun.edu.tr/scripts/lst9.asp"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

quotes=[]   
table = soup.find('pre') 

for row in table:
  print(row[578:])

"""<p>We should ignore headings:</p>"""

data = row[578:]

"""<p>Now, we need to spesify dates for our dataset.</p>
<p>IMPORTANT! YOU CAN'T SPESIFY DATE EARLIER THAN WEBSITE DATA. If you want to see all the data, you should go to bottom and take the lastest day. For example today is 5th Feb and data from Bogazici can show 1st Feb. You should write 5 to days parameter to list all because it contains 5 day.</p>
"""

today = date.today()
d0 = today.strftime("%Y.%m.%d")
print(d0)

days = 3 #@param {type:"number"}
for x in range(1, days):
    globals()['d%s' % x] = today - timedelta(days = x)
    globals()['d%s' % x] = globals()['d%s' % x].strftime("%Y.%m.%d")

"""Spesify the dates for dataset."""

print(d0, d1, d2)

"""List to dataframe and adding colums"""

date_split = split([d0 ,d1, d2], data)

for i in range(len(date_split)):
  print(date_split[i])

df = pd.DataFrame(date_split)
df.drop(index=0, inplace=True)
df

df_split = df[0].str.split(expand=True)

df_split

df_split = df_split.loc[:, 0: 6]

df_split

"""<p>Our data set don't have any column names. We need to spesify them with the following code block.</p>"""

df_split.columns = ['Saat', 'Enlem', 'Boylam', 'Derinlik', 'MD', 'ML', \
                    'Mw']

"""<p>We should get rid of '-.-' symbol to clear data.</p>"""

df_split['MD'] = df_split['MD'].replace(['-.-'], '')
df_split['Mw'] = df_split['Mw'].replace(['-.-'], '')
df_split['Saat'] = df_split['Saat'].replace([')'], '')

df_split

"""<p>We should drop rows which have more than 3 NaN cells.</p>

"""

df_split.dropna(thresh=3, inplace=True)

df_split[["Enlem", "Boylam", "Derinlik", "MD", "ML", "Mw"]] = df_split[["Enlem", "Boylam", "Derinlik", "MD", "ML", "Mw"]].apply(pd.to_numeric)

"""<h3>Filter Data</h3>"""

df_split[['ML']].idxmax()
df_split.loc[501:502]

df_split[df_split['ML'] >= 5]

"""<br>
<h2 align=center id="dbscan">Clustering with DBSCAN and Visualization</h2>

<p>The matplotlib basemap toolkit is a library for plotting 2D data on maps in Python. Basemap does not do any plotting on it’s own, but provides the facilities to transform coordinates to a map projections.</p>

<p>Approximate coordinates:</p>
"""

date = datetime.datetime.utcnow()

df_split

"""<p>Through our data, we should define edges of the earthquakes.</p>"""

max_lat = df_split['Enlem'].max()
max_lat = max_lat + 1
min_lat = df_split['Enlem'].min()
min_lat = min_lat - 1

max_lon = df_split['Boylam'].max()
max_lon = max_lon + 1
min_lon = df_split['Boylam'].min()
min_lon = min_lon - 1

my_map = Basemap(projection='merc',
            resolution = 'h', area_thresh = 100.0,
            llcrnrlon=min_lon, llcrnrlat=min_lat, #min longitude (llcrnrlon) and latitude (llcrnrlat)
            urcrnrlon=max_lon, urcrnrlat=max_lat) #max longitude (urcrnrlon) and latitude (urcrnrlat)

my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color = 'white', alpha = 0.3)
my_map.shadedrelief()
my_map.nightshade(date)
parallels = np.arange(36, 42, 1) # Turkey coordinates (parallels)
my_map.drawparallels(parallels,labels=[True,True,True,True], color='#A9A9A9')
meridians = np.arange(26, 45, 1) # Turkey coordinates (meridians)
my_map.drawmeridians(meridians,labels=[True,True,True,True], color='#A9A9A9')

xs, ys = my_map(np.asarray(df_split.Boylam), np.asarray(df_split.Enlem))
df_split['xm']= xs.tolist()
df_split['ym'] =ys.tolist()

my_map.shadedrelief()
my_map.drawcoastlines(color='gray')
my_map.drawcountries(color='gray')
my_map.fillcontinents(color = 'white', alpha = 0.1)
my_map.nightshade(date)
parallels = np.arange(36, 42, 1) # Turkey coordinates (parallels)
my_map.drawparallels(parallels,labels=[True,True,True,True], color='#A9A9A9')
meridians = np.arange(26, 45, 1) # Turkey coordinates (meridians)
my_map.drawmeridians(meridians,labels=[True,True,True,True], color='#A9A9A9')

lon = df_split['Boylam']
lat = df_split['Enlem']
mag = df_split['ML']


nx, ny = 20, 20
lon_bins = np.linspace(min_lon, max_lon, nx+1)
lat_bins = np.linspace(min_lat, max_lat, ny+1)

density, _, _ = np.histogram2d(lon, lat, [lon_bins, lat_bins])

a = my_map.imshow(density.T, interpolation='spline36', alpha=0.7, cmap='YlOrBr', vmin=0, vmax=34)

for index, row in df_split.iterrows():
   my_map.plot(row.xm, row.ym, markerfacecolor =([0.7, 0, 0]),  marker='o', markersize= 5, alpha = 0.75)
plt.show()

my_map.shadedrelief()
my_map.drawcoastlines(color='gray')
my_map.drawcountries(color='gray')
my_map.fillcontinents(color = 'white', alpha = 0.1)
my_map.nightshade(date)
parallels = np.arange(36, 42, 1) # Turkey coordinates (parallels)
my_map.drawparallels(parallels,labels=[True,True,True,True], color='#A9A9A9')
meridians = np.arange(26, 45, 1) # Turkey coordinates (meridians)
my_map.drawmeridians(meridians,labels=[True,True,True,True], color='#A9A9A9')

for index, row in df_split.iterrows():
   my_map.plot(row.xm, row.ym, markerfacecolor =([1, 0, 0]),  marker='o', markersize= 5, alpha = 0.75)
plt.show()

"""<h3>Clustering of Stations Based on Their Magnitude</h3>

<p><i>DBSCAN</i> form sklearn library can run <i>DBSCAN</i> clustering from vector array or distance matrix. In our case, we pass it the Numpy array Clus_dataSet to find core samples of high density and expands clusters from them.</p>
"""

sklearn.utils.check_random_state(100)
Clus_dataSet = df_split[['xm', 'ym']]
Clus_dataSet = np.nan_to_num(Clus_dataSet)
Clus_dataSet = StandardScaler().fit_transform(Clus_dataSet)

"""<p>Computing DBSCAN.</p>"""

df_split

db = DBSCAN(eps=0.15, min_samples=10).fit(Clus_dataSet)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
df_split["Clus_Db"]=labels

labels

realClusterNum=len(set(labels)) - (1 if -1 in labels else 0)
clusterNum = len(set(labels))

df_split[["ML", "Clus_Db"]].head(5)

set(labels)

df_split

"""<h4>Visualization of Clusters Based on Location</h4>"""

my_map = Basemap(projection='merc',
            resolution = 'l', area_thresh = 100.0,
            llcrnrlon=min_lon, llcrnrlat=min_lat, #min longitude (llcrnrlon) and latitude (llcrnrlat)
            urcrnrlon=max_lon, urcrnrlat=max_lat) #max longitude (urcrnrlon) and latitude (urcrnrlat)

my_map.shadedrelief()
my_map.drawcoastlines(color='gray')
my_map.drawcountries(color='gray')
my_map.fillcontinents(color = 'white', alpha = 0.1)
my_map.nightshade(date)
parallels = np.arange(36, 42, 1) # Turkey coordinates (parallels)
my_map.drawparallels(parallels,labels=[True,True,True,True], color='#A9A9A9')
meridians = np.arange(26, 45, 1) # Turkey coordinates (meridians)
my_map.drawmeridians(meridians,labels=[True,True,True,True], color='#A9A9A9')

colors = plt.get_cmap('jet')(np.linspace(0.0, 1.0, clusterNum))

for clust_number in set(labels):
    c=(([0.4, 0.4, 0.4]) if clust_number == -1 else colors[np.int(clust_number)])
    clust_set = df_split[df_split.Clus_Db == clust_number]                    
    my_map.scatter(clust_set.xm, clust_set.ym, color=c,  marker='o', s=10, alpha = 0.85)
    if clust_number != -1:
        cenx=np.mean(clust_set.xm) 
        ceny=np.mean(clust_set.ym) 
        plt.text(cenx, ceny, str(clust_number), fontsize=18, color='red')
        print ("Cluster " + str(clust_number)+', Avg Magnitude: '+ str(np.mean(clust_set.ML)))

"""<br>

<h2>Contact Me</h2>
<p>If you have something to say to me please contact me:</p>

<ul>
  <li>Twitter: <a href="https://twitter.com/Doguilmak">Doguilmak</a></li>
  <li>Mail address: doguilmak@gmail.com</li>
</ul>
"""

from datetime import datetime
print(f"Changes have been made to the project on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")