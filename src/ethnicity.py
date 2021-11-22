import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import cleanPopulation
import cleanDeath


def plotPie(data, title):
    """
    Using
    """
    plt.pie(data['Count'], autopct='%1.1f%%', labels=data['Cause_Desc'])
    plt.title(title)
    plt.rc('font', size=16)
    plt.show()
    # if '/' in title:
    #     strr = ""
    #     for i in title.split('/'):
    #         strr += i+' '
    #     plt.savefig(strr[:-1]+'.png')
    # else:
    #     plt.savefig(title+'.png')
    # plt.close()


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
        temp = counting.iloc[-1].copy()
        counting.iloc[-1] = counting.iloc[-2]
        counting.iloc[-2] = temp
        temp = counting.iloc[0].copy()
        counting.iloc[0] = counting.iloc[1]
        counting.iloc[1] = temp
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
        temp = counting.iloc[-1].copy()
        counting.iloc[-1] = counting.iloc[-2]
        counting.iloc[-2] = temp
        temp = counting.iloc[0].copy()
        counting.iloc[0] = counting.iloc[1]
        counting.iloc[1] = temp
        print(counting)
        plt.rc('font', size=16)
        plt.pie(counting['Count'], autopct='%1.1f%%', labels=counting['Strata_Name'])
        plt.show()
    data = data.groupby(['Strata_Name', 'Cause_Desc']).sum().reset_index()

    #Plot causes pie chart
    if plot:
        for name, group in data.groupby('Strata_Name'):
            plotPie(group, name)


if __name__ == '__main__':
    cleanEthniciyData(plot = True)
    cleanEthnicityDataByCounty(plot = True)