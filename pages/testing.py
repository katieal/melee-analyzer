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

add_theme_button = dbc.Button(
    "Add Theme",
    id='add-theme-btn',
    n_clicks=0
)
theme_input = dbc.Row(
    [
        dbc.Label("Tournament Theme", size='lg', width=label_width),
        dbc.Col(
            [
                add_theme_button
            ],
            id='theme-input-container',
            width=input_width
        )
    ],
    className=margin
)

bracket_info_form = dbc.Form([name_input, theme_input])

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
                color='danger',
                n_clicks=0
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

    prevent_initial_call=True,
)
def add_theme(add_clicks):
    if add_clicks > 0:
        patched_children = Patch()
        #cn = 'mt-2' if len(children) >= 1 else ''
        # delete add theme button
        del patched_children[0]
        # add theme input field
        patched_children.append(get_field(add_clicks, ''))
        return patched_children
    else:
        raise PreventUpdate


@callback(
    Output('theme-input-container', 'children', allow_duplicate=True),
    Input({'type': 'theme-remove-button', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def del_theme(clicks):
    if clicks[0] > 0:
        patched_children = Patch()
        # delete input field
        del patched_children[0]
        # insert add theme button
        patched_children.append(add_theme_button)
        return patched_children
    else:
        raise PreventUpdate