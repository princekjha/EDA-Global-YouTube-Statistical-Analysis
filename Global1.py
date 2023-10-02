#!/usr/bin/env python
# coding: utf-8

# In[1]:


# get_ipython().system('pip install dash')


# In[3]:


import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import seaborn as sns

# Load the CSV data
url = 'Global.xlsx'
df = pd.read_excel(url)


# In[62]:


#df.head(5)


# In[63]:


#df.tail(5)


# In[64]:


#df.describe()


# In[65]:


#df.info()


# In[8]:


# checking for the outlier
#print(sns.boxplot(df["created_year"]))


# In[4]:


# Filter rows where 'created_year' is greater than or equal to 2005
df1 = df[df['created_year'] >= 2005]
#df1


# In[9]:


#sns.boxplot(df1["created_year"])


# In[11]:


#df1.info()


# # Top 10 YouTubers by Subscribers

# In[15]:


fig1 = px.bar(df1.head(10), x='Youtuber', y='subscribers', title='Top 10 YouTubers by Subscribers')
#fig1.show()


# # Geographic Distribution of Viewers

# In[66]:


fig2 = px.scatter_geo(df1, lat='Latitude', lon='Longitude', size='video views', projection='natural earth',
                      animation_frame='category',title='Geographic Distribution of Viewers',height=500,width=1000)
#fig2.show()


# # Total Video Uploads by Year

# In[48]:


df2 = df1[['created_year','uploads']]
#df2


# In[52]:


sum_uploads_by_year = df2.groupby('created_year')['uploads'].sum().reset_index()

# Create the bar plot
# plt.figure(figsize=(10, 6))
fig3 = px.bar(sum_uploads_by_year, x='created_year', y='uploads',title='Total video Uploads by Year')
#fig3.show()


# # Top 5 Countries and Their Top 5 Categories

# In[53]:


# Calculate total viewers and subscribers by grouping by 'Country' and 'category'
grouped_df = df1.groupby(['Country', 'category']).agg({'video views': 'sum', 'subscribers': 'sum'}).reset_index()


# In[54]:


# Find the top 5 countries by total 'video views'
top_5_countries = grouped_df.groupby('Country').agg({'video views': 'sum'}).nlargest(5, 'video views').index.tolist()


# In[55]:


# Filter the DataFrame to include only data for the top 5 countries
top_5_countries_df = grouped_df[grouped_df['Country'].isin(top_5_countries)]


# In[56]:


# Sort the data to get the top 5 categories within each of the top 5 countries
top_5_countries_categories_df = top_5_countries_df.groupby('Country').apply(lambda x: x.nlargest(5, 'video views')).reset_index(drop=True)


# In[57]:


# Create the sunburst chart
fig4 = px.sunburst(top_5_countries_categories_df, path=['Country', 'category'],
                  values='video views',
                  hover_name='category',
                  hover_data={'video views', 'subscribers'},
                  title='Sunburst Chart: Top 5 Countries and Their Top 5 Categories')

# Show the chart
#fig4.show()


# # YouTube Subscribers Growth Over the Years

# In[58]:


# Group the data by 'created_year' and sum the 'subscribers' for each year
subscribers_growth = df1.groupby('created_year')['subscribers'].sum().reset_index()


# In[59]:


# Create a line chart
fig5 = px.line(subscribers_growth, x='created_year', y='subscribers',
              title='YouTube Subscribers Growth Over the Years',
              labels={'created_year': 'Year', 'subscribers': 'Total Subscribers'})

# Show the chart
#fig5.show()


# # Creating Dashboard

# In[67]:


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Global YouTube Statistics Dashboard"),

    # Dropdown to select a chart
    dcc.Dropdown(
        id='chart-dropdown',
        options=[
            {'label': 'Top 10 YouTubers', 'value': 'top-10-youtubers'},
            {'label': 'Geographic Distribution of Viewers', 'value': 'geo-plot'},
            {'label': 'Top 5 Years of Channel Creation', 'value': 'Total Uploads by Year'},
            {'label': 'Sunburst Chart', 'value': 'sunburst-chart'},
            {'label': "YouTube Subscribers Growth Over the Years", 'value': 'top-5-growing-channels'},
        ],
        value='top-10-youtubers'  # Default chart
    ),

    # Chart container
    dcc.Graph(id='selected-chart'),
])

# Callback to update the displayed chart based on the selected value
@app.callback(
    Output('selected-chart', 'figure'),
    Input('chart-dropdown', 'value')
)
def update_selected_chart(selected_chart):
    # Replace these placeholders with your actual chart logic
    # You can use Plotly Express or Plotly.graph_objects to create the charts

    if selected_chart == 'top-10-youtubers':
        fig = fig1
    elif selected_chart == 'geo-plot':
        fig = fig2   
    elif selected_chart == 'Total Uploads by Year':
        fig = fig3   
    elif selected_chart == 'sunburst-chart':
        fig = fig4
    elif selected_chart == 'top-5-growing-channels':
        fig = fig5
    else:
        fig = None  # Default to None if an invalid chart is selected

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8061)


# In[ ]:




