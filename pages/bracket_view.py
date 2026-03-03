# Import Packages
import dash
from dash import Dash, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from melee_db import df
import melee_db as melee_db

dash.register_page(__name__)

# overflowX in style property in a div can enable horizontal scrollbar

player_name_border = 'border border-2 rounded-start-3 border-end-0'
player_score_border = 'border border-2 rounded-end-3 border-start-0'
bg_fill_class = 'bg-light border border-2'

match_single = [
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
]

match_pair = [
    html.Div(match_single, className='flex-fill mt-2 mb-3'),
    html.Div(match_single, className='flex-fill my-2'),
]

def get_match_pair(margin_bottom, margin_top):
    content = [
        html.Div(match_single, className='flex-fill mt-2 ' + margin_bottom),
        html.Div(match_single, className='flex-fill mb-2 ' + margin_top)
    ]
    return content

# NOTE: in future, change to be based on single matches instead
# returns the first column of bracket with specified num of match pairs
# sets the row height
def get_first_match_col(num):
    content = []
    for i in range(num):
        content.append(html.Div(get_match_pair('mb-3', 'mt-3'), className='flex-fill my-2'))

    # return div with matches
    return html.Div(content, className='d-flex flex-column justify-content-evenly')

# return a html.Div with a single match that expands vertically to fill available space
def get_flex_match_single():
    return html.Div(
        html.Div(match_single, className='flex-fill'),
        className='flex-fill d-flex align-items-center'
    )

# return a html.Div with specified number of matches that auto centers and expands vertically
def get_flex_match_col(num):
    content = []
    for i in range(num):
        content.append(get_flex_match_single())
    return html.Div(content, className='d-flex flex-column h-100')

# ======== Connectors ========
base_border_class = 'flex-grow-1 border border-2'
border_top_class = 'border-start-0 border-end-0 border-bottom-0'
border_bottom_class = 'border-start-0 border-end-0 border-top-0'

connector_merge = html.Div(
    [
        html.Div(
            [
                html.Div(className=base_border_class + ' ' + border_bottom_class), # bot
                html.Div(className=base_border_class + ' border-start-0 border-bottom-0'), # top and end
                html.Div(className=base_border_class + ' border-start-0 border-top-0'), # bot and end
                html.Div(className=base_border_class + ' ' + border_top_class) # top
            ],
            className='h-100 d-flex flex-column',
        )
    ],
    className='flex-grow-1'
)

connector_single = html.Div(
    [
        html.Div(
            [
                html.Div(className='flex-grow-1'), # none
                html.Div(className=base_border_class + ' ' + border_bottom_class), # bot
                html.Div(className=base_border_class + ' ' + border_top_class), # top
                html.Div(className='flex-grow-1') # none
            ],
            className='h-100 d-flex flex-column',
        )
    ],
    className='flex-grow-1'
)

connector_merge_grid = html.Div(
    [
        connector_merge,
        connector_single
    ],
    className='flex-grow-1 d-flex flex-row',
)

# return html.Div with specified number of connectors
def get_connector_col(num):
    content = []
    for i in range(num):
        content.append(connector_merge_grid)

    return html.Div(content, className='d-flex flex-column h-100 justify-content-evenly')


# ============= Utility ==================
col_visual = dbc.Col(
    width=1,
    class_name='bg-light border border-2'
)

# ======= Final Layout ==============
match_width = 3
con_width = 1

bracket_grid = html.Div(
    [
        dbc.Col([get_first_match_col(4)], width=match_width, className='pe-0'),
        dbc.Col([get_connector_col(4)], width=con_width, className='ps-0 pe-0'),
        dbc.Col([get_flex_match_col(4)], width=match_width, className='pe-0'),
        dbc.Col([get_connector_col(2)], width=con_width, className='ps-0 pe-0'),
        dbc.Col([get_flex_match_col(2)], width=match_width, className='pe-0'),
        dbc.Col([get_connector_col(1)], width=con_width, className='ps-0 pe-0'),
        dbc.Col([get_flex_match_col(1)], width=match_width, className='pe-0'),
    ],
    className='d-flex flex-row'
)

def build_bracket(bracket_id):
    # returns an array of arrays of matches,

    # should return a bracket_grid
    pass

def layout(bracket_id=None, **kwargs):
    return dbc.Container([
        dbc.Row(dbc.Col(html.Div(f"Bracket {bracket_id} Results", className='text-center h1 mt-5 mb-0'))),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(bracket_grid, width=8, className='ps-0 pe-0')
            ],
            align='center',
        )
    ])

