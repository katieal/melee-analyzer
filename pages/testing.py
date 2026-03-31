# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx
import dash_ag_grid as dag
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

# overflowX in style property in a div can enable horizontal scrollbar
bracket_link = 'https://www.start.gg/tournament/pho-tai-melee-134/event/melee-singles/brackets/2210582/3211219'



test_button = dbc.Button(
    "Test Button",
    id='test-btn',
    n_clicks=0,
)

test_input = html.Div(
    daq.NumericInput(
        id='num-input',
        value=0,
        label={'style': {'marginBottom': '0px'}}
    )
)

test_custom = html.Div(
    [
        daq.NumericInput(
            id='custom-num-input',
            value=0,

        )
    ],
)

custom_btn = html.Div(
    html.Button(
        "Test button",

    ),
    className='custom__style'
)

layout = dbc.Container([
    dbc.Row(dbc.Col(html.Div("Testing", className='text-center h1 mt-5 mb-0'))),
    html.Hr(),
    html.Br(),
    dbc.Row(
        dbc.Col(
            [
                html.Div("Tournament Information", className='text-center h3 mt-3 mb-3'),
                test_input,
                test_custom,
                custom_btn
            ],
            width=8,
            className='px-5 border border-3 rounded-3'
        ),
        justify='center'
    ),
])
