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

label_width = 3
input_width = 9
margin = 'mb-4'

name_id = {'type': 'input-field', 'element': 'name-input', 'key': 'name'}
name_input = dbc.Row(
    [
        dbc.Label("Tournament Name", size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=name_id, placeholder="Enter tournament name"),
            ],
            width=input_width
        )
    ],
    className=margin
)

btn = dbc.Button(
    "Add Theme",
    id='add-theme-btn',
)

btn_row = dbc.Row(
    [
        dbc.Col(dbc.Input(disabled=True, className='me-2'), width=8),
        dbc.Col(dbc.Button("Add Theme"), width=4)
    ]
)

btn_stack = dbc.Stack(
    [
        dbc.Input(disabled=True),
        dbc.Button("Add Theme")
    ],
    direction='horizontal',
    gap=2
)

theme_input = dbc.Row(
    [
        dbc.Label("Tournament Theme", size='lg', width=label_width),
        dbc.Col(
            [

            ],
            id='theme-input-container',
            width=input_width
        )
    ],
    className=margin
)

theme_btn_row = dbc.Row(
    [
        dbc.Label('', size='lg', width=label_width),
        dbc.Col(
            btn,
            width=input_width
        )
    ],
    className=margin
)

bracket_info_form = dbc.Form([name_input, theme_input, theme_btn_row])

layout = dbc.Container([
    dbc.Row(dbc.Col(html.Div("Testing", className='text-center h1 mt-5 mb-0'))),
    html.Hr(),
    html.Br(),
    dbc.Row(
        dbc.Col(
            [
                html.Div("Tournament Information", className='text-center h3 mt-3 mb-3'),
                # html.Hr(),
                bracket_info_form
            ],
            width=8,
            className='px-5 border border-3 rounded-3'
        ),
        justify='center'
    ),
])

def get_field(index, class_name):
    field = dbc.InputGroup(
        [
            dbc.Input(
                type='text',
                id={
                    'type': 'input-field',
                    'element': f'theme-input-{index}',
                    'key': 'theme'
                },
                placeholder="Enter theme",
            ),
            dbc.Button(
                "Remove",
                id={
                    'type': 'theme-remove-button',
                    'index': index
                },
                color='danger'
            )
        ],
        id={
            'type': 'theme-input-group',
            'index': index
        },
        className=class_name
    )
    return field


@callback(
    Output('theme-input-container', 'children', allow_duplicate=True),
    Input('add-theme-btn', 'n_clicks'),
    State('theme-input-container', 'children'),
    prevent_initial_call=True,
)
def add_theme(add_clicks, children):
    if add_clicks > 0:
        patched_children = Patch()
        cn = 'mt-2' if len(children) >= 1 else ''
        patched_children.append(get_field(add_clicks, cn))
        return patched_children
    else:
        raise PreventUpdate


@callback(
    Output('theme-input-container', 'children', allow_duplicate=True),
    Input({'type': 'theme-remove-button', 'index': ALL}, 'n_clicks'),
    State({'type': 'theme-input-container', 'index': ALL}, 'children'), # NOT WORKING
    prevent_initial_call=True
)
def del_theme(clicks, children):
    #elif ctx.triggered_id.type == 'theme-remove-button':
        btn_index = ctx.triggered_id.index
        index = 0

        for i, x in enumerate(children):
            if x['id']['index'] == btn_index:
                index = i

        patched_children = Patch()
        del patched_children[index]
        return patched_children