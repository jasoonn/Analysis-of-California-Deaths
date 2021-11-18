import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import cleanPopulation

def combineCounty(csvFile='../data/death.csv', outputFile='../data/deathCombine.csv'):
    """
    Read death dataset and return county-combined data
    csv_file: path to csv file (dataset)
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
        data = data.iloc[:, :-1]
        data = data.reset_index()
        data.Count = data.Count.astype(int)
        for index, row in data.iterrows():
            if(row['Strata'] != 'Age' and row['Strata'] != 'Place Type'):
                if(row['Cause_Desc'] == 'All causes (total)'):
                    data = data.drop(index)
        data.to_csv(outputFile)
        return data
    
def separateData(outputFile, strata_name, cols, csvFile='../data/deathCombine.csv'):
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    if os.path.exists(outputFile):
        data = pd.read_csv(outputFile)
        return data
    else:
        df = pd.read_csv(csvFile)
        data = df.loc[df['Strata'] == strata_name, cols]
        index = data.set_index(cols[:3])[cols[3]]
        data = index.unstack()
        data = data.rename_axis(columns=None)
        data = data.reset_index()
        data.to_csv(outputFile)
        return data
    
def cleanAgeData(csvFile = '../data/CauseDesc_Year_Age.csv', outputFile = '../data/CauseDesc_Year_Age_Cleaned.csv'):
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    if os.path.exists(outputFile):
        data = pd.read_csv(outputFile)
        return data
    else:
        data = pd.read_csv(csvFile)
        for i in range(6):
            x = data.loc[(data['Strata_Name'] == 'Under 1 year') & (data['Year'] == i+2014), 'All causes (total)'].iloc[0]
            y = data.loc[(data['Strata_Name'] == '1-4 years') & (data['Year'] == i+2014), 'All causes (total)'].iloc[0]
            data.loc[(data['Strata_Name'] == '1-4 years') & (data['Year'] == i+2014), 'All causes (total)'] = int(x + y)
            s = data.loc[(data['Strata_Name'] == '5-14 years') & (data['Year'] == i+2014), 'All causes (total)'].iloc[0]
            t = data.loc[(data['Strata_Name'] == '15-24 years') & (data['Year'] == i+2014), 'All causes (total)'].iloc[0]
            data.loc[(data['Strata_Name'] == '5-14 years') & (data['Year'] == i+2014), 'All causes (total)'] = int(s + t)
            u = data.loc[(data['Strata_Name'] == '75-84 years') & (data['Year'] == i+2014), 'All causes (total)'].iloc[0]
            v = data.loc[(data['Strata_Name'] == '85 years and over') & (data['Year'] == i+2014), 'All causes (total)'].iloc[0]
            data.loc[(data['Strata_Name'] == '75-84 years') & (data['Year'] == i+2014), 'All causes (total)'] = int(u + v)
        data.loc[data['Strata_Name'] == '1-4 years', 'Strata_Name'] = 'Under 5 years'
        data.loc[data['Strata_Name'] == '5-14 years', 'Strata_Name'] = '5-24 years'
        data.loc[data['Strata_Name'] == '75-84 years', 'Strata_Name'] = '75 years and over'
        data = data.drop(data[data['Strata_Name'] == 'Under 1 year'].index)
        data = data.drop(data[data['Strata_Name'] == '15-24 years'].index)
        data = data.drop(data[data['Strata_Name'] == '85 years and over'].index)
        data.to_csv(outputFile)
        return data

if __name__ == '__main__':
    # combineCounty()
    # 'change this to get different subdataset'
    # strata_name = 'Race-Ethnicity'
    # outputFile = '../data/CauseDesc_Year_' + strata_name + '.csv'
    # cols = ['Strata_Name', 'Year', 'Cause_Desc', 'Count']
    # separateData(outputFile, strata_name, cols)
    # cleanAgeData()
    pass