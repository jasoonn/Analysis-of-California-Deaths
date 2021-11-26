import matplotlib.pyplot as plt

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

if __name__ == '__main__':
    vals = [2, 4, 6]
    title = ["two", "four", "six"]
    plotPie(vals, title, "testing")