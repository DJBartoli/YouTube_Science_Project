import matplotlib.pyplot as plt
import pandas as pd

import dash
import dash_bootstrap_components as dbc
import plotly.express as px

from dash import dcc, html, callback
from dash.dependencies import Input, Output, State

# register page
dash.register_page(__name__, name='Keyword Analysis')

# specify topics
TOPICS = ['sports', 'gaming', 'lifestyle', 'politics', 'society', 'knowledge']
step_size = 1


def create_image_dataframe():
    """
    this method creates a dataframe storing all the paths for the topic separated wordclouds
    :return: A Dataframe, with columns : topic, year, path
    """
    image_df = pd.DataFrame()
    i = 0

    # define topic specific paths and save them to a dataframe.
    for topic in TOPICS:
        for year in range(2013, 2024):
            path = f'data/keyWordClouds/topicKeyWords/youtube_keywords_{topic}_{year}.png'
            new_row = pd.DataFrame({'topic': topic, 'year': str(year), 'path': path}, index=[i])
            image_df = pd.concat([image_df, new_row])
            i += 1

    # define overall categories paths and save them to a dataframe.
    for year in range(2013, 2024):
        path = f'data/keyWordClouds/yearlyKeyWords/youtube_keywords_{year}.jpg'
        new_row = pd.DataFrame({'topic': 'all categories', 'year': str(year), 'path': path}, index=[i])

        image_df = pd.concat([image_df, new_row], )
        i += 1

    return image_df


topic_images = create_image_dataframe()

# define marks for plot
marks = {str(year): str(year) for year in topic_images['year'].unique()}

layout = html.Div([

    # headline
    dbc.Row(
        [
            dbc.Col(
                children=[html.H2('YouTube through the Years', style={'color': '#dd2b2b'}),
                          html.H3(
                              'Discover the most watched videos according to the keywords. Choose the year and a '
                              'category of interest'),
                          ],
                width={'size': 6, 'offset': 3},

            ),
        ]
    ),

    # text paragraph
    dbc.Row([
        dbc.Col(
            children=[
                html.H5('''We thought it would be interesting to look at how the most popular videos on the platform 
                have changed over the years. Our first approach was to analyze the top 300 videos per year and create 
                a WordCloud representing the yearly results. However, it did not take long to realize that this was 
                not the optimal approach. The results were very disappointing, as there were no trends or interesting 
                real-world events that corresponded to the keywords shown. We came to the conclusion that it was much 
                better to separate the keywords not only by year but also by category. This made the results much 
                more interesting and comprehensive. You can cycle through all the categories and look at the keywords 
                for the year you have chosen. You might find something that brings back memories of the past YouTube 
                landscape. For capacity reasons, we looked at the top 200 videos in each category. You can still see 
                the results of our initial approach.''')
            ],
            width={'size': 6, 'offset': 3},
        ),
    ]),
    # dropdown menu for category selection.
    dbc.Row([
        dbc.Col(
            children=[

                dcc.Dropdown(
                    id='category-dropdown',
                    options=[{'label': topic, 'value': topic} for topic in topic_images['topic'].unique()],
                    value=topic_images['topic'].unique()[0],
                    clearable=False,
                    searchable=False,
                ),
            ],
            width={'size': 6, 'offset': 3},
            style={'color': '#121212', 'margin-top': '20px'}
        ),
    ]),

    # slider to choose the year.
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Slider(
                    id='year-slider',
                    min=2013,
                    max=2023,
                    value=2013,
                    marks=marks,
                    step=step_size,
                    included=True,  # Alle Markierungen werden immer angezeigt
                    tooltip={
                        "always_visible": False,
                        "style": {"color": "#dd2b2b", "fontSize": "20px"},
                    },

                ),
            ],
            width={'size': 5, 'offset': 3},
            style={'margin-top': '5px'},
        ),

        # buttons to clic through the years.
        dbc.Col(
            children=[
                html.Button('◄', id='slider-left', n_clicks=0,
                            style={'font-size': '20px', 'background-color': '#dd2b2b', 'color': '#ffffff',
                                   'border-color': '#ffffff', 'margin-right': '5px',
                                   'border-radius': '10px'}),
                html.Button('►', id='slider-right', n_clicks=0,
                            style={'font-size': '20px', 'background-color': '#dd2b2b', 'color': '#ffffff',
                                   'margin-left': '5px',
                                   'border-radius': '10px', 'border-color': '#ffffff'}),
            ],
            width={'size': 1, 'offset': 0},
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
        ),
    ]),

    # the wordcloud plot
    dbc.Row([
        dbc.Col(
            children=[

                dcc.Graph(id='graph'),

            ],
            width={'size': 6, 'offset': 3},
            style={'padding': '5px', 'background-color': 'white', 'border-radius': '10px',
                   'box-shadow': '0px 2px 5px #949494'},
        )
    ],

    ),
    # word frequency chart
    dbc.Row([
        dbc.Col(
            children=[

                dcc.Graph(id='keyword_frequency_chart'),

            ],
            width={'size': 6, 'offset': 3},
            style={'padding': '5px', 'background-color': 'white', 'border-radius': '10px',
                   'box-shadow': '0px 2px 5px #949494', 'margin-top': '20px'},
        )
    ],

    ),
])


@callback(
    Output('graph', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_wordcloud(topic, year):
    """
        Update the word cloud image based on the selected topic and year.

        :param topic: The selected topic for the word cloud ('all categories' or a specific topic).
        :type topic: str
        :param year: The selected year for the word cloud.
        :type year: int
        :return: Plotly figure object representing the word cloud image.
        :rtype: plotly.graph_objs._figure.Figure
        """
    if topic == 'all categories':
        path = f'data/keyWordClouds/yearlyKeyWords/youtube_keywords_{year}.jpg'
    else:
        path = f'data/keyWordClouds/topicKeyWords/youtube_keywords_{topic}_{year}.jpg'

    img = plt.imread(path)

    fig = px.imshow(img)

    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    return fig


@callback(
    Output('year-slider', 'value'),
    [Input('slider-left', 'n_clicks'),
     Input('slider-right', 'n_clicks')],
    [State('year-slider', 'value')]
)
def update_slider_value(left_clicks, right_clicks, current_value):
    """
        Update the value of the slider based on left or right clicks.

        :param left_clicks: Number of left clicks on the slider.
        :type left_clicks: int
        :param right_clicks: Number of right clicks on the slider.
        :type right_clicks: int
        :param current_value: The current value of the slider.
        :type current_value: int
        :return: The updated value of the slider.
        :rtype: int
        """
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'slider-left' in changed_id:
        return max(current_value - step_size, 2013)
    elif 'slider-right' in changed_id:
        return min(current_value + step_size, 2023)
    return current_value


@callback(
    Output('keyword_frequency_chart', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_word_frequency_chart(topic, year):
    """
        Update the word frequency chart based on the selected topic and year.

        :param topic: The selected topic for the word frequency chart ('all categories' or a specific topic).
        :type topic: str
        :param year: The selected year for the word frequency chart.
        :type year: int
        :return: Plotly figure object representing the word frequency chart.
        :rtype: plotly.graph_objs._figure.Figure
        """
    if topic == 'all categories':
        path = f'data/keyWordClouds/yearlyFrequentWords/frequent_words_{year}.csv'
    else:
        path = f'data/keyWordClouds/topicFrequentWords/frequent_words_{topic}_{year}'

    frequent_words = pd.read_csv(path)

    frequent_words = frequent_words.nlargest(50, 'numbers')

    fig = px.bar(x=frequent_words['numbers'], y=frequent_words['words'], color_discrete_sequence=['#dd2b2b'],
                 orientation='h')
    fig.update_layout(title='Word Frequency',
                      xaxis_title='Frequency',
                      yaxis_title='Word',
                      font=dict(color='black'),  # Farbe der Texte im Diagramm
                      plot_bgcolor='white',  # Hintergrundfarbe des Diagramms

                      )
    return fig
