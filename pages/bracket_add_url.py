# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx, set_props
import dash_bootstrap_components as dbc
import pandas as pd
import json
import melee_db as melee_db
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

# IDs
def stringify_id(id_):
    if isinstance(id_, dict):
        return json.dumps(id_, sort_keys=True, separators=(",", ":"))
    return id_

# ========= Input Components =========
missing_feedback = dbc.FormFeedback("Field is required", type='invalid')

type_id = {'type': 'radio-field', 'id': 'source-radio'}
bracket_type_input = html.Div(
    [
        dbc.Label("Source Website", html_for=stringify_id(type_id),size='lg', className='mb-1'),
        dbc.RadioItems(
            options=["Start.gg", "Challonge"],
            id=type_id,
            inline=True
        )
    ],
    className='mb-3'
)
url_id= {'type': 'input-field', 'id': 'url-input'}
url_input = html.Div(
    [
        dbc.Label("Bracket URL", size='lg', className='mb-1'),
        dbc.Input(type='url', id=url_id, placeholder="Enter bracket URL"),
        dbc.FormText("Provide the URL for the bracket view page"),
        missing_feedback
    ],
    className='mb-3'
)
# ----- Tournament Info Inputs -----
label_width = 3
input_width = 9
margin = 'mb-4'
name_id = {'type': 'input-field', 'id': 'name-input'}
name_input = dbc.Row(
    [
        dbc.Label("Tournament Name", html_for=stringify_id(name_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=name_id, placeholder="Enter tournament name"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)
#date_id = {'type': 'date-field', 'id': 'date-input'}
date_input = dbc.Row(
    [
        dbc.Label("Date", html_for='date-input', size='lg', width=label_width),
        dbc.Col([
            dcc.DatePickerSingle(
                id='date-input',
                month_format='MMMM YYYY',
                display_format='MMMM DD, Y',
                clearable=True
            ),
            missing_feedback
        ],
            width=input_width,
            className='dbc'
        )
    ],
    className=margin
)
location_id = {'type': 'input-field', 'id': 'location-input'}
location_input = dbc.Row(
    [
        dbc.Label("Location", html_for=stringify_id(location_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=location_id, placeholder="Enter location"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)
mode_id = {'type': 'select-field', 'id': 'mode-select'}
mode_input = dbc.Row(
    [
        dbc.Label("Tournament Mode", html_for=stringify_id(mode_id), size='lg', width=label_width),
        dbc.Col([
            dbc.Select(
                id=mode_id,
                options=[
                    {'label': 'Single Elimination', 'value': 1},
                    {'label': 'Double Elimination', 'value': 2},
                    {'label': 'Round Robin', 'value': 3},
                ]
            )],
            width=input_width
        )
    ],
    className=margin
)
theme_id = {'type': 'checkbox-field', 'id': 'theme-checkbox'}
theme_input = dbc.Row(
    [
        dbc.Label("Tournament Theme", html_for=stringify_id(theme_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Checkbox(id=theme_id, label="Check if tournament has a special theme", value=False),
                dbc.Input(type='text', id='theme-input', placeholder="Enter theme", disabled=True),
            ],
            width=input_width
        )
    ],
    className=margin
)
winner_id = {'type': 'input-field', 'id': 'winner-input'}
winner_input = dbc.Row(
    [
        dbc.Label("Winner", html_for=stringify_id(winner_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=winner_id, placeholder="Enter name of tournament winner"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)

# URL input form
bracket_url_form = dbc.Form(
    [bracket_type_input, url_input]
)

# Tournament details input form
bracket_info_form = dbc.Form([name_input, date_input, location_input, mode_input, theme_input, winner_input])
bracket_info_group = html.Div([name_input, date_input, location_input, mode_input, theme_input, winner_input])

# submit button
submit_button = html.Div(
    dbc.Button("Submit", id='submit-button', size='lg', color='secondary'),
    className='d-grid col-6 mx-auto my-3'
)

# ========= Final Layout =========
layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Div("Add a New Tournament by URL", className='text-center h1 mt-5 mb-0'))),
        html.Hr(),
        dbc.Row(dbc.Col(bracket_url_form, width=8), justify='center'),
        # info
        dbc.Row(
            dbc.Col(
                [
                    html.Div("Tournament Information", className='text-center h3 mt-3 mb-3'),
                    #html.Hr(),
                    bracket_info_form
                ],
                width=8,
                className='px-5 border border-3 rounded-3'
            ),
            justify='center'
        ),
        dbc.Row(submit_button, className='mt-5'),
        dcc.Location(id='url-redirect', refresh='callback-nav')
    ],
    fluid=True,
)

@callback(
    Output( 'theme-input', 'disabled'),
    Input({'type': 'input-field', 'id': 'theme-checkbox'}, 'value')
)
def toggle_theme_input(is_checked):
    # enable/disable the custom theme input field based on if this box is checked
    return not is_checked


# clear invalid form feedback
@callback(
    Output({'type': 'input-field', 'id': MATCH}, 'invalid'),
    Input({'type': 'input-field', 'id': MATCH}, 'value'),
    State({'type': 'input-field', 'id': MATCH}, 'invalid')
)
def clear_invalid(value, is_invalid):
    if is_invalid:
        # only needs to be updated if invalid is true
        if value is not None and value != '':
            # clear invalid input warning once user inputs any value
            return False

    # if field is already valid or if input value is empty, no update
    raise PreventUpdate


# Form submission callback w/ pattern matching callback
@callback(
    Output('url-redirect', 'href'),
    inputs={
        'n_clicks': Input('submit-button', 'n_clicks'),
        'field_values': State({'type': 'input-field', 'id': ALL}, 'value'),
        'field_ids': State({'type': 'input-field', 'id': ALL}, 'id'),
        'date_value': State('date-input', 'date'),
    },
    prevent_initial_call=True
)
def submit_form_pattern(n_clicks, field_values, field_ids, date_value):
    if n_clicks > 0:
        missing_fields = []
        # get values of all components
        for i, val in enumerate(field_values):
            if val is None or val == '':
                missing_fields.append(i)

        for index in missing_fields:
            set_props(field_ids[index], {'invalid': True})
        pass
    else:
        raise PreventUpdate
