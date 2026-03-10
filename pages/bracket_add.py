# Import Packages
import dash
from dash import Dash, html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import json
import melee_db as melee_db
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

# ======== Divider Lines ========
v_line = html.Div(
    className='mt-4 border border-2',
    style={
        'height': '100%',
        'width': '0px'
    }
)

h_line = html.Div(
    className='border border-1 mb-2',
    style={
        'height': '0px',
        'width': '75%',
    }
)

# ======== Buttons ========
add_match_btn = html.Div(
    [
        dbc.Button("Add Match", size='lg', id='add-match-button', n_clicks=0)
    ],
    className='d-flex justify-content-center'
)

add_round_btn = html.Div(
    [
        dbc.Button("Add Round", size='lg', id='add-round-button', n_clicks=0),
    ],
    className='d-flex justify-content-center'
)

# ======== Matches ========
player_name_border = 'border border-2 rounded-start-3 border-end-0'
player_score_border = 'border border-2 rounded-end-3 border-start-0'
bg_fill_class = 'bg-light border border-2'

team_score = dbc.ListGroup(
    [
        dbc.ListGroupItem("Player Name", class_name='flex-fill ' + player_name_border),
        dbc.ListGroupItem("3", color='success', class_name=player_score_border)
    ],
    horizontal=True,
    class_name='flex-fill mb-2'
)

match_score = [
    dbc.ListGroup(
        [
            dbc.ListGroupItem([
                dbc.Input(placeholder="Player Name", type='text')
            ], class_name='flex-fill ' + player_name_border),
            dbc.ListGroupItem([
                dbc.Input(placeholder=0, type='text', html_size='1',
                          className='')
            ], color='success', class_name=player_score_border)
        ],
        horizontal=True,
        class_name='flex-fill mb-2'
    ),
    dbc.ListGroup(
        [
            dbc.ListGroupItem("Player Name", class_name='flex-fill ' + player_name_border),
            dbc.ListGroupItem("0", color='danger', class_name=player_score_border)
        ],
        horizontal=True,
        class_name='flex-fill'
    )
]

round_header = dbc.Stack(
    [
        html.Div("Round 2", className='h3 text-secondary mb-0 mx-auto'),
        html.Div(h_line, className='d-flex justify-content-center')
    ]
)

round_stack = html.Div(
    [
        round_header,
        dbc.Stack(
            [
                html.Div(
                    match_score,
                    className='flex-fill'
                ),
            ],
            id='round-stack',
            gap=3,
            className='mt-3 mb-3'
        ),
        add_match_btn
    ],
    className='my-2'
)


layout = dbc.Container([
    dbc.Row(dbc.Col(html.Div("Add a New Tournament", className='text-center h1 mt-4'))),
    dbc.Row(html.Hr(), className='mx-5'),
    dbc.Row(
        [
            dbc.Col(round_stack, width=3),
            dbc.Col(v_line, width='auto'),
            dbc.Col(round_stack, width=3),
            dbc.Col(v_line, width='auto'),
            dbc.Col(add_round_btn, width=3),
        ],
        className='mt-2 mx-2'
    )
])