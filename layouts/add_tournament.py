# Import Packages
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from utils.data_utils import stringify_id
import layouts.constants as constants
from layouts.constants import ElementType as EleType

# constants
label_width = 3
input_width = 9
margin = 'mb-4'

missing_feedback = dbc.FormFeedback("Field is required", type='invalid')

# utility method
def get_id(element_type: constants.ElementType, name:str):
    return constants.APP_IDS['add_tournament'][str(element_type)][name]

def make_confirm_delete_button(dialog_id, confirm_message, button_text, button_class):
    """
    Creates dcc.ConfirmDialogProvider wrapped around a red button with a minus sign
    :param dialog_id: ID of the DialogProvider, used to capture user choice. Final ID will be {'type': 'confirm-dialog'} + dialog_id
    :param confirm_message: message to display in the confirm window
    :param button_text: text of the displayed button
    :param button_class: CSS class of the displayed button
    :return: a dcc.ConfirmDialogProvider
    """
    default_id = {'type': 'confirm-dialog'}
    default_id.update(dialog_id)
    btn = dbc.Button(
        [html.I(className='fa-solid fa-minus me-2'), button_text],
        color='danger',
        size='sm',
        n_clicks=0,
        className=button_class
    )
    return dcc.ConfirmDialogProvider(
        btn,
        id=default_id,
        message=confirm_message,
    )

# =============================================
# ========= Tournament Info Fields =========
# =============================================
# Name
name_input = dbc.Row(
    [
        dbc.Label("Tournament Name", html_for=stringify_id(get_id(EleType.INPUT, 'name')), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=get_id(EleType.INPUT, 'name'), maxlength=constants.MAX_INPUT_LENGTH, placeholder="Enter tournament name"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)

# Date
date_input = dbc.Row(
    [
        dbc.Label("Date", html_for=stringify_id(get_id(EleType.INPUT, 'date')), size='lg', width=label_width),
        dbc.Col([
            dcc.DatePickerSingle(
                id=get_id(EleType.INPUT, 'date'),
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

# Location
location_input = dbc.Row(
    [
        dbc.Label("Location", html_for=stringify_id(get_id(EleType.INPUT,'location')), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=get_id(EleType.INPUT, 'location'), maxlength=constants.MAX_INPUT_LENGTH, placeholder="Enter location"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)

# Format
format_input = dbc.Row(
    [
        dbc.Label("Tournament Format", html_for=stringify_id(get_id(EleType.INPUT,'format')), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Select(
                    id=get_id(EleType.INPUT,'format'),
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

# Theme
add_theme_button = dbc.Button(
    [
        html.I(className='fa-solid fa-plus me-3'),
        "Add Theme"
    ],
    id=get_id(EleType.BUTTON,'add_theme'),
    n_clicks=0
)
theme_input_field = html.Div([
    dbc.InputGroup([
        dbc.Input(
            type='text',
            id=get_id(EleType.INPUT, 'theme'),
            maxlength=constants.MAX_INPUT_LENGTH,
            placeholder="Enter theme",
        ),
        dbc.Button(
            [html.I(className='fa-solid fa-minus')],
            id=get_id(EleType.BUTTON,'delete_theme'),
            color='danger',
            n_clicks=0
        )
    ]),
    missing_feedback
])
theme_input = dbc.Row(
    [
        dbc.Label("Tournament Theme", size='lg', width=label_width),
        dbc.Col(
            [
                add_theme_button
            ],
            id=get_id(EleType.CONTAINER, 'theme'),
            width=input_width
        )
    ],
    className=margin
)

# Winner
winner_input = dbc.Row(
    [
        dbc.Label("Winner", html_for=stringify_id(get_id(EleType.INPUT, 'winner')), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=get_id(EleType.INPUT, 'winner'), maxlength=constants.MAX_INPUT_LENGTH, placeholder="Enter name of tournament winner"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)

# Form
#tournament_info_form = dbc.Form([name_input, date_input, location_input, format_input, theme_input, winner_input])
tournament_info_section = html.Div([name_input, date_input, location_input, format_input, theme_input, winner_input])


# ========================
# ----- Website Input ----
# ========================

# ---- Header ----
web_input_header = html.Div(
    [
        html.Div("Add by Website URL", className='text-center h4'),
        dbc.Button(
            [html.I(className='fa-solid fa-minus me-3'), "Remove Section"],
            id=get_id(EleType.BUTTON, 'delete_website'),
            color='danger',
            size='sm',
            n_clicks=0,
            className='position-absolute end-0 align-self-center'
        )
    ],
    className='d-flex flex-row justify-content-center position-relative '
)

# ---- Add Button ----
add_web_button = html.Div([
    dbc.Button(
        [
            html.I(className='fa-solid fa-plus me-3'),
            "Add by Website URL"
        ],
        id=get_id(EleType.BUTTON, 'add_website'),
        color='info',
        n_clicks=0
    )],
    className='d-grid col-6 mx-auto'
)

# ---- Input Fields ----
website_input = html.Div(
    [
        dbc.Label("Source Website", html_for=stringify_id(get_id(EleType.INPUT, 'website')), size='lg', className='mb-1'),
        dbc.Select(
            id=get_id(EleType.INPUT, 'website'),
            options=[
                {'label': "Start.gg", "value": "Start.gg"},
                {'label': "Challonge", "value": "Challonge"},
                {'label': "Other", "value": "Other"}
            ],
            #placeholder="Select Website"
        ),
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
            maxlength=constants.MAX_URL_LENGTH,
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

# ---- Section ----
#web_form = dbc.Form([web_input_header, website_input, url_input])
web_section = html.Div([web_input_header, website_input, url_input])
# Container
web_input_container = dbc.Row(
    [
        add_web_button,
    ],
    id={'type': 'dynamic-input', 'element': 'website'},
    justify='center',
    className=margin
)
# Card Body Content
website_content = dbc.Card(
    dbc.CardBody(
        web_input_container
    ),
    id={'type': 'card-content', 'element': 'website-tab'},
    class_name=''
)

# =========================================
# ========= Manual Input Fields ==========
# =========================================
# ---- Header ----
manual_input_header = html.Div(
    [
        html.Div("Add Bracket Data Manually", className='text-center h4'),
        dbc.Button(
            [html.I(className='fa-solid fa-minus me-3'), "Remove Section"],
            id=get_id(EleType.BUTTON, 'delete_manual'),
            color='danger',
            n_clicks=0,
            size='sm',
            className='position-absolute end-0 align-self-center'
        )
    ],
    className='d-flex flex-row justify-content-center position-relative'
)

# ---- Add Button ----
add_manual_button = html.Div([
    dbc.Button(
        [
            html.I(className='fa-solid fa-plus me-3'),
            "Add Bracket Information Manually"
        ],
        id=get_id(EleType.BUTTON, 'add_manual'),
        color='info',
        n_clicks=0
    )],
    className='d-grid col-6 mx-auto'
)

# ----- Input Fields -----
manual_display_option = html.Div(
    [
        dbc.Switch(
            id='bracket-display-switch',
            label="Always display manual data",
            value=False
        )
    ]
)
bracket_type_select = dbc.Select(
    id=get_id(EleType.INPUT, 'bracket_type'),
    options=[
        {'label': 'Main', 'value': 'Main'},
        {'label': 'Upper Bracket', 'value': 'Upper'},
        {'label': 'Lower Bracket', 'value': 'Lower'},
        {'label': 'Winner\'s Bracket', 'value': 'Winner\'s'},
        {'label': 'Loser\'s Bracket', 'value': 'Loser\'s'}
    ]
)

add_bracket_section = html.Div(
    [
        html.Div(
            dbc.InputGroup([
                dbc.InputGroupText("Select Type"),
                bracket_type_select,
                dbc.Button(
                    [
                        html.I(className='fa-solid fa-plus me-2'),
                        "New Bracket"
                    ],
                    id=get_id(EleType.BUTTON, 'add_bracket'),
                    disabled=True,
                    n_clicks=0
                )
            ], className='w-75'),
            className='d-flex flex-row w-75 justify-content-center py-4',
            style={
                'border': 'dashed',
                'border-radius': '50rem',
                'border-color': 'var(--bs-border-color)'
            }
        )
    ],
    className='d-flex justify-content-center mt-3'
)

# bracket container
bracket_input_container = html.Div(id='bracket-input-container')

# ---- Section ----
#manual_bracket_form = dbc.Form([manual_input_header, manual_display_option, add_bracket_section])
manual_bracket_section = html.Div([manual_input_header, manual_display_option, bracket_input_container, add_bracket_section])
# Container
manual_input_container = dbc.Row( # input for entire bracket data section
    [
        add_manual_button
    ],
    id={'type': 'dynamic-input', 'element': 'bracket'},
    justify='center',
    className=margin
)
# Card Body Content
manual_content = dbc.Card(
    dbc.CardBody(
        manual_input_container,
    ),
    id={'type': 'card-content', 'element': 'manual-tab'},
    class_name='d-none'
)

# ========================
# ----- Bracket Builder ----
# ========================

# Dynamic Field Creators
def make_add_match_button(bracket_index, round_index):
    return html.Div(
        [
            dbc.Button(
                [
                    html.I(className='fa-solid fa-circle-plus fa-2xl')
                ],
                id={'type': 'add-match-button', 'bracket': bracket_index, 'round': round_index},
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

def get_player_input(bracket_index, round_index, match_index, player_num):
    """
    Get input fields for a single player name and score
    :param bracket_index: Bracket index
    :param round_index: Round number
    :param match_index: Match index
    :param player_num: 1 = score is right of name, 2 = score is left of name
    :return: dbc.Stack
    """
    player_name_input = dbc.Input(
        id={'type': 'player-name', 'bracket': bracket_index, 'round': round_index, 'match': match_index, 'player': player_num},
        placeholder=f"Player {player_num} Name",
        type='text',
        #size='lg',
        maxlength=constants.MAX_NAME_LENGTH,
        className='my-1 bg-transparent'
    )
    score_input = dbc.Input(
        id={'type': 'player-score', 'bracket': bracket_index, 'round': round_index, 'match': match_index, 'player': player_num},
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

def get_match_row(bracket_index, round_index, match_index):
    content = html.Div(
        [
            html.Div(
                [
                    html.Div(get_player_input(bracket_index, round_index, match_index, 1),
                            className='d-grid col-4 pe-0 border border-info border-2 rounded-3'),
                    html.Div(html.H3("VS", className='mb-0'),  className='d-grid col-1 p-0 text-center align-self-center'),
                    html.Div(get_player_input(bracket_index, round_index, match_index, 2),
                            className='d-grid col-4 ps-0 border border-info border-2 rounded-3'),
                    dbc.Button(
                        [html.I(className='fa-solid fa-minus')],
                        id={'type': 'delete-match-button', 'bracket': bracket_index, 'round': round_index, 'element': match_index},
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
def make_delete_round_button(bracket_index, round_index):

    dialog_id = {'element': 'delete-round', 'bracket': bracket_index, 'round': round_index}
    msg = ("Are you sure you wish to delete this round? All matches associated "
           "with this round will also be deleted. This action cannot be undone.")

    return html.Div(
        [
            dbc.Collapse(
                make_confirm_delete_button(dialog_id, msg, "Delete Round", 'ms-auto'),
                id={'type': 'round-info-collapse', 'bracket': bracket_index, 'round': round_index},
                is_open=False,
                className='me-2'
            ),
            dbc.Button(
                html.I(className='fa-solid fa-angle-down'),
                id={'type': 'round-collapse-button', 'bracket': bracket_index, 'round': round_index},
                size='sm',
                style={
                    'width': '30px'
                }
                #className='fa-solid fa-ellipsis'
            ),
        ],
        className='d-flex justify-content-end'
    )

def make_round_accordion_item(bracket_index, round_index, round_number=None):
    content = dbc.AccordionItem(
        [
            make_delete_round_button(bracket_index, round_index),
            dbc.Row(
                dbc.Col(
                    [],
                    id={'type': 'match-container', 'bracket': bracket_index, 'round': round_index}  # add/delete matches
                ),
                justify='center',
                className='mt-3'
            ),
            make_add_match_button(bracket_index, round_index),
        ],
        id={'type': 'round-accordion-item', 'bracket': bracket_index, 'round': round_index}, # update round num
        title= html.Div(f'Round {round_number}', className='fs-5') if round_number else '',
        class_name='border border-1'
    )
    return content


def make_bracket_accordion(index):
    accordion = html.Div(
        [
            dbc.Accordion(
                [
                    make_round_accordion_item(index, 0, 1)
                ],
                id={'type': 'bracket-accordion', 'bracket': index},  # called by add/delete round btn
                always_open=True,
            ),
            html.Div(
                dbc.Button(
                    [
                        html.I(className='fa-solid fa-plus me-3'),
                        "Add Round"
                    ],
                    id={'type': 'add-round-button', 'bracket': index},
                    n_clicks=0,
                    class_name=''
                ),
                className='d-grid col-3 mx-auto my-2 ',
            )
        ],
        className='px-5'
    )
    return accordion


def make_bracket_header(index, bracket_type):
    dialog_id = {'element': 'delete-bracket', 'bracket': index}
    msg = ("Are you sure you wish to delete this entire bracket? All rounds and matches associated "
           "with this bracket will also be deleted. This action cannot be undone.")

    return dbc.CardHeader(
        html.Div(
            [
                html.Div("Bracket Type: ", className='me-2'),
                html.Div(
                    dbc.Select(
                        id={'type': 'bracket-type-select', 'bracket': index, 'key': 'bracket'},
                        options=[
                            {'label': 'Main', 'value': 'Main'},
                            {'label': 'Upper Bracket', 'value': 'Upper'},
                            {'label': 'Lower Bracket', 'value': 'Lower'},
                            {'label': 'Winner\'s Bracket', 'value': 'Winner\'s'},
                            {'label': 'Loser\'s Bracket', 'value': 'Loser\'s'}
                        ],
                        value=bracket_type,
                    ),
                    className='col-3'
                ),
                html.Div(make_confirm_delete_button(dialog_id, msg, "Delete Bracket", ''), className='ms-auto')
            ],
            className='d-flex flex-row align-items-center'
        )
    )


def make_bracket_container(index, bracket_type):
    content = dbc.Card(
        [
            make_bracket_header(index, bracket_type),
            dbc.CardBody(make_bracket_accordion(index))
        ],
        # id={'type': ''}
    )

    return content

# =====================
# ----- Card Tabs -------
# =====================
card_tabs = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Add Website URL", tab_id='website-tab'),
                    dbc.Tab(label="Add Bracket Manually", tab_id='manual-tab'),
                ],
                id='card-tabs',
                active_tab='website-tab',
            )
        ),
        dbc.CardBody(
            html.P(
                [
                    website_content,
                    manual_content
                ],
                id='card-content'
            )
        )
    ]
)


DYNAMIC_FIELDS = {
    "theme": {
        "input": theme_input_field,
        "add_button": add_theme_button
    },
    "website": {
        #"input": web_form,
        "input": web_section,
        "add_button": add_web_button
    },
    "bracket": {
        #"input": manual_bracket_form,
        "input": manual_bracket_section,
        "add_button": add_manual_button
    }
}


# ===========================
# ========= Layout ==========
# ===========================

# Layout
def get_tournament_input_layout():
    children = dbc.Form([
        dbc.Row(
            dbc.Col(
                [
                    html.Div("Tournament Information", className='text-center h3 mt-3 mb-3'),
                    #tournament_info_form
                    tournament_info_section
                ],
                width=8,
                className='px-5 border border-3 rounded-3'
            ),
            justify='center',
            className='mb-3'
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Div("Bracket Information", className='text-center h3 mt-4 mb-3'),
                    card_tabs
                ],
                width=10,
                className='px-5 border border-3 rounded-3'
            ),
            justify='center'
        )
    ])
    return children