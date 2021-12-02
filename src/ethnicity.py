import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import cleanPopulation
import cleanDeath
import util
import json

def processCounting(data, consider=['Asian', 'Black', 'Hispanic', 'White']):
    """
    Filter data based on consider
    :param: data, consider 
    :type: DataFrame, list
    :returns: DataFrame
    """
    small = data[data['Strata_Name'].isin(consider)]
    data = small.append({'Strata_Name': 'Other', 'Count': data['Count'].sum()-small['Count'].sum()} , ignore_index=True)
    return data


def includeCounty(csvFile='../data/death.csv'):
    """
    Read death dataset and return processed data
    :param: csvFile
    :type: str
    :returns: DataFrame
    """
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    df = pd.read_csv(csvFile)
    grp = df.groupby(['Year', 'Strata', 'Strata_Name', 'Cause_Desc'])
    data = grp.sum()
    data = data.iloc[:, :-1]
    data = data.reset_index()
    data.Count = data.Count.astype(int)
    return data

def barPlotData(considerGroup = ['Black', 'White', 'Hispanic', 'Asian'], considerDisease = ['Assault (homicide)', 'Alzheimer\'s disease', 'Malignant neoplasms', 'Intentional self-harm (suicide)', 'Diseases of heart']):
    """
    Plot barchart of diseases
    :param: csvFile, 
    :type: str
    :returns: DataFrame
    """
    countyLabel = ['California', 'San Diego', 'Los Angeles']
    raceLabel, caData = getCalData(considerGroup, considerDisease)
    sdData = getCountyData(considerGroup, considerDisease)
    laData = getCountyData(considerGroup, considerDisease, 'Los Angeles')
    json.dump(caData, open("../data/CARace.txt", 'w'))
    json.dump(sdData, open("../data/SDRace.txt", 'w'))
    json.dump(laData, open("../data/LARace.txt", 'w'))
    
    data = [caData, sdData, laData]
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rc('font', size=13)
    for disease in considerDisease:
        X = np.arange(len(countyLabel))
        maxx = 0
        for i in range(len(raceLabel)):
            plotdata = []
            for j in range(len(data)):
                maxx = max(maxx, data[j][disease][i])
                plotdata.append(data[j][disease][i])
            plt.bar(X+0.15*i, plotdata, width=0.15)
        plt.ylabel('Percentages')
        plt.legend(labels=raceLabel)
        plt.title(disease)
        plt.ylim(0, maxx*1.5)
        plt.xticks(np.arange(len(countyLabel))+0.25, countyLabel)
        plt.show()

        

def getCalData(considerGroup, considerDisease):
    """
    Filter data in California based on considerGroup and cnsiderDisease
    :param: considerGroup, considerDisease
    :type: list, list
    :returns: (list, dict)
    """
    ans = defaultdict(list)
    data = includeCounty().groupby('Strata').get_group('Race-Ethnicity').drop(columns=['Strata', 'Year']).groupby(['Strata_Name', 'Cause_Desc']).sum().reset_index()
    race = []
    for name, group in data.groupby('Strata_Name'):
        if name in considerGroup:
            allNum = group.set_index('Cause_Desc')['Count']['All causes (total)']
            race.append(name)
            for index, row in group.iterrows():
                if row['Cause_Desc'] in considerDisease:
                    ans[row['Cause_Desc']].append(row['Count']*100/allNum)
    return (race, ans)

def getCountyData(considerGroup, considerDisease, county='San Diego'):
    """
    Return a dict of data
    :param: considerGroup, considerDisease
    :type: list, list
    :returns: dict
    """
    ans = defaultdict(list)
    df = pd.read_csv('../data/death.csv')
    data = df.groupby(['County']).get_group(county)
    data = data.groupby('Strata').get_group('Race-Ethnicity').set_index('Strata_Name').drop(columns=['Annotation_Code', 'Year', 'Geography_Type', 'Cause', 'Annotation_Desc', 'Strata'])
    data = data.groupby(['Strata_Name', 'Cause_Desc']).sum().reset_index()
    data.Count = data.Count.astype(int)
    for name, group in data.groupby('Strata_Name'):
        if name in considerGroup:
            allNum = group.set_index('Cause_Desc')['Count']['All causes (total)']
            for index, row in group.iterrows():
                if row['Cause_Desc'] in considerDisease:
                    ans[row['Cause_Desc']].append(row['Count']*100/allNum)
    return ans



def CAComposition():
    """
    Plot death composition of California
    """
    # Read data
    data = cleanDeath.combineCounty()
    # Clean data
    data = data.groupby('Strata').get_group('Race-Ethnicity')
    data = data.set_index('Strata_Name')
    data = data.drop(columns=['Strata', 'Unnamed: 0', 'Year'])
    counting = data.groupby(['Strata_Name']).sum().reset_index()
    counting = processCounting(counting)
    counting.to_csv('../data/CAComposition.csv')
    # Plot data
    util.plotPie(counting['Count'], counting['Strata_Name'], title='California')

def countyComposition(county='San Diego'):
    """
    Plot death composition of specific county in California
    """
    # Read data
    csvFile='../data/death.csv'
    #Clean data
    df = pd.read_csv(csvFile)
    data = df.groupby(['County']).get_group(county).groupby('Strata').get_group('Race-Ethnicity').set_index('Strata_Name')
    data = data.drop(columns=['Annotation_Code', 'Year', 'Geography_Type', 'Cause', 'Annotation_Desc', 'Strata'])
    counting = data.groupby(['Strata_Name']).sum().reset_index()
    counting.Count = counting.Count.astype(int)
    counting = processCounting(counting)
    counting.to_csv('../data/' + county + 'Composition.csv')
    #Plot data
    util.plotPie(counting['Count'], counting['Strata_Name'], title=county)

            

if __name__ == '__main__':
    CAComposition()
    countyComposition()
    barPlotData()