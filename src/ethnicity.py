import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import cleanPopulation
import cleanDeath


def plotPiee(data, label, title=None, fontSize=13):
    """Plot piechart from given data and label
    :param: data, label, title
    :type: list, list, str
    :returns: None
    """
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rc('font', size=fontSize)
    plt.title(title)
    plt.pie(data, autopct='%1.1f%%', labels=label)
    plt.show()


def plotPie(data, title):
    """
    Using
    """
    swtichColumn(data, 1, -1)
    swtichColumn(data, 0, 1)
    swtichColumn(data, 4, 10)
    swtichColumn(data, 5, 7)
    plotPiee(data['Count'], data['Cause_Desc'], title)

def swtichColumn(data, i ,j):
    temp = data.iloc[i].copy()
    data.iloc[i] = data.iloc[j]
    data.iloc[j] = temp


def cleanEthnicityDataByCounty(csvFile='../data/death.csv', plot = False, county='San Diego'):
    """
    Clean race data for specific county
    """
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    df = pd.read_csv(csvFile)
    data = df.groupby(['County']).get_group(county)
    data = data.groupby('Strata').get_group('Race-Ethnicity')
    data = data.set_index('Strata_Name')
    data = data.drop(columns=['Annotation_Code', 'Year', 'Geography_Type', 'Cause', 'Annotation_Desc', 'Strata'])
    counting = data.groupby(['Strata_Name']).sum().reset_index()
    counting.Count = counting.Count.astype(int)
    #data = data.drop(columns=['Strata', 'Unnamed: 0', 'Year'])
    
    if plot:
        swtichColumn(counting, -1, -2)
        swtichColumn(counting, 0, 1)
        print(counting)
        plt.rc('font', size=16)
        plt.pie(counting['Count'], autopct='%1.1f%%', labels=counting['Strata_Name'])
        plt.show()

    data = data.groupby(['Strata_Name', 'Cause_Desc']).sum().reset_index()
    data.Count = data.Count.astype(int)

    #Plot causes pie chart
    if plot:
        for name, group in data.groupby('Strata_Name'):
            plotPie(group.reset_index().drop([1]), name)


def includeCounty(csvFile='../data/death.csv', outputFile='../data/deathCombine.csv'):
    """
    Read death dataset and return county-combined data
    csv_file: path to csv file (dataset)
    :return: Dataframe
    """
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    df = pd.read_csv(csvFile)
    grp = df.groupby(['Year', 'Strata', 'Strata_Name', 'Cause_Desc'])
    data = grp.sum()
    data = data.iloc[:, :-1]
    data = data.reset_index()
    data.Count = data.Count.astype(int)
    return data

def filterEthnicityDataByCounty(csvFile='../data/death.csv', plot = False, county='San Diego'):
    """
    Clean race data for specific county
    """
    assert isinstance(csvFile, str) and os.path.exists(csvFile), 'Invalid path'
    df = pd.read_csv(csvFile)
    data = df.groupby(['County']).get_group(county)
    data = data.groupby('Strata').get_group('Race-Ethnicity')
    data = data.set_index('Strata_Name')
    data = data.drop(columns=['Annotation_Code', 'Year', 'Geography_Type', 'Cause', 'Annotation_Desc', 'Strata'])
    data = data.groupby(['Strata_Name', 'Cause_Desc']).sum().reset_index()
    data.Count = data.Count.astype(int)
    considerGroup = ['Black', 'White', 'Hispanic', 'Asian']
    consider = ['Assault (homicide)', 'Alzheimer\'s disease', 'Malignant neoplasms', 'Intentional self-harm (suicide)', 'Diseases of heart']

    #Plot causes pie chart
    if plot:
        tmp = [0]*4
        fig, ((tmp[0], tmp[1]), (tmp[2], tmp[3])) = plt.subplots(2, 2)
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rc('font', size=13)
        count = 0
        for name, group in data.groupby('Strata_Name'):
            if name in considerGroup:
                allNum = group.set_index('Cause_Desc')['Count']['All causes (total)']
                group = group[group['Cause_Desc'].isin(consider)]
                group = group.append({'Strata_Name': name, 'Cause_Desc': 'Other', 'Count': allNum-group['Count'].sum()} , ignore_index=True)
                tmp[count].pie(group['Count'], autopct='%1.1f%%', labels=group['Cause_Desc'])
                tmp[count].set_title(name, fontdict = {"fontfamily": "Times New Roman"})
                count += 1
        fig.suptitle('San Diego', size=20)
        plt.show()


def filterEthniciyData(plot = False):
    """
    Plot death according to age
    """
    data = includeCounty()
    data = data.groupby('Strata').get_group('Race-Ethnicity')
    data = data.set_index('Strata_Name')
    data = data.drop(columns=['Strata', 'Year'])
    #Plot causes pie chart
    data = data.groupby(['Strata_Name', 'Cause_Desc']).sum().reset_index()
    considerGroup = ['Black', 'White', 'Hispanic', 'Asian']
    consider = ['Assault (homicide)', 'Alzheimer\'s disease', 'Malignant neoplasms', 'Intentional self-harm (suicide)', 'Diseases of heart']
    if plot:
        tmp = [0]*4
        fig, ((tmp[0], tmp[1]), (tmp[2], tmp[3])) = plt.subplots(2, 2)
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rc('font', size=13)
        count = 0
        for name, group in data.groupby('Strata_Name'):
            if name in considerGroup:
                allNum = group.set_index('Cause_Desc')['Count']['All causes (total)']
                group = group[group['Cause_Desc'].isin(consider)]
                group = group.append({'Strata_Name': name, 'Cause_Desc': 'Other', 'Count': allNum-group['Count'].sum()} , ignore_index=True)
                tmp[count].pie(group['Count'], autopct='%1.1f%%', labels=group['Cause_Desc'])
                tmp[count].set_title(name, fontdict = {"fontfamily": "Times New Roman"})
                count += 1
        fig.suptitle('California', size=20)
        plt.show()

def cleanEthniciyData(plot = False):
    """
    Plot death according to age
    """
    data = cleanDeath.combineCounty()
    data = data.groupby('Strata').get_group('Race-Ethnicity')
    data = data.set_index('Strata_Name')
    data = data.drop(columns=['Strata', 'Unnamed: 0', 'Year'])

    # Plot death race composition
    counting = data.groupby(['Cause_Desc']).sum()
    counting = data.groupby(['Strata_Name']).sum().reset_index()
    if plot:
        swtichColumn(counting, -1, -2)
        swtichColumn(counting, 0, 1)
        plt.rc('font', size=16)
        plt.pie(counting['Count'], autopct='%1.1f%%', labels=counting['Strata_Name'])
        plt.show()

    #Plot causes pie chart
    data = data.groupby(['Strata_Name', 'Cause_Desc']).sum().reset_index()
    if plot:
        for name, group in data.groupby('Strata_Name'):
            plotPie(group, name)
            

if __name__ == '__main__':
    cleanEthniciyData(plot = False)
    cleanEthnicityDataByCounty(plot = False)
    filterEthniciyData(plot = False)
    filterEthnicityDataByCounty(plot = True)