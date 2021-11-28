# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 22:19:10 2021

@author: Bian
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import cleanPopulation

def clean(typename, outputFile, csvFile='../data/death.csv'):
    """
    Read death dataset and return cleaned data for each Geography_Type
    csv_file: path to csv file (dataset)
    :return: Dataframe
    """
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    if os.path.exists(outputFile):
        data = pd.read_csv(outputFile)
        return data
    else:
        df = pd.read_csv(csvFile)
        grp = df.groupby('Geography_Type').get_group(typename)
        data = grp.drop(columns=['Geography_Type', 'Annotation_Code', 'Annotation_Desc', 'Cause'])
        data = data.groupby(['Year', 'County', 'Strata', 'Strata_Name', 'Cause_Desc'])
        data = data.sum()
        data = data.reset_index()
        data.Count = data.Count.astype(int)
        data.to_csv(outputFile)
        return data
    
def combineCounty(outputFile, csvFile):
    """
    Read cleaned dataset and return county-combined data for each Geography_Type
    csv_file: path to csv file (cleaned dataset)
    :return: Dataframe
    """
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    if os.path.exists(outputFile):
        data = pd.read_csv(outputFile)
        return data
    else:
        df = pd.read_csv(csvFile)
        grp = df.groupby(['Year', 'Strata', 'Strata_Name', 'Cause_Desc'])
        data = grp.sum()
        data = data.reset_index()
        data = data.drop('Unnamed: 0', 1)
        data.Count = data.Count.astype(int)
        for index, row in data.iterrows():
            if(row['Strata'] != 'Age' and row['Strata'] != 'Place Type'):
                if(row['Cause_Desc'] == 'All causes (total)'):
                    data = data.drop(index)
        data = data.reset_index(drop=True)
        data.to_csv(outputFile)
        return data
    
def selectCounty(outputFile, csvFile):
    """
    Read cleaned dataset and return top10 county data for each Geography_Type
    csv_file: path to csv file (cleaned dataset)
    :return: Dataframe
    """
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    if os.path.exists(outputFile):
        data = pd.read_csv(outputFile)
        return data
    else:
        data = pd.read_csv(csvFile)
        countyDeath = {}
        for index, row in data.iterrows():
            if(row['Strata'] == 'Total Population' and row['Cause_Desc'] == 'All causes (total)'):
                countyDeath[getattr(row,'County')] = getattr(row,'Count')
        # print(len(countyDeath))
        for index, row in data.iterrows():
            if(row['Strata'] != 'Age' and row['Strata'] != 'Place Type'):
                if(row['Cause_Desc'] == 'All causes (total)'):
                    data = data.drop(index)
        data = data.reset_index(drop=True)
        countyDeathOrder = sorted(countyDeath.items(),key=lambda x:x[1],reverse=True)
        topTenCounty = []
        for t in countyDeathOrder[0:10]:
            topTenCounty.append(t[0])
        # print(topTenCounty)
        indexes_to_drop = []
        for index, row in data.iterrows():
            if(row['County'] not in topTenCounty):
                indexes_to_drop.append(index)
        data = data.drop(data.index[indexes_to_drop])
        data = data.reset_index(drop=True)
        data = data.drop('Unnamed: 0', 1)
        data.to_csv(outputFile)
    return data

def selectCertainCounty(county, outputFile, csvFile):
    """
    Read cleaned dataset and return certain county data for each Geography_Type
    csv_file: path to csv file (cleaned dataset)
    :return: Dataframe
    """
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    if os.path.exists(outputFile):
        data = pd.read_csv(outputFile)
        return data
    else:
        data = pd.read_csv(csvFile)
        indexes_to_drop = []
        for index, row in data.iterrows():
            if(row['County'] != county):
                indexes_to_drop.append(index)
        data = data.drop(data.index[indexes_to_drop])
        data = data.reset_index(drop=True)
        data = data.drop('Unnamed: 0', 1)
        data.to_csv(outputFile)
    return data
    
    
# def separateData(outputFile, strata_name, cols, csvFile):
#     assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
#     if os.path.exists(outputFile):
#         data = pd.read_csv(outputFile)
#         return data
#     else:
#         df = pd.read_csv(csvFile)
#         data = df.loc[df['Strata'] == strata_name, cols]
#         index = data.set_index(cols[:len(cols)-1])[cols[len(cols)-1]]
#         data = index.unstack()
#         data = data.rename_axis(columns=None)
#         data = data.reset_index()
#         data.to_csv(outputFile, index=False)
#         return data
    
def separateData_new(strata_name, outputFile, csvFile):
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    if os.path.exists(outputFile):
        data = pd.read_csv(outputFile)
        return data
    else:
        data = pd.read_csv(csvFile)
        indexes_to_drop = []
        for index, row in data.iterrows():
            if(row['Strata'] != strata_name):
                indexes_to_drop.append(index)
        data = data.drop(data.index[indexes_to_drop])
        # data = data.reset_index(drop=True)
        data = data.drop(['Unnamed: 0','Strata'], 1)
        # data.to_csv(outputFile, index=False)
        grp_female = data.groupby('Strata_Name').get_group('Female')
        grp_male = data.groupby('Strata_Name').get_group('Male')
        grp_male.to_csv(outputFile, index=False)
    return data

def substractGender(outputFile, csvFile1, csvFile2):
    assert isinstance(csvFile1, str) and os.path.exists(csvFile1) and isinstance(csvFile2, str) and os.path.exists(csvFile2), 'Invalid path'
    if os.path.exists(outputFile):
        data = pd.read_csv(outputFile)
        return data
    else:
        pd_female = pd.read_csv(csvFile1)
        pd_male = pd.read_csv(csvFile2)
        data = pd_female.copy(deep=True)
        data['Count'] = pd_female['Count'] - pd_male['Count']
        data = data.drop('Strata_Name',1)
        data.to_csv(outputFile)
        return data
    
if __name__ == '__main__':
    typename = 'Occurrence'
    # outputFile_cleaned = '../data/'+ typename + '/death_cleaned.csv'
    # clean(typename, outputFile_cleaned)
    # csvFile_tocombine = '../data/'+ typename + '/death_cleaned.csv'
    # outputFile_combined = '../data/'+ typename + '/death_combined.csv'
    # combineCounty(outputFile_combined, csvFile_tocombine)
    # csvFile_toselect = '../data/'+ typename + '/death_cleaned.csv'
    # outputFile_selected = '../data/'+ typename + '/death_top10county.csv'
    # selectCounty(outputFile_selected,csvFile_toselect)
    # county = 'San Diego'
    # csvFile_toselect = '../data/'+ typename + '/death_top10county.csv'
    # outputFile_singleselected = '../data/'+ typename + '/death_' + county + '.csv'
    # selectCertainCounty(county, outputFile_singleselected, csvFile_toselect)
    strata_name = 'Gender'
    # csvFile_toseperate = '../data/'+ typename + '/death_combined.csv'
    # outputFile = '../data/' + typename + '/combined_causeDesc_year_' + strata_name + '_Male.csv'
    #### cols = ['Strata_Name', 'Year', 'Cause_Desc', 'Count']
    # separateData_new(strata_name, outputFile, csvFile_toseperate)
    csvFile1 = '../data/' + typename + '/combined_causeDesc_year_' + strata_name + '_Female.csv'
    csvFile2 = '../data/' + typename + '/combined_causeDesc_year_' + strata_name + '_Male.csv'
    outputFile_substracted = '../data/' + typename + '/combined_causeDesc_year_' + strata_name + '_substracted.csv'
    substractGender(outputFile_substracted, csvFile1, csvFile2)