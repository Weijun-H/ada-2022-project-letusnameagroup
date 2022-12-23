import base64

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

st.set_page_config(page_title="Beer Story",
                   page_icon="🍺")


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
def plot_html(filename, height):
    with open(filename, 'r') as f:
        html_data = f.read()
    st.components.v1.html(html_data, scrolling=True, height=height)


def plot_gif(filename):
    """### gif from local file"""
    file_ = open(filename, "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )


###################
### BACKGROUNDS ###
###################

image = Image.open('beer.jpg')

st.image(image)

####################
### INTRODUCTION ###
####################

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))

# with row0_1:
st.title("Trends in the American Beer Market: How can we help the declining beer styles to revive?")

# _, row2, _ = st.columns((.1, 3.2, .1))
# with row2:
st.subheader("Introduction")
st.markdown("Beer is one of the oldest beverages in the world. With the progress of brewing technology, "
            "many new brands and styles have been created. Meanwhile, a proportion of breweries are still trying "
            "to preserve their traditional brewing techniques.")
st.markdown("As a significant beer consumer, the United States plays a crucial role in the world’s beer industry. "
            "Therefore, with the curiosity about beer among Americans, let’s have an insight into their beer "
            "industry. After some research, we found that the website “BeerAdvocate.” users are mainly from the "
            "U.S., so we retrieved the user data, brewery data, and review data, ranging from 1998 to 2017, "
            "from the BeerAdvocate dataset.")
st.markdown("We write this analysis to discuss the overall trend in the U.S. beer market, like which styles are "
            "becoming more popular and which are declining. Combined with sentiment analysis and high-frequency "
            "words, we analyzed the reasons behind it. We also analyzed the trends specified in regions and gave some "
            "basic instructions to the breweries.")
st.markdown(
    "You can find the source code in the [here]("
    "https://github.com/epfl-ada/ada-2022-project-letusnameagroup)")

### First Glimpse ###

st.subheader("First Glimpse of the all reviews")
st.markdown("To get a general feeling about the popular beers among American families, we first look at the number of "
            "ratings grouped by two perspectives, the ABV (alcoholic strength) and the style.")
st.markdown("For the ABV, the graph roughly follows a normal distribution. The number of reviews is high in the "
            "center, and then it goes down on both sides. It isn’t hard to figure out that the number of reviews is "
            "relatively low when the ABV is either too high or too low. Users’ reviews focus on beers with an ABV of "
            "around 5.")
# TODO: change figure size
plot_html('./figure/hist.html', 450)

st.markdown("Among the various types of beer, which styles are the most popular in the United States? We found that "
            "by 2017, the top 3 styles with the most significant number of reviews are American IPA, "
            "American Double/Imperial IPA, and American Porter, which add up to one-fourth of the total number of "
            "reviews. And for American IPA, it even accounts for 10% of the reviews! Maybe your favorite type is just "
            "in these three types! What’s more, American Pale Ale(APA), Russian Imperial Stout, and American "
            "Amber/Red Ale also have large percentages.")
st.markdown("For simplicity, we mainly focus on the top three styles with an ABV in the middle 50% quantile in the "
            "later analysis.")

### Trend Analysis:###
st.subheader("Are the popular beer styles set in stone?")
st.markdown("In order to get some knowledge of the US beer market, we first focus on each style's trend. The trend in "
            "the number of reviews in the top 3 styles (American IPA, American Double/Imperial IP, and American "
            "Porter) is demonstrated below.")

st.image('./figure/number_of_review_top_3.png')

st.markdown("As demonstrated in the line plots, the number of reviews for all three styles increased from 1998 to "
            "2011, starting from zero and reaching high values. However, from 2011 to 2014, the numbers all decreased "
            "incredibly. Although a turning point existed from around 2014 to 2015, they all fell again after 2015. "
            "The line graphs all look like mountains with two peaks.")
st.markdown("Is this just a coincidence that the trends look similar? May the number of active users on the website "
            "influence the above charts? By common sense, from 1998 to the early 21st century, personal computers and "
            "the Internet were only partially popularized, so the number of active users might increase. And after "
            "the first decade of the millennium, the number of users who were still active on the website fell again "
            "due to smartphones and social apps' springing up. To know whether this is really the case, we plot the "
            "number of users over time.")

st.image('./figure/number_of_review_every_year.png')

st.markdown("The graph shows that the trend is the same as the three most popular styles and almost the same as our "
            "common sense. To cancel out the influence, we divide the number of reviews for each style by the total "
            "number of reviews per year.")

st.image('./figure/without_prediction.png')

st.markdown("The above is the trend of the three styles after scaling by the total number of reviews. Because the "
            "number of considerations before 2003 is relatively small, the variation of the lines is quite "
            "significant. Nevertheless, the result seems correct for the trend after 2003. The proportion for "
            "American IPA and American Double/Imperial IPA has been increasing since 2003, while that for American "
            "Porter is the opposite.")

st.markdown("Based on the trend, breweries can adjust their output and production strategies. Treating the data as a "
            "time series, we make predictions on the proportions of the three types over the next five years.")

st.image('./figure/with_prediction.png')

st.markdown("Here for the American IPA, the variation in the prediction is due to the property in time series "
            "forecasting. There is volatility, and because the variation before the starting point of prediction is "
            "quite large, the volatility is also significant. However, still, we can see the overall trend is "
            "increasing. So, breweries can increase the production of American IPA a little bit and Imperial IPA a "
            "lot while reducing the production of American Porter to get more profits.")

st.markdown("However, why is this the trend? Why did the first two styles increase in popularity when American Porter "
            "received less attention? Can we revive American Porter?")

st.markdown("We will follow up on the three questions above in the next sections.")

### Sentiment Analysis ###
st.subheader("Let's explore the textual review?")

st.markdown("Let’s dive into the sea of reviews. Maybe it will tell us that people’s sentiments in the review may "
            "somehow be related to the change in the fraction of the beer.")
st.markdown("First, we plot the change in positive sentiments for the three styles.")

st.image('./figure/fraction_of_positive_reviews.png')

st.markdown("There is almost no difference in the positive sentiment of reviews for the styles. So maybe look at the "
            "negative ones.")

st.image('./figure/fraction_of_negative_reviews.png')

st.markdown("From the line chart, we can tell that starting from 2003 (a large variation before the year), "
            "the fractions of negative reviews for American IPA and Imperial IPA are almost unchanged, although with "
            "some vibrations. But for American Porter, the concentration of negative sentiment increased much more "
            "obviously than the other two, from around 0.01 to the highest 0.03. The increase in the fraction of "
            "negative reviews can show that consumers' attitudse toward American Porter shifts to the negative side a "
            "bit. Also, there is a term in psychology called “negative bias,” which states compared to positive "
            "information, we tend to pay more attention to the negative one. So when the negative concentration "
            "increased, people started to focus more on the negative reviews, and thus the popularity decreased.")
st.markdown("So breweries can learn from the negative reviews to improve their products and make them more popular. "
            "We should know what people said about it in the reviews with negative sentiment.")
st.markdown("Let us extract what people frequently say in negative reviews!")
st.markdown("But first, we need to figure out whether there is any relationship between the negative sentiment and "
            "the low ratings so that we can better filter the negative reviews. We use linear regression to fit the "
            "rating and the negative sentiment and find no linear relationship between them (too low in R-square). So "
            "there may be negative sentiment in reviews with high ratings and positive sentiment in reviews with low "
            "ratings. Thus, we need to filter reviews with both negative sentiment and low ratings.")

st.markdown("In most cases, nouns and adjectives carry more information. Therefore, in the reviews we filtered out, "
            "we extracted both the top 20 frequently used nouns and adjectives.")

st.image("./figure/noun_adj.png")

st.markdown("From the list of nouns, we can see that in the negative reviews, people place more emphasis on the hop, "
            "flavor, taste, and aroma. In the adjective word list, words like bitter, sweet, light, dark, white, "
            "brown, and golden occur. But it is still hard to draw a conclusion about whether people think the beer "
            "is too bitter or too sweet, and whether the user likes or dislikes the beer being too light in flavor.")

st.markdown("To ensure we get the correct instructions for the breweries, we must research the beer’s characteristics "
            "and brewing techniques. Let us first research the three styles we previously filtered, the more and more "
            "popular American IPA, Imperial IPA, and American Porter which is becoming less and less popular.")

table_md = """
|                              | Color                     | Bitterness       | Alchohol           | Hop                                                     | Easters                      |
|------------------------------|---------------------------|------------------|--------------------|---------------------------------------------------------|------------------------------|
| American IPA                 | Gold to Copper, Red/Brown | 50-70IBU(High)   | Mild to noticeable | Floral and citrus-like aroma <br /> High in bitterness         | Citrus, Tropical Fruit, Pine |
| American Double/Imperial IPA | Gold to Light Brown       | 60-100IBU(High)  | Noticeable         | Fresh and lively aroma <br /> High in bitterness               | Fruity easter aroma          |
| American Porter              | BLACK                     | 30-35IBU(medium) | Noticeable         | Medium-low in bitterness Low-medium in aroma and flavor | Ale-like fruity ester        |
"""
st.markdown(table_md)

st.markdown(
    "Surprisingly, we found some obvious differences between American/Imperial IPA and American Porter. American IPA "
    "and Imperial IPA are light in color, while American Porter is black. The bitterness of American IPA and Imperial "
    "IPA is high, while American Porter’s bitterness is relatively lower. There is an evident refreshing flavor and "
    "high bitterness in American IPA and Imperial IPA’s hop. At the same time, American Porter is low to medium in "
    "aroma and flavor and is less bitter for its hop.")

st.markdown("Do people not prefer beer that is dark in color, low in bitterness, with less evident flavor and aroma "
            "in the hop, and Ale-like ester anymore?")
st.markdown("So we found American Amber / Red Ale and Belgian Strong Dark Ale, which have darker colors and less "
            "flavor from the hop.The following figures show the total ratings of these beers compared to all beers "
            "over time.")

st.image("./figure/ale.png")

st.markdown("We can see that these styles are also becoming less and less popular. So combined with the frequent "
            "words, we can tell breweries to improve their brewing techniques to make the hops more fruity and "
            "refreshing flavor and make bitterness higher.")

st.markdown('We also find an article about American Porters, it writes')
st.markdown('> Why didn’t porters stay popular? Caramel malt '
            'is no longer a popular ingredient, and it has been stripped down or out of most pales, stouts, '
            'and IPAs these days. Red ales and amber ales, beers dependent on caramel malt, have become scarce. The '
            'flavor of caramel and the heavy body it imparts is unfashionable, and styles have left it behind.')
st.markdown('This corresponds to what we found about users’ preferences.')

### Style Trend in different States ###
st.subheader("How could we learn from what people say in the review?")

# TODO: change figure
st.image('./figure/wordcloud.png')

st.markdown("Our team based on the reviews on BeerAdvocate to analyze the quality of the reviews. We summarized the "
            "frequent adjectives and nouns in different regions. And a lot of them are related to hop and taste. "
            "Based on it, we researched popular beer colors and hop and found that the lighter and bitterer beers "
            "are, the more popular they are. But does this phenomenon vary from region to region?")

st.markdown("In the next step, we aimed to identify potential differences in user profiles for beer across various "
            "regions. To do so, we grouped our data set by region and focused on the top three regions with the "
            "highest number of reviews: Pennsylvania, California, and New York in the US. We then analyzed the nouns "
            "and adjectives that appeared most frequently in reviews from each region.")

# TODO: add GIF
_left, mid, _right = st.columns((0.01, .9, .15))
with mid:
    st.image(
        "https://github.com/Weijun-H/ada-2022-project-letusnameagroup/blob/main/gif/+United%20States,%20California.gif?raw=true")
    st.image(
        "https://github.com/Weijun-H/ada-2022-project-letusnameagroup/blob/main/gif/+United%20States,%20Pennsylvania.gif?raw=true")
    st.image("https://github.com/Weijun-H/ada-2022-project-letusnameagroup/blob/main/gif/+United%20States,%20New%20York.gif?raw=true")

st.markdown("Our findings indicate that the reviews from these three regions had many similarities in that they all "
            "emphasized the importance of malt liquor and the flavor and taste of the beer. This aligns with our "
            "previous research, which identified taste as the primary factor influencing overall satisfaction with "
            "beer.")

st.markdown("Additionally, sweetness, citrus, aroma, and bitterness were among the next most frequently mentioned "
            "aspects in these reviews. However, appearance and price did not rank highly as concerns among users in "
            "these regions. There were also some differences in the way users rated the beer in each region. For "
            "example, Pennsylvanians placed a higher emphasis on the color of the beer compared to the aroma and "
            "sweetness, while New Yorkers also considered color to be important but less so than Pennsylvanians. New "
            "Yorkers also preferred carbonation. Californians, on the other hand, were more focused on the taste of "
            "the beer and gave less weight to color.")

st.markdown("This information can be useful for brewers as it provides insight into the preferences of their "
            "customers in different regions. For example, Pennsylvanians placed a higher emphasis on the color of the "
            "beer, and in the animation, we found that the IPAs which are generally lighter in color are becoming "
            "more popular, and the American Porter and Amber Ale, which are darker are on the opposite.")

st.markdown("And for Californians, they focused on the taste of the beer. The IPA category is far more popular than "
            "the traditional Ale category. The preference score for the most popular American IPA is around three "
            "times that of the most popular Ale. The IPA category has a fuller hop flavour, a higher alcohol content, "
            "and a more varied flavour profile, and the taste of Ale can be improved by considering these aspects.")

st.markdown("By understanding these preferences, brewers can tailor their beers to better meet the needs of their "
            "customers in each region.")

st.subheader("Conclusion")
st.markdown("In summary, the purpose of this study was to explore trends in the American beer market and specific "
            "regions within it. To accomplish this, we employed statistical and time series modeling, as well as "
            "sentiment analysis and natural language processing techniques, to analyze consumer comments. Our "
            "analysis revealed key trends in consumer preferences for various beer styles and how these preferences "
            "have evolved over time. These findings provide valuable insights for breweries and marketers looking to "
            "understand the changing preferences of beer drinkers and make informed decisions about their products "
            "and marketing strategies.")