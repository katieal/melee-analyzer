# Import Packages
import dash
from dash import Dash, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from melee_db import df

dash.register_page(__name__)

# overflowX in style property in a div can enable horizontal scrollbar

player_name_border = 'border border-2 rounded-start-3 border-end-0'
player_score_border = 'border border-2 rounded-end-3 border-start-0'
bg_fill_class = 'bg-light border border-2'

match_lg = html.Div(
    [
        dbc.ListGroup(
            [
                dbc.ListGroupItem("Player Name", class_name='flex-fill ' + player_name_border),
                dbc.ListGroupItem("3", color='success', class_name=player_score_border)
            ],
            horizontal=True,
            class_name='mb-2',
        ),
        dbc.ListGroup(
            [
                dbc.ListGroupItem("Player Name", class_name='flex-fill ' + player_name_border),
                dbc.ListGroupItem("0", color='danger', class_name=player_score_border)
            ],
            horizontal=True,
        )
    ],
    className='pe-0 flex-fill my-4'
)

# Match col
match_flex_col = html.Div(
    [
        match_lg,
        match_lg,
    ],
    className='d-flex flex-column justify-content-evenly',
)

# ======== Connectors ========
connector_line_h = html.Div(className='h-0 w-100 border border-2 align-self-center')

# TODO: make a grid of boxes, use border to draw lines (border top/bot)
connector_line_v = html.Div(className='')

connector_flex_col = html.Div(
    [
        # col 1
        html.Div(
            [
                html.Div( style={"backgroundColor": "red"}, className="flex-grow-1"),
                html.Div( style={"backgroundColor": "orange"}, className="flex-grow-1"),
            ],
            className="h-100 w-50 d-flex flex-column",
        ),
        # col 2
        html.Div(
            [
                html.Div(style={"backgroundColor": "red"}, className="flex-grow-1"),
                html.Div(style={"backgroundColor": "orange"}, className="flex-grow-1"),
            ],
            className="h-100 w-50 d-flex flex-column",
        )
    ],
    className='d-flex flex-row h-100'
)



connector_grid_col = html.Div(
    [
        html.Div(
            [
                html.Div(
                    className="border border-2 flex-grow-1"
                ),
                html.Div(
                    className="border border-2 flex-grow-1"
                ),
                html.Div(
                    className="border border-2 flex-grow-1"
                ),
                html.Div(
                    className="border border-2 flex-grow-1"
                )
            ],
            className="h-100 d-flex flex-column",
        )
    ],
    className="flex-grow-1"
)

connector_r1_lines = html.Div(
    [
        html.Div(
            [
                html.Div( className="border border-2 border-top-5 flex-grow-1"),
                html.Div( className="flex-grow-1"),
                html.Div( className="flex-grow-1"),
                html.Div( className="border border-top-2 flex-grow-1")
            ],
            className="h-100 d-flex flex-column",
        )
    ],
    className="flex-grow-1"
)

connector_grid = html.Div(
    [
        connector_r1_lines,
        connector_grid_col
    ],
    className="h-100 d-flex flex-row",
)


# return a html.div with specified num of connector lines and width
def make_connector_h(num_lines, width, add_visual):
    content = []
    for i in range(num_lines):
        if add_visual:
            content.append(html.Div(connector_line_h, style={'backgroundColor': get_color(i)}, className='d-flex flex-grow-1'))
        else:
            content.append(html.Div(connector_line_h, className='d-flex flex-grow-1'))
    connector = html.Div(content, className=width + ' h-100 d-flex flex-column')
    return connector

def get_color(num):
    if num == 0: return 'red'
    elif num == 1: return 'orange'
    elif num == 2: return 'yellow'
    elif num == 3: return 'green'
    elif num == 4: return 'blue'
    elif num == 5: return 'purple'
    return 'white'

# ============= Utility ==================
col_visual = dbc.Col(
    width=1,
    class_name='bg-light border border-2'
)
# ===============================

layout = dbc.Container([
    dbc.Row(dbc.Col(html.Div("Bracket Results", className='text-center h1 mt-5 mb-0'))),
    html.Hr(),
    html.Br(),
    dbc.Row(
        [
            dbc.Col([match_flex_col], width=3, className='pe-0'),
            dbc.Col([connector_grid], width=1, className='ps-0'),
            #dbc.Col(make_connector_h(4, 'w-25', True), width=1, className='ps-0'),
            #dbc.Col(make_connector_h(2, 'w-25', True), width=1, className='ps-0'),
            col_visual
        ],
        justify='start'
    )
])

