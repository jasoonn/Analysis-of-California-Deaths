# Group data based on the counties
# i.e for every county, what are the counts of deaths by particular diseases over the years
# For e.g: In San Diego, in 2014, 200 ppl died of liver infection and in 2015, 300
import os
import pandas as pd
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname( __file__ ))
DATA_DIR = f'{BASE_DIR}/data'
VISUALIZATION_DIR = f'{BASE_DIR}/visualization'
CSV_FILE = 'death.csv'
raw_data_file = pd.read_csv(f'{DATA_DIR}/{CSV_FILE}')
COUNTY_COL = 'County'
CAUSE_COL = 'Cause_Desc'
COUNT_COL = 'Count'
YEAR_COL = 'Year'

modified_data = raw_data_file[[YEAR_COL,COUNTY_COL, CAUSE_COL, COUNT_COL]].copy()
modified_data.drop(modified_data.index[modified_data[CAUSE_COL] == 'All causes (total)'], inplace = True)

grouped_data = (modified_data.groupby([YEAR_COL, COUNTY_COL, CAUSE_COL])[COUNT_COL].sum().reset_index(name='Total Count'))
year_county_deaths = grouped_data.pivot_table(values='Total Count', index=[COUNTY_COL, YEAR_COL], columns=CAUSE_COL, aggfunc='first')
year_county_deaths.sort_values(by=[YEAR_COL, COUNTY_COL], inplace = True)
year_county_deaths.reset_index(inplace=True)
year_county_deaths.to_csv(f'{DATA_DIR}/grouped_deaths_by_counties.csv')

def disease_county_dist_yearly_analysis(year_county_deaths, year=2019):

    county_2019_values = year_county_deaths.loc[year_county_deaths[YEAR_COL] == year]

    for col in county_2019_values.columns:
        if col != COUNTY_COL and col != YEAR_COL:
            curr_df = county_2019_values[[COUNTY_COL, col]]
            n_largest_df = curr_df.nlargest(10, col)
            
            plt.figure()
            plt.bar(n_largest_df[COUNTY_COL].to_list(), n_largest_df[col].to_list(), color='green')
            plt.xlabel("Counties")
            plt.ylabel(f"{col}")
            plt.title(f"{col} across counties")
            plt.xticks(rotation=25, fontsize=7)
            plt.show()
            break

# def get_percentage_changes_across_years(year_county_deaths):
column_names = year_county_deaths.columns
column_names = column_names[2:]
county_names = ['Los Angeles', 'San Diego', 'Riverside', 'Orange', 'San Bernardino', 'Sacramento', 'Santa Clara']

width = 0.1


for disease in column_names:
    curr_df = year_county_deaths[[COUNTY_COL, YEAR_COL, disease]]
    n = len(county_names)
    r = np.arange(n)
    d = defaultdict(list)
    for year in list(sorted(set(year_county_deaths[YEAR_COL]))):
        new_df = curr_df.loc[curr_df[YEAR_COL] == year]
        new_df = new_df.loc[new_df[COUNTY_COL].isin(county_names)]
        
        d[year] = list(new_df[disease])
    i = 0
    plt.figure()
    for y, value in d.items():
        bars = plt.bar(r+width*i,value,width = width,label=f'{y}')
        i += 1
    plt.xlabel("Counties")
    plt.ylabel("Number of deaths per year")
    plt.title(f"No. of deaths per year due to {disease} by county")
    plt.xticks(r + width/2,county_names,rotation=25,fontsize=7)
    plt.legend()
  
    plt.savefig(f'{VISUALIZATION_DIR}/county/{disease}.png')
    print(f"Done with {disease} plot..")
    break
                
        

# def multiple_bar_charts_per_disease(year_county_deaths):
#     column_names = year_county_deaths.columns
#     column_names = column_names[2:]
    
#     x_axis = list(set(year_county_deaths[COUNTY_COL]))
    
# disease_county_dist_yearly_analysis(year_county_deaths, 2014)
# multiple_bar_charts_per_disease(year_county_deaths)
