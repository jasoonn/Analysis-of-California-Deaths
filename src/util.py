import matplotlib.pyplot as plt
import pandas as pd

def plotPie(data, label, title=None, fontSize=16):
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

def swtichColumn(data, i ,j):
    """Switch two specific columns in pandas
    :param: data, i, j
    :type: DataFrame, int, int
    :returns: None
    """
    temp = data.iloc[i].copy()
    data.iloc[i] = data.iloc[j]
    data.iloc[j] = temp

if __name__ == '__main__':
    vals = [2, 4, 6]
    title = ["two", "four", "six"]
    plotPie(vals, title, "testing")