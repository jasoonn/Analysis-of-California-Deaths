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
    

if __name__ == '__main__':
    print(combineCounty())