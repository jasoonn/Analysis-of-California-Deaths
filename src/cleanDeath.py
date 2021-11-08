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
        data.to_csv(outputFile)
        return data

def plotAgeData():
    """
    Plot death according to age
    """
    data = combineCounty()
    data = data.groupby('Strata').get_group('Age')
    data = data.set_index('Strata_Name')
    data = data.drop(columns=['Strata', 'Cause_Desc', 'Unnamed: 0'])
    changeName = {'1-4 years': 'Under 5 years', 'Under 1 year': 'Under 5 years', '15-24 years': '5-24 years', '5-14 years': '5-24 years', '75-84 years': '75 years and over', '85 years and over': '75 years and over'}
    dicts = {}
    for index, row in data.iterrows():
        if index in changeName:
            index = changeName[index]
        if index not in dicts:
            dicts[index] = defaultdict(int)
        dicts[index][row[0]] += row[1]
    print(data)
    def plotPieData(dicts, year=2019, normalize = False): 
        if not normalize:
            plt.pie([dicts[i][year] for i in dicts], labels=[i for i in dicts], autopct='%1.1f%%')
            plt.title(str(year)+' Non-normalized age pie chart')
            plt.show()
        else:
            data = cleanPopulation.cleanAgeData()
            plt.pie([dicts[i][year]*100/data[i][str(year)] for i in dicts], labels=[i for i in dicts], autopct='%1.1f%%')
            plt.title(str(year)+' Normalized age pie chart')
            plt.legend()
            plt.show()
    plotPieData(dicts)
    plotPieData(dicts, normalize=True)
    

if __name__ == '__main__':
    #print(combineCounty())
    plotAgeData()