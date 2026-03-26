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

success_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            "Tournament added!",
            class_name='bg-secondary border rounded-3'
        ),
    ],
    #id='success-modal',
    size='sm',
    is_open=False,
    backdrop_class_name='bg-transparent'
)

layout = dbc.Container([
    dbc.Row(dbc.Col(html.Div("Testing", className='text-center h1 mt-5 mb-0'))),
    success_modal,
    html.Hr(),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                [
                    test_button
                ],
                width='auto',
                #className='d-flex vh-100'
            )
        ],
        align='center',
    ),
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