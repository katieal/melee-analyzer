# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx, set_props
import dash_bootstrap_components as dbc
import pandas as pd
import json
import re
import dash_daq as daq
import melee_data
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

# IDs
def stringify_id(id_):
    if isinstance(id_, dict):
        return json.dumps(id_, sort_keys=True, separators=(",", ":"))
    return id_


# ========= General Components =========
missing_feedback = dbc.FormFeedback("Field is required", type='invalid')
max_url_length = 100
max_input_length = 30
label_width = 3
input_width = 9
margin = 'mb-4'
input_patterns = {
    'Start.gg': [r'^https://www.start.gg/'],
    'Challonge': [r'^https://challonge.com/', r'^https://www.challonge.com/'],
    'Other': [r'^https://']
}

def get_feedback(div_id):
    return dbc.FormFeedback(
        "Field is required",
        type='invalid',
        id={'type': 'form-feedback', 'element': div_id},
    )

# =============================================
# ========= Tournament Info Fields =========
# =============================================
name_id = {'type': 'input-field', 'element': 'name-input', 'key': 'name'}
name_input = dbc.Row(
    [
        dbc.Label("Tournament Name", html_for=stringify_id(name_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=name_id, maxlength=max_input_length, placeholder="Enter tournament name"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)
date_id = {'type': 'alt-input-field', 'element': 'date-picker'}
date_input = dbc.Row(
    [
        dbc.Label("Date", html_for=stringify_id(date_id), size='lg', width=label_width),
        dbc.Col([
            dcc.DatePickerSingle(
                id=date_id,
                month_format='MMMM YYYY',
                display_format='MMMM DD, Y',
                clearable=True
            ),
            dbc.Input(type='hidden', id={'type': 'input-hidden', 'element': 'date-picker'}),
            missing_feedback
        ],
            width=input_width,
            className='dbc'
        )
    ],
    className=margin
)
location_id = {'type': 'input-field', 'element': 'location-input', 'key': 'location'}
location_input = dbc.Row(
    [
        dbc.Label("Location", html_for=stringify_id(location_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=location_id, maxlength=max_input_length, placeholder="Enter location"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)
format_id = {'type': 'input-field', 'element': 'format-select', 'key': 'format'}
format_input = dbc.Row(
    [
        dbc.Label("Tournament Format", html_for=stringify_id(format_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Select(
                    id=format_id,
                    options=[
                        {'label': "Single Elimination", 'value': "single_elim"},
                        {'label': "Double Elimination", 'value': "double_elim"},
                        {'label': "Round Robin", 'value': "robin"},
                    ],
                    # placeholder text in this field doesn't have the same muted appearance as the placeholders
                    # in input fields which looks weird so omitting it for now
                    # placeholder="Select tournament format"
                ),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)
add_theme_button = dbc.Button(
    [
        html.I(className='fa-solid fa-plus me-3'),
        "Add Theme"
    ],
    id={'type': 'dynamic-add', 'element': 'theme'},
    n_clicks=0
)
theme_input_field = html.Div([
    dbc.InputGroup([
        dbc.Input(
            type='text',
            id={
                'type': 'input-field',
                'element': 'theme-input',
                'key': 'theme'
            },
            maxlength=max_input_length,
            placeholder="Enter theme",
        ),
        dbc.Button(
            [html.I(className='fa-solid fa-minus')],
            id={'type': 'dynamic-delete', 'element': 'theme'},
            color='danger',
            n_clicks=0
        )
    ]),
    missing_feedback
])
theme_id = {'type': 'dynamic-input', 'element': 'theme'}
theme_input = dbc.Row(
    [
        dbc.Label("Tournament Theme", size='lg', width=label_width),
        dbc.Col(
            [
                add_theme_button
            ],
            id=theme_id,
            width=input_width
        )
    ],
    className=margin
)
winner_id = {'type': 'input-field', 'element': 'winner-input', 'key': 'winner'}
winner_input = dbc.Row(
    [
        dbc.Label("Winner", html_for=stringify_id(winner_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=winner_id, maxlength=max_input_length, placeholder="Enter name of tournament winner"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)

# =============================================
# ========= Bracket Info Fields =========
# =============================================
type_id = {'type': 'alt-input-field', 'element': 'source-radio'}
website_input = html.Div(
    [
        dbc.Label("Source Website", html_for=stringify_id(type_id),size='lg', className='mb-1'),
        dbc.RadioItems(
            options=["Start.gg", "Challonge", "Other"],
            id=type_id,
            inline=True
        ),
        dbc.Input(type='hidden', id={'type': 'input-hidden', 'element': 'source-radio'}),
        missing_feedback
    ],
    className='mb-3'
)
url_input = html.Div(
    [
        dbc.Label("Bracket URL", html_for='url-input', size='lg', className='mb-1'),
        dbc.Input(
            type='url',
            id='url-input',
            maxlength=max_url_length,
            inputmode='url',
            placeholder="Enter bracket URL",
            disabled=True
        ),
        dbc.FormText("Provide the URL for the bracket view page (must select source website first)", id='url-form-text'),
        dbc.FormFeedback(
            "Invalid value",
            type='invalid',
            id='url-form-feedback'
        ),
        dbc.Popover(
            [
                dbc.PopoverBody("All URLs must start with \"https://\""),
                dbc.PopoverBody("Start.gg URLs must start with \"https://www.start.gg/\""),
                dbc.PopoverBody("Challonge URLs must start with \"https://challonge.com/\"")
            ],
            target='url-form-text',
            trigger='hover focus'
        )
    ],
    id='url-input-container',
    className='opacity-50'
)
web_input_header = html.Div(
    [
        html.Div("Add by Website URL", className='text-center h4'),
        dbc.Button(
            [html.I(className='fa-solid fa-minus')],
            id={'type': 'dynamic-delete', 'element': 'website'},
            color='danger',
            n_clicks=0,
            className='position-absolute end-0 align-self-center'
        )
    ],
    className='d-flex flex-row justify-content-center position-relative '
)
add_web_button = html.Div([
    dbc.Button(
        [
            html.I(className='fa-solid fa-plus me-3'),
            "Add by Website URL"
        ],
        id={'type': 'dynamic-add', 'element': 'website'},
        color='info',
        n_clicks=0
    )],
    className='d-grid col-6 mx-auto'
)
web_input = dbc.Row(
    [
        add_web_button
    ],
    id={'type': 'dynamic-input', 'element': 'website'},
    justify='center',
    className=margin
)

# =========================================
# ======== Match Data Input Fields ========
# =========================================
max_name_length = 20

# ==== Add Manual Bracket Section ====
bracket_input_header = html.Div(
    [
        html.Div("Add Bracket Data Manually", className='text-center h4'),
        dbc.Button(
            [html.I(className='fa-solid fa-minus me-3'), "Remove Section"],
            id={'type': 'dynamic-delete', 'element': 'bracket'},
            color='danger',
            n_clicks=0,
            className='position-absolute end-0 align-self-center'
        )
    ],
    className='d-flex flex-row justify-content-center position-relative'
)
bracket_display_option = html.Div(
    [
        dbc.Switch(
            id='bracket-display-switch',
            label="Always display manual data",
            value=False
        )
    ]
)
add_manual_button = html.Div([
    dbc.Button(
        [
            html.I(className='fa-solid fa-plus me-3'),
            "Add Bracket Information Manually"
        ],
        id={'type': 'dynamic-add', 'element': 'bracket'},
        color='info',
        n_clicks=0
    )],
    className='d-grid col-6 mx-auto'
)
manual_bracket_input = dbc.Row( # input for entire bracket data section
    [
        add_manual_button
    ],
    id={'type': 'dynamic-input', 'element': 'bracket'},
    justify='center',
    className=margin
)

# ====================
# BRACKET BUILDER
# ====================

# Match data
def make_add_match_button(round_index):
    return html.Div(
        [
            dbc.Button(
                [
                    html.I(className='fa-solid fa-circle-plus fa-2xl')
                ],
                id={'type': 'add-match-button', 'round': round_index},
                size='lg',
                n_clicks=0,
                className='bg-transparent border border-0',
                style={
                    'boxShadow': 'none'
                }
            )
        ],
        className='d-flex justify-content-center'
    )


def get_player_input(round_index, match_index, player_num):
    """
    Get input fields for a single player name and score
    :param round_index: Round number
    :param match_index: Match index
    :param player_num: 1 = score is right of name, 2 = score is left of name
    :return: dbc.Stack
    """
    player_name_input = dbc.Input(
        id={'type': 'player-name', 'round': round_index, 'match': match_index, 'player': player_num},
        placeholder=f"Player {player_num} Name",
        type='text',
        #size='lg',
        maxlength=max_name_length,
        className='my-1 bg-transparent'
    )
    score_input = dbc.Input(
        id={'type': 'player-score', 'round': round_index, 'match': match_index, 'player': player_num},
        placeholder=0,
        type='number',
        max=9,
        min=0,
        #size='lg',
        className='my-1 pe-0 bg-transparent text-center',
        style={'width': '62px'}
    )

    stack = dbc.Stack(
        [
            player_name_input if player_num == 1 else score_input,
            html.Div(className='vr bg-info', style={'width': '4px'}),
            score_input if player_num == 1 else player_name_input
        ],
        direction='horizontal'
    )
    return stack


def get_match_row(round_index, match_index):
    content = html.Div(
        [
            html.Div(
                [
                    html.Div(get_player_input(round_index, match_index, 1),
                            className='d-grid col-4 pe-0 border border-info border-2 rounded-3'),
                    html.Div(html.H3("VS", className='mb-0'),  className='d-grid col-1 p-0 text-center align-self-center'),
                    html.Div(get_player_input(round_index, match_index, 2),
                            className='d-grid col-4 ps-0 border border-info border-2 rounded-3'),
                    dbc.Button(
                        [html.I(className='fa-solid fa-minus')],
                        id={'type': 'delete-match-button', 'round': round_index, 'element': match_index},
                        color='danger',
                        n_clicks=0,
                        className='position-absolute end-0 align-self-center'
                    ),
                ],
                className='d-flex flex-row justify-content-center position-relative'
            ),
            # divider
            dbc.Row(
                dbc.Col(
                    [html.Hr(className='border border-1 border-primary')],
                    width=10
                ),
                justify='center'
            )
        ],
    )
    return content

# ---- Round Data ----
def make_delete_round_modal(round_index):
    content = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Confirm Deletion"), close_button=True),
            dbc.ModalBody("Are you sure you want to delete this round? This action will also delete all matches associated with this round. This action cannot be undone."),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Confirm",
                        id={'type': 'modal-confirm', 'element': 'round'},
                        n_clicks=0,
                    ),
                    dbc.Button(
                        "Cancel",
                        n_clicks=0,
                    )
                ]
            )
        ],
        id='delete-confirm-modal',
        centered=True,
        is_open=False
    )


def make_delete_round_button(round_index):
    btn = dbc.Button(
        [html.I(className='fa-solid fa-minus me-2'), "Delete Round"],
        id={'type': 'delete-round-button', 'round': round_index},
        color='danger',
        size='sm',
        n_clicks=0,
        className='ms-auto'
    )
    return html.Div(
        [

            dbc.Collapse(
                dcc.ConfirmDialogProvider(
                    btn,
                    id={'type': 'delete-round-confirm', 'round': round_index},
                    message="Are you sure????"
                ),
                id={'type': 'round-info-collapse', 'round': round_index},
                is_open=False,
                #dimension='width'
                className='me-2'
            ),
            dbc.Button(
                html.I(className='fa-solid fa-angle-down'),
                id={'type': 'round-collapse-button', 'round': round_index},
                size='sm',
                style={
                    'width': '30px'
                }
                #className='fa-solid fa-ellipsis'
            ),
        ],
        className='d-flex justify-content-end'
    )


def make_round_accordion_item(round_index, round_number):
    content = dbc.AccordionItem(
        [
            make_delete_round_button(round_index),
            dbc.Row(
                dbc.Col(
                    [],
                    id={'type': 'match-container', 'round': round_index}  # add/delete matches
                ),
                justify='center',
                className='mt-3'
            ),
            make_add_match_button(round_index),
        ],
        id={'type': 'round-accordion-item', 'round': round_index}, # add/delete rounds
        title= html.Div(f'Round {round_number}', className='fs-5'),
        class_name='border border-1'
    )
    return content


bracket_data_accordion = html.Div(
    [
        dbc.Accordion(
            [
                make_round_accordion_item(0, 1)
            ],
            id='bracket-accordion', # called by add/delete round btn
            always_open=True,
        ),
        html.Div(
            dbc.Button(
                [
                    html.I(className='fa-solid fa-plus me-3'),
                    "Add Round"
                ],
                id='add-round-button',
                n_clicks=0,
                class_name=''
            ),
            className='d-grid col-3 mx-auto my-2 ',
        )
    ],
    className='px-5'
)

# Tournament details input form
tournament_info_form = dbc.Form([name_input, date_input, location_input, format_input, theme_input, winner_input])
# Bracket info input form
# wrap in a col to decrease width?
web_form = dbc.Form(
    [web_input_header, website_input, url_input],
    className='p-4 border border-2 rounded-3')
manual_bracket_form = dbc.Form(
    [
        bracket_input_header,
        bracket_display_option,
        bracket_data_accordion
    ],
    className='p-4 border border-2 rounded-3')


dynamic_fields = {
    "theme": {
        "input": theme_input_field,
        "add_button": add_theme_button
    },
    "website": {
        "input": web_form,
        "add_button": add_web_button
    },
    "bracket": {
        "input": manual_bracket_form,
        "add_button": add_manual_button
    }
}

# submit button
submit_button = html.Div(
    dbc.Button("Submit", id='submit-button', size='lg', color='secondary', n_clicks=0),
    className='d-grid col-6 mx-auto my-3'
)

# invalid field alert box
invalid_alert = dbc.Alert(
    "Submission Failed: Missing or invalid fields!",
    id='invalid-alert',
    color='danger',
    dismissable=True,
    is_open=False,
)

confirm_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle(id='confirm-modal-title'), close_button=True),
        dbc.ModalBody(id='confirm-modal-body'),
        dbc.ModalFooter(
            [
                dbc.Button(
                    "Confirm",
                    id='confirm-modal-yes-button',
                    n_clicks=0
                ),
                dbc.Button(
                    "Cancel",
                    id='confirm-modal-no-button',
                    color='danger',
                    n_clicks=0
                )
            ],
            id='confirm-modal-footer'),
    ],
    id='confirm-modal',
    centered=True,
    is_open=False
)


# ========= Final Layout =========
layout = dbc.Container(
    [
        # title
        dbc.Row(dbc.Col(html.Div("Add a New Tournament by URL", className='text-center h1 mt-5 mb-0'))),
        html.Hr(),
        # info
        dbc.Row(
            dbc.Col(
                [
                    html.Div("Tournament Information", className='text-center h3 mt-3 mb-3'),
                    tournament_info_form
                ],
                width=8,
                className='px-5 border border-3 rounded-3'
            ),
            justify='center',
            className='mb-3'
        ),
        # bracket data
        dbc.Row(
            dbc.Col(
                [
                    html.Div("Bracket Information", className='text-center h3 mt-3 mb-3'),
                    web_input,
                    manual_bracket_input
                ],
                width=10,
                className='px-5 border border-3 rounded-3'
            ),
            justify='center'
        ),
        dbc.Row(
            dbc.Col(invalid_alert, width=8),
            justify='center',
            className='mt-4'
        ),
        dbc.Row(submit_button, className='mt-4'),
        # confirm modal
        confirm_modal,
        dcc.Location(id='url-redirect', refresh='callback-nav')
    ],
    fluid=True,
)


@callback(
    Output('bracket-accordion', 'children', allow_duplicate=True),
    Input({'type': 'delete-round-confirm', 'round': ALL}, 'submit_n_clicks'),
    prevent_initial_call=True
)
def delete_round(submit_n_clicks):
    if not submit_n_clicks:
        raise PreventUpdate
    else:
        # get index of triggered button
        index = 0
        for i, button in enumerate(ctx.inputs_list[0]):
            if button['id'] == ctx.triggered_id:
                index = i
                break

        if submit_n_clicks[index]:
            patched_children = Patch()
            del patched_children[index]
            return patched_children
        else:
            raise PreventUpdate


"""
@callback(
    Output('confirm-modal', 'is_open', allow_duplicate=True),
    inputs={
        'delete_clicks': Input({'type': 'delete-round-button', 'round': ALL}, 'n_clicks'),
        'confirm_clicks': Input('confirm-modal-yes-button', 'n_clicks'),
        'is_open': State('confirm-modal', 'is_open')
    },
    prevent_initial_call=True
)
def confirm_delete_round(delete_clicks, confirm_clicks, is_open):

    btn_clicked = ctx.triggered_id.type if type(ctx.triggered_id) == dict else ctx.triggered_id

    # open confirm modal
    if btn_clicked == 'delete-round-button':
        # get index of triggered button
        index = 0
        for i, button in enumerate(ctx.inputs_list[0]):
            if button['id'] == ctx.triggered_id:
                index = i
                break

        # check clicks for triggered button
        if delete_clicks[index] > 0:
            print("open passed: ", not is_open)

            title = "Confirm Deletion"
            body = ("Are you sure you want to delete this round? All matches associated with this round will "
                    "also be deleted. This action cannot be undone.")

            # set modal props
            set_props('confirm-modal-title', {'children': title})
            set_props('confirm-modal-body', {'children': body})

            return not is_open

        else:
            raise PreventUpdate

    elif btn_clicked == 'confirm-modal-yes-button':

        # delete associated row

    else:
        print("open not passed: ", is_open)
        raise PreventUpdate


@callback(
    Output('confirm-modal', 'is_open', allow_duplicate=True),
    Input('confirm-modal-no-button', 'n_clicks'),
    State('confirm-modal', 'is_open'),
    prevent_initial_call=True
)
def close_confirm_modal(n_clicks, is_open):
    if n_clicks:
        print("close passed: ", not is_open)
        return not is_open
    else:
        print("close not passed: ", is_open)
        raise PreventUpdate
"""


@callback(
    Output({'type': 'round-info-collapse', 'round': MATCH}, 'is_open'),
    Output({'type': 'round-collapse-button', 'round': MATCH}, 'children'),
    Input({'type': 'round-collapse-button', 'round': MATCH}, 'n_clicks'),
    State({'type': 'round-info-collapse', 'round': MATCH}, 'is_open'),
    prevent_initial_call=True
)
def toggle_round_collapse(n_clicks, is_open):
    if n_clicks:
        closed = html.I(className='fa-solid fa-angle-down')
        opened = html.I(className='fa-solid fa-angle-left')

        return not is_open, closed if is_open else opened
    else:
        raise PreventUpdate


@callback(
    Output('bracket-accordion', 'children', allow_duplicate=True),
    Input('add-round-button', 'n_clicks'),
    State('bracket-accordion', 'children'),
    prevent_initial_call=True
)
def add_round(n_clicks, items):
    if n_clicks > 0:
        patched_children = Patch()
        patched_children.append(make_round_accordion_item(n_clicks, len(items) + 1)) # calculate round num
        return patched_children
    else:
        return PreventUpdate


@callback(
    Output({'type': 'match-container', 'round': MATCH} , 'children', allow_duplicate=True),
    Input({'type': 'add-match-button', 'round': MATCH}, 'n_clicks'),
    prevent_initial_call=True
)
def add_match(n_clicks):
    if n_clicks > 0:
        patched_children = Patch()
        round_index = ctx.triggered_id.round
        patched_children.append(get_match_row(round_index, n_clicks))
        return patched_children
    else:
        raise PreventUpdate


@callback(
    Output({'type': 'match-container', 'round': MATCH}, 'children', allow_duplicate=True),
    Input({'type': 'delete-match-button', 'round': MATCH, 'element': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def delete_match(n_clicks):
    # get index of triggered button
    index = 0
    for i, button in enumerate(ctx.inputs_list[0]):
        if button['id'] == ctx.triggered_id:
            index = i
            break

    # check if button was actually clicked
    if n_clicks[index] > 0:
        patched_children = Patch()
        del patched_children[index]
        return patched_children
    else:
        raise PreventUpdate


# =========== Add/Delete Dynamic Fields ===========
@callback(
    Output({'type': 'dynamic-input', 'element': MATCH}, 'children', allow_duplicate=True),
    Input({'type': 'dynamic-add', 'element': MATCH}, 'n_clicks'),
    prevent_initial_call=True
)
def add_dynamic_field(n_clicks):
    """
    Delete the Add button and insert Input field
    """
    if n_clicks > 0:
        patched_children = Patch()
        # delete first element (add button)
        del patched_children[0]
        # insert input field
        element = ctx.triggered_id.element
        patched_children.append(dynamic_fields[element]['input'])
        return patched_children
    else:
        raise PreventUpdate

@callback(
    Output({'type': 'dynamic-input', 'element': MATCH}, 'children', allow_duplicate=True),
    Input({'type': 'dynamic-delete', 'element': MATCH}, 'n_clicks'),
    prevent_initial_call=True
)
def delete_dynamic_field(n_clicks):
    """
    Delete the Input field and insert Add button
    """
    # Separate callback to avoid element not found error
    if n_clicks > 0:
        patched_children = Patch()
        # delete first element (input field)
        del patched_children[0]
        # insert add field button
        element = ctx.triggered_id.element
        patched_children.append(dynamic_fields[element]['add_button'])
        return patched_children
    else:
        raise PreventUpdate


# ========= URL Field Callbacks =========
def update_url_error(is_empty):
    """
    Update the URL input field's form feedback to display the correct error message.
    Will display 'Field is required' or 'Invalid format'
    :param is_empty: Is the URL input field empty/null?
    """
    msg = "Field is required" if is_empty else "Invalid website format"
    # set correct message for form feedback
    set_props('url-form-feedback', {'children': msg})

@callback(
    Output('url-input', 'disabled'),
    Output('url-input-container', 'className'),
    Input({'type': 'alt-input-field', 'element': 'source-radio'}, 'value'),
    prevent_initial_call=True
)
def enable_url_input(web_value):
    """
    Enable URL input field after a website radio button is selected
    """
    if web_value is None or web_value == '':
        raise PreventUpdate
    else:
        # enable url input and reset opacity after a website has been selected
        return False, ''


@callback(
    Output('url-input', 'invalid'),
    inputs={
        'url': Input('url-input', 'value'),
        'website': State({'type': 'alt-input-field', 'element': 'source-radio'}, 'value'),
    },
    prevent_initial_call=True
)
def validate_url(url, website):
    """
    Validate URL based on currently selected website and defined URL patterns
    """
    # url box is only enabled after website is selected
    if website is None or website == '':
        raise PreventUpdate
    else:
        # check url against website patterns
        is_invalid = True
        for pattern in input_patterns[website]:
            comp = re.compile(pattern)
            if comp.match(url):
                # break if url matches one of the patterns
                is_invalid = False
                break
        # display correct error message text
        if is_invalid:
            update_url_error(False)
        # set invalid to true if url does NOT match pattern, false if it DOES match
        return is_invalid

"""
# ========== Callbacks to clear missing input alert ==========
# clear invalid form feedback
@callback(
    Output({'type': 'input-field', 'element': MATCH, 'key': MATCH}, 'invalid'),
    Input({'type': 'input-field', 'element': MATCH, 'key': MATCH}, 'value'),
    State({'type': 'input-field', 'element': MATCH, 'key': MATCH}, 'invalid'),
    prevent_initial_call=True
)
def clear_invalid(value, is_invalid):
    if is_invalid:
        # only needs to be updated if invalid is true
        if value is not None and value != '':
            # clear invalid input warning once user inputs any value
            return False

    # if field is already valid or if input value is empty, no update
    raise PreventUpdate
# clear invalid form feedback for radio
@callback(
    Output({'type': 'input-hidden', 'element': 'source-radio'}, 'invalid'),
    Input({'type': 'alt-input-field', 'element': 'source-radio'}, 'value'),
    State({'type': 'input-hidden', 'element': 'source-radio'}, 'invalid'),
    prevent_initial_call=True
)
def clear_invalid_radio(value, is_invalid):
    if is_invalid:
        # only needs to be updated if invalid is true
        if value is not None and value != '':
            # clear invalid input warning once user inputs any value
            return False

    # if field is already valid or if input value is empty, no update
    raise PreventUpdate
# clear invalid form feedback for date
@callback(
    Output({'type': 'input-hidden', 'element': 'date-picker'}, 'invalid'),
    Input({'type': 'alt-input-field', 'element': 'date-picker'}, 'date'),
    State({'type': 'input-hidden', 'element': 'date-picker'}, 'invalid'),
    prevent_initial_call=True
)
def clear_invalid_date(date, is_invalid):
    if is_invalid:
        # only needs to be updated if invalid is true
        if date is not None and date != '':
            # clear invalid input warning once user inputs any value
            return False

    # if field is already valid or if input value is empty, no update
    raise PreventUpdate


# ========== Form submission callback ==========
@callback(
    Output('url-redirect', 'href'),
    Output('data-store', 'data'),
    inputs={
        'n_clicks': Input('submit-button', 'n_clicks'),
        'inputs': {
            'values': State({'type': 'input-field', 'element': ALL, 'key': ALL}, 'value'),
            'ids': State({'type': 'input-field', 'element': ALL, 'key': ALL}, 'id'),
        },
        'alt_inputs': {
            'url_value': State('url-input', 'value'), # maybe change this to a reg input field and add invalid checks for all fields?
            'url_invalid': State('url-input', 'invalid'),
            'source-value': State({'type': 'alt-input-field', 'element': 'source-radio'}, 'value'),
            'date_value': State({'type': 'alt-input-field', 'element': 'date-picker'}, 'date'),
        },
    },
    prevent_initial_call=True
)
def submit_form(n_clicks, inputs, alt_inputs):
    if n_clicks > 0:
        # track if form is ready to submit
        is_form_valid = True
        # build data dict
        data = {}

        # Check for null values in input fields
        missing_fields = []
        for i, val in enumerate(inputs['values']):
            if val is None or val == '':
                # find all fields with empty values
                missing_fields.append(i)
                # flag that form has an invalid field
                is_form_valid = False
            if is_form_valid:
                # add to data dict if form is still valid
                data[inputs['ids'][i]['key']] = val
        for index in missing_fields:
            # set invalid to true if field value is null
            set_props(inputs['ids'][index], {'invalid': True})

        # check if url is valid
        if not alt_inputs['url_invalid']:
            if alt_inputs['url_value'] is None or alt_inputs['url_value'] == '':
                # flag that form has an invalid field
                is_form_valid = False
                set_props('url-input', {'invalid': True})
                # show missing value error msg
                update_url_error(True)
            elif is_form_valid:
                # add to data dict if form is still valid
                data["url"] = alt_inputs['url_value']
        else:
            # url does not match pattern
            is_form_valid = False

        # check radio button for empty value
        if alt_inputs['source-value'] is None or alt_inputs['source-value'] == '':
            # flag that form has an invalid field
            is_form_valid = False
            set_props({'type': 'input-hidden', 'element': 'source-radio'}, {'invalid': True})
        elif is_form_valid:
            data["website"] = alt_inputs['source-value']

        # check date field for empty value
        if alt_inputs['date_value'] is None or alt_inputs['date_value'] == '':
            # flag that form has an invalid field
            is_form_valid = False
            set_props({'type': 'input-hidden', 'element': 'date-picker'}, {'invalid': True})
        elif is_form_valid:
            data["date"] = alt_inputs['date_value']

        # Submit data and redirect if form is valid
        if is_form_valid:
            print("Submission successful!")
            # submit data and display success screen
            melee_data.add_tournament(data)
            return '/bracket-history', {"success_modal": True}
        else:
            print("Submission failed!")
            # display error screen
            set_props('invalid-alert', {'is_open': True})
            return dash.no_update, dash.no_update
    else:
        raise PreventUpdate
"""