import os
import json
import pandas as pd

import dash
import dash_bootstrap_components as dbc
import plotly.express as px

from dash import dcc, html, callback
from geopy.geocoders import Nominatim
from dash.dependencies import Input, Output
from datetime import datetime, timedelta


# Register the page with the specified name
dash.register_page(__name__, name='Trends')

# Initialize geolocator for country coordinates
geolocator = Nominatim(user_agent="country_locator")

# Load Europe GeoJSON data
with open('data/europe.geojson', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Define data folder and EU countries ISO2 codes
data_folder = 'data/Trends100vRegions'
eu_countries_iso2 = {
    'Austria': 'AT',
    'Australia': 'AU',
    'Belgium': 'BE',
    'Brazil': 'BR',
    'Bulgaria': 'BG',
    'Canada': 'CA',
    'Croatia': 'HR',
    'Cyprus': 'CY',
    'Czech Republic': 'CZ',
    'Denmark': 'DK',
    'Estonia': 'EE',
    'Finland': 'FI',
    'France': 'FR',
    'Germany': 'DE',
    'Greece': 'GR',
    'Hungary': 'HU',
    'India': 'IN',
    'Ireland': 'IE',
    'Italy': 'IT',
    'Japan': 'JP',
    'Latvia': 'LV',
    'Lithuania': 'LT',
    'Luxembourg': 'LU',
    'Malta': 'MT',
    'Netherlands': 'NL',
    'Niger': 'NG',
    'Poland': 'PL',
    'Portugal': 'PT',
    'Romania': 'RO',
    'Slovakia': 'SK',
    'Slovenia': 'SI',
    'Spain': 'ES',
    'Sweden': 'SE',
    'United Kingdom': 'GB',
    'USA': 'US',
}

# Read category options from a CSV file
category_options = pd.read_csv('data/Categories.csv')

# Load data from CSV files in the specified folder
file_list = os.listdir(data_folder)
dfs = []

# Concatenate all CSV files into a single DataFrame
for file_name in file_list:
    if file_name.endswith('.csv'):
        df = pd.read_csv(os.path.join(data_folder, file_name))
        df['Country'] = file_name[:2]
        dfs.append(df)
weekly_df = pd.concat(dfs, ignore_index=True)

# Function to get coordinates of a country
def get_country_coordinates(country):
    location = geolocator.geocode(country)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Load initial data for pie chart
pie_data = pd.read_csv(f'{data_folder}/DE_category_distribution.csv')
df_selected_date = pie_data[pie_data['Execution Date'] == '2024-03-15']
selected_pie_data = df_selected_date.groupby('Category Title')['Quantity'].sum().reset_index()
pie_first_data = px.pie(selected_pie_data, values='Quantity', names='Category Title',
                        hover_data={'Category Title': False, 'Quantity': True}, hover_name='Category Title')
pie_first_data.update_traces(hovertemplate='Quantity')


# ///////////////Layout//////////////////

layout = html.Div([
    # Header
    dbc.Row(
        [
            dbc.Col(
                html.H2('Youtube Trends Analytics', style={'color': '#dd2b2b'}),
                width={'size': 5, 'offset': 1},
            ),
        ]
    ),
    # Description
    dbc.Row(dbc.Col(html.H5('''
                    Here, you can observe the distribution of categories in the top 100 videos per day and country.
                    The countries available for selection include all EU member states and a selection of interesting countries from each additional continent.
                    The date selection is available within the range where data is present.
                    '''),
                    width={'size': 4, 'offset': 1}
                    ),
            ),
    dbc.Row(dbc.Col(html.H1('''
                    '''),
                    ),
            ),
     # Dropdowns for country and date selection
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': iso2} for country, iso2 in eu_countries_iso2.items()],
                value='DE',
                clearable=False,
                searchable=False,
            ),
            style={'color': '#262626'},
            width={'size': 2, 'offset': 1, 'order': 1}
        ),
        # Date picker
        dbc.Col(
            dcc.DatePickerSingle(
                id='date-picker',
                min_date_allowed=datetime(2024, 3, 6),
                max_date_allowed=(datetime.today() - timedelta(days=1)),
                initial_visible_month=datetime.today(),
                date=(datetime(2024, 3, 15))
            ),
            width={'size': 1, 'offset': 1, 'order': 0}
        ),
    ]),
    # Pie chart and map graph
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='pie-chart', figure=pie_first_data),
            style={'padding': '5px', 'background-color': '#d1d1d1', 'border-radius': '10px', 'box-shadow': '0px 2px 5px #949494'},
            width={'size': 4, 'offset': 1}
        ),
        dbc.Col(
            dcc.Graph(id='map-graph'),
            style={'padding': '5px', 'background-color': '#d1d1d1', 'border-radius': '10px', 'box-shadow': '0px 2px 5px #949494'},
            width={'size': 3, 'offset': 1},
        )
    ],
    className="g-0"),
    dbc.Row([
        dbc.Col(html.Hr(style={'margin': '20px 0', 'border': 'none', 'border-top': '1px solid #ccc'}),
        width={'size':8, 'offset':1}
                )
    ],
    style={'height':'50px'},
    ),
    # Description for weekly graph
    dbc.Row([
        dbc.Col(html.H5('''
                Here, you can view the distribution of individual
                 categories over a few days for the selected country above.
                '''),
                width={'size': 3, 'offset': 1},
                
                )
    ],
    style={'height':'100px'},
    align="start",),
    # Dropdown for category selection
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': category, 'value': category} for category in category_options['Category Title']],
            value='Music',
            clearable=False,
            searchable=False,
            # placeholder="Select a category",
        ),
            style={'color': '#262626'},
            width={'size': 2, 'offset': 1}
        ),
        # dbc.Col(dcc.Graph(id='weekly-graph'), width=4)
    ]),
    dbc.Row([
        dbc.Col(html.H1()
        ),
        # dbc.Col(dcc.Graph(id='weekly-graph'), width=4)
    ]),
    # Weekly graph and description
    dbc.Row([
        dbc.Col(dcc.Graph(id='weekly-graph'), width={'size':4,'offset':1},
            style={'padding': '5px', 'background-color': '#d1d1d1', 'border-radius': '10px', 'box-shadow': '0px 2px 5px #949494'},
        ),
        dbc.Col([html.H5('''
                For several years now, the music industry has established that songs
                and albums are released on the night of Thursday to Friday.
                This is also shown by the trends over the week. On Friday, the number of
                music videos jumps up and then increases even further over the next few days as the
                new music videos are watched there. The proportion then drops again by next Friday.
                
                '''),
                html.Br(),
                html.H5('Unfortunately, on days where there are no values, the Youtube API query failed.'),
        ],width={'size':4})
    ],
    ),
])


# ///////////////Callbacks//////////////////

# Callback to update weekly graph based on category and country selection
@callback(
    Output('weekly-graph', 'figure'),
    [Input('category-dropdown', 'value'),
    Input('country-dropdown', 'value')]
)
def update_weeklygraph(selected_category, selected_country):
    if selected_category and selected_country:
        weekly_df['Execution Date'] = pd.to_datetime(weekly_df['Execution Date'])
        filtered_df = weekly_df[(weekly_df['Category Title'] == selected_category) &
                                (weekly_df['Country'] == selected_country) &
                                (weekly_df['Execution Date'] >= weekly_df['Execution Date'].min()) &
                                (weekly_df['Execution Date'] <= weekly_df['Execution Date'].max())]
        weekly_fig = px.bar(filtered_df, x='Execution Date', y='Quantity', color='Country', title=f'Data for {selected_category} in {selected_country}')
        weekly_fig.update_traces(marker_color='#dd2b2b', hovertemplate='%{y}')
        weekly_fig.update_xaxes(title_text='Date')
        weekly_fig.update_yaxes(title_text='Quantity')
        weekly_fig.update_layout(
            plot_bgcolor='#e7e7e7',
            paper_bgcolor='#d1d1d1',
            showlegend=False)
        return weekly_fig
    else:
        return {}

# Callback to update pie chart based on country and date selection
@callback(
    Output('pie-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('date-picker', 'date')]
)
def update_pie_chart(selected_country, selected_date):
    if selected_country is None or selected_date is None:
        return {}

    file_path = f'{data_folder}/{selected_country}_category_distribution.csv'
    df = pd.read_csv(file_path)

    selected_date = datetime.strptime(selected_date[:10], '%Y-%m-%d')
    df_selected_date = df[df['Execution Date'] == selected_date.strftime('%Y-%m-%d')]

    if df_selected_date.empty:
        return {
            'data': [],
            'layout': {
                'annotations': [{
                    'text': 'No data available for the selected date.',
                    'x': 0.5,
                    'y': 0.5,
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {
                        'size': 25
                    }
                }],
                'showlegend': False,
                'plot_bgcolor': '#d1d1d1',
                'paper_bgcolor': '#d1d1d1',
                'xaxis': {'visible': False},
                'yaxis': {'visible': False}
            }
        }

    df_grouped = df_selected_date.groupby('Category Title')['Quantity'].sum().reset_index()
    pie = px.pie(df_grouped, values='Quantity', names='Category Title', hover_name='Category Title',
                color_discrete_map={
                        'Film & Animation': '#1f77b4',
                        'Autos & Vehicles': '#ff7f0e',
                        'Music': '#2ca02c',
                        'Pets & Animals': '#d62728',
                        'Sports': '#9467bd',
                        'Travel & Events': '#8c564b',
                        'Gaming': '#e377c2',
                        'People & Blogs': '#7f7f7f',
                        'Comedy': '#bcbd22',
                        'Entertainment': '#17becf',
                        'News & Politics': '#aec7e8',
                        'Howto & Style': '#ffbb78',
                        'Education': '#98df8a',
                        'Science & Technology': '#ff9896',
                        'Nonprofits & Activism': '#c5b0d5'})
                        
    pie.update_traces(hovertemplate='%{hovertext}')
    pie.update_layout(
        # showlegend=False,
        plot_bgcolor='#e7e7e7',
        paper_bgcolor='#d1d1d1',
    )
    return pie

# Callback to update map graph based on country selection
@callback(
    Output('map-graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_map(selected_country):
    if selected_country is None:
        return {}

    # Lade die Koordinaten für das ausgewählte Land
    country_lat, country_lon = get_country_coordinates(selected_country)

    # Erstelle eine Karte mit dem ausgewählten Land zentriert
    map_fig = px.choropleth_mapbox(
        color=[1],
        mapbox_style="carto-positron",
        center={"lat": country_lat, "lon": country_lon},
        zoom=3
    )
    map_fig.update_layout(
        plot_bgcolor='#e7e7e7',
        paper_bgcolor='#d1d1d1',
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return map_fig
