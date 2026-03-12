# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, Patch, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import json
import melee_db as melee_db
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

# ======== Divider Lines ========
v_line = html.Div(
    className='border border-2',
    style={
        'height': '80%',
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

del_round_btn_static = html.Div(
    [
        dbc.Button("Delete Round", size='lg', id='del-round-btn-static', n_clicks=0),
    ],
    className='d-flex justify-content-center my-5'
)

def get_del_btn(btn_index:int):
    return html.Div(
    [
        dbc.Button("Delete Round",
                   size='lg',
                   id={'type': 'delete-round-btn', 'index': btn_index},
                   n_clicks=0),
    ],
    className='d-flex justify-content-center my-5'
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
            ], class_name=player_score_border)
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

def get_round_header(round_num:int):
    # could add an id to this to update round num after deleting specific row
    title = "Round " + str(round_num)
    return dbc.Stack(
    [
        html.Div(title, className='h3 text-secondary mb-0 mx-auto'),
        html.Div(h_line, className='d-flex justify-content-center')
    ]
)

def get_round_stack(match_count:int):
    content = []
    for i in range(match_count):
        content.append(html.Div(match_score, className='flex-fill'))

    return dbc.Stack(
        content,
        gap=3,
        className='mt-3 mb-3'
    )

def get_round_col(round_num:int, match_count:int, col_index:int):
    return html.Div(
        [
            get_round_header(round_num),
            get_round_stack(match_count),
            html.Div(add_match_btn, className='my-5'),
            #get_del_btn(col_index),
        ],
        id={
            'type': 'round-col',
            'index': col_index
        },
        className='my-2'
    )

layout = dbc.Container([
    dbc.Row(dbc.Col(html.Div("Add a New Tournament", className='text-center h1 mt-4'))),
    dbc.Row(html.Hr(), className='mx-5'),
    dbc.Row(
        [
            dbc.Col(get_round_col(1, 2, 0), width=3),
            dbc.Col(v_line, width='auto'),
            dbc.Col([add_round_btn, del_round_btn_static], width=3),
        ],
        id='bracket-container',
        style={'overflow-x': 'scroll', 'overflow-y': 'visible'},
        className='mt-2 mx-2 flex-nowrap',
    )
    ],
    fluid=True,
)

@callback(
    Output('bracket-container', 'children'),
    Input('add-round-button', 'n_clicks'),
    Input('del-round-btn-static', 'n_clicks'),
    State({'type': 'round-col', 'index': ALL}, 'children'),
    prevent_initial_call=True,
)
def update_rounds(add_btn, del_btn, round_cols):
    triggered_id = ctx.triggered_id

    if triggered_id == 'add-round-button':

        patched_children = Patch()
        patched_children.insert(-1, dbc.Col(get_round_col(len(round_cols) + 1, 1, add_btn), width=3))
        patched_children.insert(-1, dbc.Col(v_line, width='auto'))

        return patched_children
    elif triggered_id == 'del-round-btn-static':

        patched_children = Patch()

        # delete most recently added round
        del patched_children[-2]
        del patched_children[-2]

        return patched_children

    raise PreventUpdate