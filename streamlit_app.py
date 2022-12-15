from IPython.display import HTML, Javascript, display
from ipywidgets import interact
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats import diagnostic
from scipy import stats
import streamlit as st
import numpy as np
import pandas as pd
import pickle
import time
from matplotlib.ticker import FuncFormatter

from PIL import Image



import matplotlib.pyplot as plt
import seaborn as sns
import datetime

placehold = ""
with open('placehold.txt') as f:
    placehold = ('').join(f.readlines())

sns.set_style("darkgrid")


st.set_page_config(layout="wide")

### Data Import ###

# df_database = pd.read_csv("./data/data_BuLi_13_20_cleaned.csv")
# types = ["Mean","Absolute","Median","Maximum","Minimum"]
# label_attr_dict = {"Goals":"goals","Halftime Goals":"ht_goals","Shots on Goal":"shots_on_goal","Distance Covered (in km)":"distance","Passes":"total_passes", "Successful Passes":"success_passes", "Failed Passes":"failed_passes", "Pass Success Ratio":"pass_ratio", "Ball Possession":"possession", "Tackle Success Ratio":"tackle_ratio", "Fouls Committed":"fouls", "Fouls Received":"got_fouled", "Offsides":"offside", "Corners":"corners"}
# label_attr_dict_teams = {"Goals Scored":"goals","Goals Received":"goals_received","Halftime Goals Scored":"ht_goals","Halftime Goals Received":"halftime_goals_received","Shots on opposing Goal":"shots_on_goal","Shots on own Goal":"shots_on_goal_received","Distance Covered (in km)":"distance","Passes":"total_passes", "Successful Passes":"success_passes", "Failed Passes":"failed_passes", "Pass Success Ratio":"pass_ratio", "Ball Possession":"possession", "Tackle Success Ratio":"tackle_ratio", "Fouls Committed":"fouls", "Fouls Received":"got_fouled", "Offsides":"offside", "Corners":"corners"}
# color_dict = {'1. FC Köln': '#fc4744', '1. FC Nürnberg':'#8c0303', '1. FC Union Berlin':'#edd134', '1. FSV Mainz 05':'#fa2323', 'Bayer 04 Leverkusen':'#cf0c0c', 'Bayern München':'#e62222', 'Bor. Mönchengladbach':'#1f9900', 'Borussia Dortmund':'#fff830', 'Eintracht Braunschweig':'#dbca12', 'Eintracht Frankfurt':'#d10606', 'FC Augsburg':'#007512', 'FC Ingolstadt 04':'#b50300', 'FC Schalke 04':'#1c2afc', 'Fortuna Düsseldorf':'#eb3838', 'Hamburger SV':'#061fc2', 'Hannover 96':'#127a18', 'Hertha BSC':'#005ac2', 'RB Leipzig':'#0707a8', 'SC Freiburg':'#d1332e', 'SC Paderborn 07':'#0546b5', 'SV Darmstadt 98':'#265ade', 'TSG Hoffenheim':'#2b82d9', 'VfB Stuttgart':'#f57171', 'VfL Wolfsburg':'#38d433', 'Werder Bremen':'#10a30b'}
# label_attr_dict_correlation = {"Goals":"delta_goals", "Halftime Goals":"delta_ht_goals","Shots on Goal":"delta_shots_on_goal","Distance Covered (in km)":"delta_distance","Passes":"delta_total_passes","Pass Sucess Ratio":"delta_pass_ratio","Possession":"delta_possession","Tackle Success Ratio":"delta_tackle_ratio","Fouls":"delta_fouls","Offside":"delta_offside","Corners":"delta_corners"}
# label_fact_dict = {"goals scored":'goals',"halftime goals scored":'ht_goals',"shots on the goal":'shots_on_goal',"distance covered (in km)":'distance',"total passes":'total_passes',"pass ratio":'pass_ratio',"possession ratio":'possession',"successful tackle ratio":'tackle_ratio',"fouls":'fouls',"offsides":'offside',"corners":'corners'}

### Helper Methods ###



###############################
### ANALYSIS METHODS (PLOT) ###
###############################
def plot_html(filename):
  with open(filename, 'r') as f:
      html_data = f.read()
  st.components.v1.html(html_data,height=450, scrolling = True)


###################
### BACKGROUNDS ###
###################

image = Image.open('beer.jpg')

st.image(image)

####################
### INTRODUCTION ###
####################

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))

with row0_1:
  st.title("Let us make the most popular beer🍺!")

_, row2, _ = st.columns((.1, 3.2, .1))
with row2:
  st.subheader("Introduction")
  st.markdown("Over the 20 years, beer rating websites have attracted plenty of users to give ratings and reviews about beers. As time passes, people may change their preference for beer. We intend to use the review and scores of different beers on BeerAdvocate and RateBeer websites. To determine which factors have the most significant influence on beer's overall rating. And give production or sales suggestions to the breweries in the different regions. Due to the increasing number of negative reviews and water army, the consumer would easily be affected by these grading. We would like to know if this phenomenon also happened in our dataset. Because negative reviews are generally random text, we intend to train the model using reviews as input and ratings as labels. Thus detecting malicious reviews and eliminating this affection.")
  st.markdown(
      "You can find the source code in the [Let us make the most popular beer!](https://github.com/epfl-ada/ada-2022-project-letusnameagroup)")


_, row3, _ = st.columns((.1, 3.2, .1))
with row3:
  st.subheader("The portrait of the beers that are most popular among people")
  plot_html('./figure/hist.html')
  st.write(placehold)

_, row4, _ = st.columns((.1, 3.2, .1))
with row4:
  st.subheader("What is the relation between descriptive reviews and Overall scores?")
  st.write(placehold)


_, row5, _ = st.columns((.1, 3.2, .1))
with row5:
  st.subheader("What is the shift in people's preference for beer style over some time? How do we use the trend to give some brewing advice to Brewery?")
  st.write(placehold)
