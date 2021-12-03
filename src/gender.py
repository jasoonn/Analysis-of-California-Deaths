#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')
from bokeh.plotting import show, output_file



# In[2]:


typename = 'Occurrence'
strata_name = 'Gender'
csvFile = '../data/' + typename + '/San Diego_causeDesc_year_' + strata_name + '.csv'
df = pd.read_csv(csvFile)
df


# In[9]:


grp1 = df.groupby('Strata_Name').get_group('Male')
deathdata1 = hv.Dataset(data=grp1, kdims=['Cause_Desc', 'Year'])
opts.defaults(
    opts.HeatMap(title = 'Number of Deaths for Male in San Diego', ylabel= 'Cause of Death', fontsize={'title': '14pt', 'ticks':'11pt', 'xlabel':'15pt', 'ylabel' :'15pt'},cmap='Reds', colorbar=True,width=1000,height=600,xrotation=0,tools=['hover']))
output_file('test.html')
show(hv.render(deathdata1.to(hv.HeatMap,['Year','Cause_Desc'],'Count')))


# In[10]:


grp2 = df.groupby('Strata_Name').get_group('Female')
deathdata2 = hv.Dataset(data=grp2, kdims=['Cause_Desc', 'Year'])
opts.defaults(
    opts.HeatMap(title = 'Number of Deaths for Female in San Diego', ylabel= 'Cause of Death', fontsize={'title': '14pt', 'ticks':'11pt', 'xlabel':'15pt', 'ylabel' :'15pt'},cmap='Reds', colorbar=True,width=1000,height=600,xrotation=0,tools=['hover']))
output_file('test.html')
show(hv.render(deathdata2.to(hv.HeatMap,['Year','Cause_Desc'],'Count')))


# In[12]:


csvFile = '../data/' + typename + '/San Diego_causeDesc_year_' + strata_name + '_substracted.csv'
df_sub = pd.read_csv(csvFile)
df_sub


# In[13]:


deathdata_sub = hv.Dataset(data=df_sub, kdims=['Cause_Desc', 'Year'])
opts.defaults(
    opts.HeatMap(title = 'Difference of Number of Deaths in San Diego', ylabel= 'Cause of Death', fontsize={'title': '14pt', 'ticks':'11pt', 'xlabel':'15pt', 'ylabel' :'15pt'},cmap='bwr', colorbar=True,width=1000,height=600,xrotation=0,tools=['hover']))
output_file('test.html')
show(hv.render(deathdata_sub.to(hv.HeatMap,['Year','Cause_Desc'],'Count')))


# In[7]:


csvFile = '../data/' + typename + '/combined_causeDesc_year_' + strata_name + '.csv'
df_CA = pd.read_csv(csvFile)
df_CA


# In[14]:


grp1_CA = df_CA.groupby('Strata_Name').get_group('Male')
deathdata1_CA = hv.Dataset(data=grp1_CA, kdims=['Cause_Desc', 'Year'])
opts.defaults(
    opts.HeatMap(title = 'Number of Deaths for Male in California', ylabel= 'Cause of Death', fontsize={'title': '14pt', 'ticks':'11pt', 'xlabel':'15pt', 'ylabel' :'15pt'},cmap='Reds', colorbar=True,width=1000,height=600,xrotation=0,tools=['hover']))
output_file('test.html')
show(hv.render(deathdata1_CA.to(hv.HeatMap,['Year','Cause_Desc'],'Count')))


# In[8]:


grp2_CA = df_CA.groupby('Strata_Name').get_group('Female')
deathdata2_CA = hv.Dataset(data=grp2_CA, kdims=['Cause_Desc', 'Year'])
opts.defaults(
    opts.HeatMap(title = 'Number of Deaths for Female in California', ylabel= 'Cause of Death', fontsize={'title': '14pt', 'ticks':'11pt', 'xlabel':'15pt', 'ylabel' :'15pt'},cmap='Reds', colorbar=True,width=1000,height=600,xrotation=0,tools=['hover']))
output_file('test.html')
show(hv.render(deathdata2_CA.to(hv.HeatMap,['Year','Cause_Desc'],'Count')))


# In[15]:


csvFile = '../data/' + typename + '/combined_causeDesc_year_' + strata_name + '_substracted.csv'
df_sub_CA = pd.read_csv(csvFile)
df_sub_CA


# In[16]:


deathdata_sub_CA = hv.Dataset(data=df_sub_CA, kdims=['Cause_Desc', 'Year']) 
opts.defaults(
    opts.HeatMap(title = 'Difference of Number of Deaths in California', ylabel= 'Cause of Death', fontsize={'title': '14pt', 'ticks':'11pt', 'xlabel':'15pt', 'ylabel' :'15pt'}, cmap='bwr', colorbar=True,width=1000,height=600,xrotation=0,tools=['hover']))
output_file('test.html')
show(hv.render(deathdata_sub_CA.to(hv.HeatMap,['Year','Cause_Desc'],'Count')))

