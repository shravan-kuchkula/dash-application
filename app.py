# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from wrangling_scripts.wrangling import data_wrangling
from dash.dependencies import Input, Output

# get the data from backend, these are defaults
df = data_wrangling('Chelsea', 0)

# define your stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# this is needed for the procfile to deploy to heroku
server = app.server

# Sample markdown text
markdown_text = '''
### Select the **neighbourhood** from the dropdown
'''

app.layout = html.Div(children=[
    html.H1(children='Find similar Airbnb locations in New York City'),

    html.Div([
        dcc.Markdown(children=markdown_text)
    ]),

    html.Div([
    dcc.Dropdown(
        id='dropdown',
        options = [
            {'label': 'Chelsea', 'value': 'Chelsea'},
            {'label': 'West Village', 'value': 'West Village'},
            {'label': 'Greenpoint', 'value': 'Greenpoint'}
        ],
        value='Chelsea'
            )],
        style={'margin-left': '2%', 'width': '48%', 'display': 'inline-block'}
    ),

    html.Div([
    dcc.Graph(
        id='3d-scatter-plot'
        #figure=fig
    )], style={'margin-left': '2%', 'width': '60%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select number of bedrooms'),
        dcc.Slider(
            id='bedroom-slider',
            min=0,
            max=4,
            value=0,
            marks={i: 'Studio' if i==0 else str(i) for i in range(5)},
            step=None
            )],
            style={'margin-left': '2%', 'width': '48%', 'display': 'inline-block', 'color': 'black'}
    )

])

@app.callback(
    Output(component_id='3d-scatter-plot', component_property='figure'),
    [Input(component_id='dropdown', component_property='value'),
    Input(component_id='bedroom-slider', component_property='value')]
)
def update_function(dropdown_input_value, slider_price):

    # filter the dataframe
    df = data_wrangling(dropdown_input_value, slider_price)

    # use that dataframe in the figure
    fig = px.scatter_3d(df, x='TSNE1', y='TSNE2', z='TSNE3', color='price_category',
                    hover_name='name', hover_data=['price', 'bedrooms', 'minimum_nights', 'id'],
                    template='plotly_dark', opacity=0.9, title='Visualizing airbnb locations in feature space',
                    labels={'TSNE1': 'X', 'TSNE2': 'Y', 'TSNE3':'Z'})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
