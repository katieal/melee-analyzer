import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path='/')

# Components
header = html.Div([
    dbc.Row(dbc.Col(html.Div("Past Bracket Results", class_name='text-center h1 p-2 m-3'))),
])

cards = html.Div([
    dbc.Card(dbc.CardBody([""]))
])

# Final Layout
layout = dbc.Container([
    header,
    html.Hr(),
    dbc.Row(html.Div("Next tournament date: Today!", class_name='text-center h2'))
])