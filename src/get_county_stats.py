# Group data based on the counties
# i.e for every county, what are the counts of deaths by particular diseases over the years
# For e.g: In San Diego, in 2014, 200 ppl died of liver infection and in 2015, 300
import os
import pandas as pd
BASE_DIR = os.path.dirname(os.path.dirname( __file__ ))
DATA_DIR = f'{BASE_DIR}/data'
CSV_FILE = 'death.csv'
raw_data_file = pd.read_csv(f'{DATA_DIR}/{CSV_FILE}')
COUNTY_COL = 'County'
CAUSE_COL = 'Cause_Desc'
COUNT_COL = 'Count'
YEAR_COL = 'Year'

modified_data = raw_data_file[[YEAR_COL,COUNTY_COL, CAUSE_COL, COUNT_COL]].copy()
modified_data.drop(modified_data.index[modified_data[CAUSE_COL] == 'All causes (total)'], inplace = True)
# x = modified_data.pivot_table(values=COUNT_COL, index=modified_data.index, columns=[YEAR_COL, COUNTY_COL, CAUSE_COL], aggfunc='first')
y = (modified_data.groupby([YEAR_COL, COUNTY_COL, CAUSE_COL])[COUNT_COL].sum().reset_index(name='Total Count'))
x = y.pivot_table(values='Total Count', index=[COUNTY_COL, YEAR_COL], columns=CAUSE_COL, aggfunc='first')

x.to_csv(f'{DATA_DIR}/grouped_deaths_by_counties.csv')