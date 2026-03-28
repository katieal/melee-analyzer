# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx
import dash_ag_grid as dag
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

img_path = 'assets/amyfest7.png'

test_img = html.Img(
    src=img_path,
    alt="Tournament profile image",
    style={
        'width': '100%',
        'height': '100%',
        'objectFit': 'contain'
    }
)

layout = dbc.Container([
    dbc.Row(dbc.Col(html.Div("Testing", className='text-center h1 mt-5 mb-0'))),
    html.Hr(),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                [
                    test_img
                ],
                width=2,
                className='border border-2 vh-100'
            ),
            dbc.Col(
                [
                    test_button
                ],
                width=10,
                className='border border-2'
            )
        ],
        align='center',
    )
])

"""
@callback(
    Output('success-modal', 'is_open'),
    Input('test-btn', 'n_clicks'),
)
def toggle(n_clicks):
    if n_clicks > 0:
        return True
    return dash.no_update
"""