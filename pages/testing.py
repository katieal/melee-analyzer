# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate
import json

dash.register_page(__name__)

# overflowX in style property in a div can enable horizontal scrollbar
bracket_link = 'https://www.start.gg/tournament/pho-tai-melee-134/event/melee-singles/brackets/2210582/3211219'

layout = dbc.Container(
    [
        # title
        dbc.Row(dbc.Col(html.Div("Testing", className='text-center h1 mt-5 mb-0'))),
        html.Hr(),

    ],
    fluid=True,
)
