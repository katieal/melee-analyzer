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

modal = html.Div(
    [
        dbc.Button("Open modal", id="open1", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Header")),
                dbc.ModalBody("This is the content of the modal"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="closer1", className="ms-auto", n_clicks=0)
                ),
            ],
            id="modal1",
            is_open=False,
        ),
    ]
)



layout = dbc.Container([
    dbc.Row(dbc.Col(html.Div("Testing", className='text-center h1 mt-5 mb-0'))),
    html.Hr(),
    html.Br(),
    dbc.Row(
        dbc.Col(
            [
                html.Div("Tournament Information", className='text-center h3 mt-3 mb-3'),
                modal

            ],
            width=8,
            className='px-5 border border-3 rounded-3'
        ),
        justify='center'
    ),
])

"""
@callback(
    Output("modal", "is_open", allow_duplicate=True),
    [Input("open", "n_clicks")],
    [State("modal", "is_open")],
    prevent_initial_call=True
)
def toggle_modal(n1, is_open):

    if n1:
        print("open passed: ", not is_open)
        return not is_open
    print("open not passed: ", is_open)
    return is_open

@callback(
    Output("modal", "is_open", allow_duplicate=True),
    [Input("closer", "n_clicks")],
    [State("modal", "is_open")],
    prevent_initial_call=True
)
def toggle_2(n2, is_open):
    if n2:
        print("close passed: ", not is_open)
        return not is_open
    print("close not passed: ", is_open)
    return is_open
"""