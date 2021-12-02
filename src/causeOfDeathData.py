import pandas as pd
import matplotlib.pyplot as plt
import os

# Causes of death over the period of 2014-2019

def cleanData(df):
    assert isinstance(df, pd.DataFrame)
    clean_df = df[df["Count"].notna()]
    clean_df = clean_df[["Year", "County", "Strata", "Strata_Name", "Cause", "Cause_Desc","Count"]]
    return clean_df

def causeOfDeath(inputFile='data/death.csv'):
    assert isinstance(inputFile, str) and os.path.exists(inputFile)
    
    data = pd.read_csv(inputFile)
    c_df = cleanData(data)
    print(c_df["Cause_Desc"].unique())
    
    f = {
        'Cause_Desc' : 'unique',
        'Count' : 'sum'
    }
    
    c_df = c_df.groupby(['Year','Cause', "Strata"]).agg(f).reset_index()
    c_df.set_index("Year")
    c_df = c_df[c_df["Cause"] != "ALL"]
    c_df = c_df[c_df["Strata"] == "Total Population"]
    
    return c_df

def plot_and_save_clause(df, causes=[]):
    fig = plt.figure()
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rc('font', size=8)
    
    all_causes = df["Cause"].unique()
    final_save_string = ""
    if not causes:
        causes = all_causes
    else:
        for c in causes:
            final_save_string += "_"
            final_save_string += c
            if c not in all_causes:
                raise Exception(f"{c} is not in the list of causes")
            
    for cause in causes:
        print(df[df["Cause"] == cause])
        to_plot = df[df["Cause"] == cause]
        to_plot.reset_index()
        plt.plot(to_plot["Year"], to_plot["Count"], label=cause, marker='o')
        plt.text(to_plot["Year"].iloc[-1], to_plot["Count"].iloc[-1], f'{cause}')

    plt.legend(bbox_to_anchor=(1.2, 1))
    plt.title("Trends of Causes of Death between 2014 - 2019",
              fontsize=12)
    plt.xlabel("Years between 2014 - 2019")
    plt.ylabel("Number of deaths")
    plt.tight_layout()
    plt.savefig(f"visualization/{final_save_string}.png")

def plot_total_pie(df, year):
    assert isinstance(year, int)
    fig = plt.figure()
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rc('font', size=8)
    plt.title(f"Causes of Death Percentages in {year}",
              fontsize=12)
    all_causes = df["Cause"].unique()
    plot_df = df[df["Year"] == year]
    plt.pie(plot_df["Count"], startangle=90, autopct='%1.1f%%', labels=plot_df["Cause"])

    plt.savefig(f"visualization/total_death_percentage_pie.png")

df = causeOfDeath()
plot_and_save_clause(df, causes=["ALZ","HYP","HTD"])
plot_and_save_clause(df, causes=["ALZ"])
plot_and_save_clause(df, causes=["HYP"])
plot_and_save_clause(df, causes=["HTD"])
plot_total_pie(df, 2014)
