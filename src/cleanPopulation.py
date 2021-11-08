import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from collections import defaultdict

def cleanAgeData(csvFile='../data/CAGroupByAge.csv', writeFile='../data/CAGroupByAge.txt'):
    """
    Read age population dataset and return cleaned data as a dict
    csvFile: path to csv file (dataset)
    writeFile: path to csv file (cleaned dataset)
    :return: dict
    """
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    if os.path.exists(writeFile):
        dicts = json.load(open(writeFile))
        return dicts
    else:
        df = pd.read_csv(csvFile)
        grp = df.groupby(['Age']) 
        data = grp.sum()
        data = data.iloc[:, 2:9]
        changeName = {'18 to 24 Years': '5-24 years', '25 to 34 Years': '25-34 years', '35 to 44 Years': '35-44 years', '45 to 54 Years': '45-54 years', '5 to 17 Years': '5-24 years', '55 to 59 Years': '55-64 years', '60 & 61 Years': '55-64 years', '62 to 64 Years': '55-64 years', '65 to 74 Years': '65-74 years', '75 Years & Over': '75 years and over', 'Under 5 Years': 'Under 5 years'}
        dicts = {}
        for index, row in data.iterrows():
            if changeName[index] not in dicts:
                dicts[changeName[index]] = defaultdict(int)
            for j in range(len(row)):
                dicts[changeName[index]][2013+j] += int(row[j])
        json.dump(dicts, open(writeFile,'w'))
        return dicts

def plotAgeData():
    """
    Visualize age population data according to years
    """
    data = cleanAgeData()
    for i in data:
        plt.plot([j for j in data[i]], [data[i][j] for j in data[i]], label=i, marker='o')
    plt.ylim(0, 2*10**7)
    plt.legend()
    plt.show()

def plotPieAgeData(year='2019'):
    """
    Visualize age population data using pie chart
    """
    data = cleanAgeData()
    assert isinstance(year, str) and year in data['5-24 years'], 'Invalid key'
    plt.pie([data[i][year] for i in data], labels=[i for i in data], autopct='%1.1f%%')
    plt.title(year+' age pie chart')
    plt.show()

def cleanRaceData(csvFile='../data/CAGroupByRace.csv', writeFile='../data/CAGroupByRace.txt'):
    """
    Read race population dataset and return cleaned data as a dict
    csvFile: path to csv file (dataset)
    writeFile: path to csv file (cleaned dataset)
    :return: dict
    """
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    if os.path.exists(writeFile):
        dicts = json.load(open(writeFile))
        return dicts
    else:
        df = pd.read_csv(csvFile)
        grp = df.groupby(['Race'])
        data = grp.sum()
        data = data.iloc[:, 2:9]
        dicts = {}
        for index, row in data.iterrows():
            if index not in dicts:
                dicts[index] = defaultdict(int)
            for j in range(len(row)):
                dicts[index][2013+j] += int(row[j])
        json.dump(dicts, open(writeFile,'w'))
        return dicts

def plotRaceData():
    """
    Visualize race population data
    """
    data = cleanRaceData()
    for i in data:
        plt.plot([j for j in data[i]], [data[i][j] for j in data[i]], label=i, marker='o')
    plt.legend()
    plt.show()

def plotPieRaceData(year='2019'):
    """
    Visualize age population data using pie chart
    """
    data = cleanRaceData()
    assert isinstance(year, str), 'Invalid key'
    plt.pie([data[i][year] for i in data], labels=[i for i in data], autopct='%1.1f%%')
    plt.title(year+' race pie chart')
    plt.show()


if __name__ == '__main__':
    #print('Age Dict', cleanAgeData())
    #print('Race Dict', cleanRaceData())
    #plotAgeData()
    #plotRaceData()
    #plotPieAgeData()
    #plotPieRaceData()
    pass