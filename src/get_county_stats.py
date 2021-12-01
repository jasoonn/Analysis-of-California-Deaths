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

def get_county_deaths_by_disease():
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
                
def car_accidents_percentage_increase():
    '''
    Resource:
    https://ktla.com/news/local-news/traffic-related-fatalities-increased-in-2019-as-number-of-collisions-dropped-in-l-a-police-chief-says/
    '''
    car_accidents_column = 'Accidents (unintentional injuries)'
    accidents_df = year_county_deaths[[COUNTY_COL, YEAR_COL, car_accidents_column]]
    concerned_years = [2018,2019]
    last_2_years_accidents = accidents_df.loc[accidents_df[YEAR_COL].isin(concerned_years)]
    last_2_years_accidents.sort_values(by=[YEAR_COL])
    
    percentage_increase = defaultdict(float)
    for county in county_names:
        accident_value = last_2_years_accidents.loc[last_2_years_accidents[COUNTY_COL] == county]
        value_2018 = (accident_value[car_accidents_column].iloc[0])
        value_2019 = (accident_value[car_accidents_column].iloc[len(accident_value.index)-1])
        percentage_increase[county] = ((value_2019-value_2018)/value_2018)*100;  
    
    total_items = len(percentage_increase)-1
    total_increase_other_counties = 0
    for county, incr in percentage_increase.items():
        if county != 'Los Angeles':
            total_increase_other_counties += incr
    avg_increase = total_increase_other_counties/total_items
    
    x_pos = [0,1]
    x_axis = ['Los Angeles', 'All Other Counties']
    y_axis = [percentage_increase['Los Angeles'], avg_increase]
    plt.figure()
    plt.bar(x_pos,y_axis,width=0.25)
    plt.xticks(x_pos, x_axis)
    plt.xlabel("Counties")
    plt.ylabel("Percentage increase in deaths due to accidents")
    plt.title(" % Increase in deaths due to accidents from 2018 to 2019")
    
    plt.show()
    # plt.savefig(f'{VISUALIZATION_DIR}/accident/accident_analysis.png')
    
def get_homicide_rates_county():
    homicide_column = 'Assault (homicide)'
    concerned_county = 'San Diego'
    homicide_df = year_county_deaths[[COUNTY_COL, YEAR_COL, homicide_column]]
    print(homicide_df)
    concerned_years = [2017,2018,2019]
    san_diego_homicides = homicide_df.loc[homicide_df[COUNTY_COL] == concerned_county]
    san_diego_homicides = san_diego_homicides.loc[san_diego_homicides[YEAR_COL].isin(concerned_years)]
    
    # print(san_diego_homicides.iloc[0])
    
def get_influenza_rates_county():
    influenza_col = 'Influenza and pneumonia'
    influenza_df = year_county_deaths[[COUNTY_COL, YEAR_COL, influenza_col]]
    concerned_years = [2018, 2019]
    county_influenza_df = influenza_df.loc[influenza_df[COUNTY_COL].isin(county_names)]
    county_influenza_df = county_influenza_df.loc[county_influenza_df[YEAR_COL].isin(concerned_years)]
    county_influenza_df.sort_values(by=[YEAR_COL])
    # print(county_influenza_df[county_influenza_df[YEAR_COL] == 2018])
    # values_2018 = county_influenza_df.loc[county_influenza_df[YEAR_COL] == '2018']
    # print(values_2018)
    values = defaultdict(list)
    values_year_1 = list()
    values_year_2 = list()
    for year in (concerned_years):
        for county in county_names:
            values[county].append((county_influenza_df[county_influenza_df[YEAR_COL] == year][county_influenza_df[COUNTY_COL] == county][influenza_col].iloc[0]))
    for _,value in values.items():
        values_year_1.append(value[0])
        values_year_2.append(value[1])
    
    n = len(county_names)
    r = np.arange(n)
    plt.figure()
    width = 0.2
    plt.bar(r, values_year_1, width, label = '2018')
    plt.bar(r + 0.2, values_year_2, width, label = '2019')
    plt.xlabel("Counties")
    plt.ylabel("Number of deaths per year due to influenza")
    plt.title(" Trend of deaths due to influenza from 2018 to 2019")
    plt.xticks(r,county_names,rotation=25,fontsize=7)
    plt.legend()
    plt.savefig(f'{VISUALIZATION_DIR}/accident/influenza.png')
        
# get_homicide_rates_county()
# get_influenza_rates_county()
# car_accidents_percentage_increase()  
# disease_county_dist_yearly_analysis(year_county_deaths, 2014)
# multiple_bar_charts_per_disease(year_county_deaths)
