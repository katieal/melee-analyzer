# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import json
import melee_db as melee_db
from dash.exceptions import PreventUpdate

dash.register_page(__name__)


# ========= Input Components =========
bracket_type_input = html.Div(
    [
        dbc.Label("Source Website", html_for='bracket-source-radio', size='lg', className='mb-1'),
        dbc.RadioItems(
            options=[
                {'label': "Start.gg", 'value': 1},
                {'label': "Challonge", 'value': 2},
            ],
            id='bracket-source-radio',
            inline=True
        )
    ],
    className='mb-3'
)
url_input = html.Div(
    [
        dbc.Label("Bracket URL", html_for='bracket-url', size='lg', className='mb-1'),
        dbc.Input(type='url', id='bracket-url', placeholder="Enter bracket URL"),
        dbc.FormText("Provide the URL for the bracket view page")
    ],
    className='mb-3'
)

bracket_name_input = html.Div(
    [
        dbc.Label("Tournament Name", html_for='bracket-name', size='lg', className='mb-1'),
        dbc.Input(type='text', id='bracket-name', placeholder="Enter tournament name"),
    ],
    className='mb-3'
)
date_input = html.Div(
    [
        dbc.Label("Date", html_for='bracket-date', size='lg', className='mb-1'),
        dcc.DatePickerSingle(
            id='bracket-date',
            month_format='MMMM YYYY',
            display_format='MMMM DD, Y'
        )
    ],
    className='mb-3'
)

bracket_url_form = dbc.Form(
    [bracket_type_input, url_input]
)

# info header
bracket_info_header = html.Div(
    [
        "Tournament Information"

    ]
)
bracket_info_form = dbc.Form([bracket_name_input, date_input])

# ========= Final Layout =========
layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Div("Add a New Tournament by URL", className='text-center h1 mt-5 mb-0'))),
        html.Hr(),
        dbc.Row(dbc.Col(bracket_url_form, width=8), justify='center'),
        # info
        dbc.Row(
            dbc.Col(
                [
                    html.Div("Tournament Information", className='text-center h3 mt-3'),
                    #html.Hr(),
                    bracket_info_form
                ],
                width=8,
                className='px-5 border border-3 rounded-3'
            ),
            justify='center'
        )
    ],
    fluid=True,
)