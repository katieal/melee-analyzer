import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path='/')

# Components
header = html.Div([
    dbc.Row(dbc.Col(html.Div("Melee Homepage", className='text-center h1 mt-5'))),
])


# Info Cards
next_tournament_info = dbc.CardGroup([
    dbc.Card(
        dbc.CardBody([
            html.H4("Date", className='card-title text-center'),
            html.H5("MM/DD/YYYY", className='card-text text-center')
        ]),
        color='primary'
    ),
    dbc.Card(
        dbc.CardBody([
            html.H4("Time", className='card-title text-center'),
            html.H5("00:00 PM", className='card-text text-center')
        ]),
        color='primary'
    ),
    dbc.Card(
        dbc.CardBody([
            html.H4("Location", className='card-title text-center'),
            html.H5("PhoThai", className='card-text text-center')
        ]),
        color='primary'
    )
])


next_tournament_card = dbc.Card([
    dbc.CardHeader("Next Tournament Information", className='text-center h2 mt-3'),
    dbc.CardBody(
        dbc.Row(
            dbc.Col(next_tournament_info, width=11),
            justify='center'
        )
    )],
    color='primary'
)

cards = html.Div([
    dbc.Row(
        [
            dbc.Col(dbc.Card(dbc.CardBody("Most Recent Winner: Name"), color='info', className='text-center h3'), width=5),
            dbc.Col(dbc.Card(dbc.CardBody("Card 2 text"), color='info', className='text-center h3'), width=5),
        ],
        justify='evenly',
        class_name='mt-4 mb-4'
    ),
    dbc.Row(
        dbc.Col(next_tournament_card, width=9),
        justify='center',
        class_name='mb-4'
    )
])


# Final Layout
layout = dbc.Container([
    header,
    html.Hr(),
    cards,
    html.Hr()
])