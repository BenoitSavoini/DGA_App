# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 13:51:59 2023

@author: Alkios
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
import plotly.express as px
import json



cwd = 'C:/Users/Alkios/Downloads/DGA_app'
os.chdir(cwd)



with open('Atlanta_Neighborhoods.geojson') as f:
    neighborhood_geojson = json.load(f)


# Load data
df = pd.read_csv('atlcrime.csv')

df2 = df.groupby(['date']).count()

# Group the data by neighborhood and sum the number of crimes
df_neighborhood = df.groupby(['neighborhood'])['crime'].count().reset_index()



app = dash.Dash(__name__)

# Create a scatter mapbox figure using plotly.express
fig = px.scatter_mapbox(df, 
                        lat="lat", 
                        lon="long", 
                        color="crime", 
                        mapbox_style="open-street-map",
                        zoom=10)

fig.update_layout(
    title="Crime Map",
    mapbox_style="open-street-map",
    mapbox=dict(
        zoom=10,
        center=dict(lat=df['lat'].mean(), lon=df['long'].mean())
    )
)


fig2 = px.line(df2, x=df2.index, y="crime", title="Crime Over Time")

# Set the layout for the line plot
fig2.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Crimes"
)



# Create a choropleth map using plotly.express
fig3 = px.choropleth(df_neighborhood, 
                    geojson=neighborhood_geojson,  # GeoJSON file containing the neighborhood boundaries
                    locations='neighborhood',
                    featureidkey='properties.NAME',
                    color='crime', 
                    color_continuous_scale='YlOrRd', 
                    range_color=(0, df_neighborhood['crime'].max()),
                    labels={'crime':'Number of Crimes'})


fig3.update_geos(fitbounds="locations", visible=False)

app.layout = html.Div(children=[
    html.H1(children='Crime Data Visualization'),
    
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Crime Numbers Over Time', value='tab-1', children=[
            dcc.Graph(
        id='crime-over-time',
        figure=fig2
    )]),
        
        dcc.Tab(label='Crime Location on Map', value='tab-2', children=[
            dcc.Graph(
        id='crime-map',
        figure=fig,
        style={'height': '80vh', 'width': '90%'}  # Set the height and width of the graph component
    )])
        ,
        dcc.Tab(label='Crime by Neighborhood', value='tab-3', children=[
            dcc.Graph(
        id='crime-by-neighborhood',
        figure=fig3,
        style={'height': '80vh', 'width': '90%'}  # Set the height and width of the graph component
    )
        ])
    ])
])
if __name__ == '__main__':
    app.run_server(debug=False)

