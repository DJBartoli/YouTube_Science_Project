import os
from datetime import datetime, timedelta
import json

import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.graph_objects as go

from geopy.geocoders import Nominatim
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import json
import dash_bootstrap_components as dbc

dash.register_page(__name__,  name='Duration Interactions')

df = pd.read_csv('data/duration/Markiplier_Formatted.csv')

boxdf = pd.read_csv('data/duration/Boxplot_Data.csv')

avg_like = df.groupby('Category')['Like/View'].mean().reset_index()

avg_comment = df.groupby('Category')['Comment/View'].mean().reset_index()

# Barchart

bar_titles = ['0-5', '5-10', '10-20', '20-30', '30-60', '60+']

fig = go.Figure(data=[
    go.Bar( name='Average Likes', x=avg_like['Category'], y=avg_like['Like/View']),
    go.Bar( name='Avegare Comments', x=avg_comment['Category'], y=avg_comment['Comment/View'], marker_color='#dd2b2b',)
])

bar_titles = ['0-5', '5-10', '10-20', '20-30', '30-60', '60+']
fig.update_layout(title_text='Average Viewer Interactions measured by Comments and Likes', barmode='stack',
            plot_bgcolor='#e7e7e7',
            paper_bgcolor='#d1d1d1')
fig.update_xaxes(title='Video Length in Minutes',tickvals=avg_like['Category'], ticktext=bar_titles)
fig.update_yaxes(title='Interactions per 1000 Views')

# Layout

layout = html.Div(
    dbc.Row(
        [
            dbc.Col(
                html.H2('Viewer Interaction based on Video Length', style={'color': '#dd2b2b'}),
                width={'size': 5, 'offset': 1},
                style={'height':'80px'},
            ),

            dbc.Row(dbc.Col(
                html.H5('The charts on this page show the correlation between video length and viewer engagement for the channel "Markiplier".', ),
                width={'size': 7, 'offset': 1},
                style={'height':'80px'},
            )),

            dbc.Row([
                dbc.Col(dcc.Graph(
                id='duration-bar', figure=fig),
                width={'size': 7, 'offset': 1},
                style={'padding': '5px', 'background-color': '#d1d1d1', 'border-radius': '10px', 'box-shadow': '0px 2px 5px #949494'},
                ),
            dbc.Col(html.H5('''
                    Since viewer engagement can vary a lot between different channels, this graph focusses on a single YouTube channel. We are using the Channel "Markiplier", because there
                    are a lots of videos with a great variety in length uploaded to the channel. Another factor that influenced our choice is the ammount of YouTube Shorts uploaded to the channel, 
                    since in terms of length/iteraction ration, they are not comparible to regular videos on the platform. On "Markiplier"s channel, there are only 4 Shorts uploaded, so they don't have a noticeable 
                    influence on our data, because the data used on this page contains a total of 5000 Videos. The Barchart shows a clear trend, especially for the average comment values. The shortest videos have 
                    the highest ammount of comments and the longer the video gets, the lower ammount of comments per view gets. For the average like count it can also be said that it is the highest for the 
                    shortest video and the lowest for the longest video, but there is no clear trend for the categories in between.
                    ''' 
                            
                            ))
            ]),
            dbc.Row([
                dbc.Col(html.Hr(style={'margin': '20px 0', 'border': 'none', 'border-top': '1px solid #ccc'}),
                width={'size':10, 'offset':1}
                        )
            ],
            style={'height':'50px'},
            ),
            dbc.Col(
                html.H2('Data displayed as a Boxplot', style={'color': '#dd2b2b'}),
                width={'size': 5, 'offset': 1},
                style={'height':'70px'}
            ),

            dbc.Row(
                dbc.Col(dcc.Dropdown(
                id='duration-drop',
                options=[{'label': 'Comments', 'value': 'Comments'},
                        {'label': 'Likes', 'value': 'Likes'},
                        ],
                        value='Comments',
                        clearable=False
                        ),

                        style={'color': '#262626'},
                        width={'size': 2, 'offset': 1} ),

            ),
            dbc.Row(dbc.Row(html.H5(),style={'height':'20px'})),

            dbc.Row([
                dbc.Col(dcc.Graph(
                id='duration-boxplot',),
                width={'size': 7, 'offset': 1},
                style={'padding': '5px', 'background-color': '#d1d1d1', 'border-radius': '10px', 'box-shadow': '0px 2px 5px #949494'},
                
                ),
                dbc.Col(html.H5('''
                        These boxplots show how the interaction values are distributed in each video length category. In the dropdown menu, you can chose between the comment and the like plots.
                        In these boxplots, you can see that there are many outliers, especially for shorter videos. To filter out extreme points, we removed all entries 
                        in the dataset that are more than 3 times the standard deviation away from the mean. In total, 190 entries were filtered out. Since we already filtered out the outliers that we do not 
                        want to have in our visualization, we are using the linear algorithm for the computation of the boxplots. These boxplots show similar trends to the barchart above. You can see that the 
                        ammount of comments consistently gets lower the longer the videos get, while there also is no clear trend for the likes.
                        '''))
            ]),
            
    ])
            
    ),
    
# Callback

@callback(
    Output('duration-boxplot', 'figure'),
    [Input('duration-drop', 'value')]
)

# Callback Function

def update_duration_box(selected_value):

    if selected_value == 'Comments':


        trace = go.Box(x=boxdf['Length'], y=boxdf['Comment/View'], marker_color='#dd2b2b', name='Boxplot')

        layout = go.Layout(title=f'Boxplot for {selected_value}', xaxis_title='Video Duration in Minutes',yaxis_title='Comments per 1000 Views', plot_bgcolor='#e7e7e7', paper_bgcolor='#d1d1d1')

        return {'data': [trace], 'layout': layout}
    
    elif selected_value == 'Likes' :

        trace2 = go.Box(x=boxdf['Length'], y=boxdf['Like/View'],  name='Boxplot2')

        layout = go.Layout(title=f'Boxplot for {selected_value}',xaxis_title='Video Duration in Minutes',yaxis_title='Likes per 1000 Views', plot_bgcolor='#e7e7e7', paper_bgcolor='#d1d1d1')

        return{'data': [trace2], 'layout': layout}


