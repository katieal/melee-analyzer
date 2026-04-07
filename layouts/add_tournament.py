# Import Packages
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from utils.data_utils import stringify_id
import layouts.constants as constants

# constants
label_width = 3
input_width = 9
margin = 'mb-4'

missing_feedback = dbc.FormFeedback("Field is required", type='invalid')


# =============================================
# ========= Tournament Info Fields =========
# =============================================
# Name
name_id = {'type': 'input-field', 'element': 'name-input', 'key': 'name'}
name_input = dbc.Row(
    [
        dbc.Label("Tournament Name", html_for=stringify_id(name_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=name_id, maxlength=constants.MAX_INPUT_LENGTH, placeholder="Enter tournament name"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)

# Date
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

# Location
location_id = {'type': 'input-field', 'element': 'location-input', 'key': 'location'}
location_input = dbc.Row(
    [
        dbc.Label("Location", html_for=stringify_id(location_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=location_id, maxlength=constants.MAX_INPUT_LENGTH, placeholder="Enter location"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)

# Format
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

# Theme
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
            maxlength=constants.MAX_INPUT_LENGTH,
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

# Winner
winner_id = {'type': 'input-field', 'element': 'winner-input', 'key': 'winner'}
winner_input = dbc.Row(
    [
        dbc.Label("Winner", html_for=stringify_id(winner_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id=winner_id, maxlength=constants.MAX_INPUT_LENGTH, placeholder="Enter name of tournament winner"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)

# Form
tournament_info_form = dbc.Form([name_input, date_input, location_input, format_input, theme_input, winner_input])



# ========================
# ----- Website Input ----
# ========================

# ---- Header ----
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

# ---- Add Button ----
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

# ---- Input Fields ----
type_id = {'type': 'alt-input-field', 'element': 'source-radio'}
website_input = html.Div(
    [
        dbc.Label("Source Website", html_for=stringify_id(type_id), size='lg', className='mb-1'),
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

# ---- Form ----
web_form = dbc.Form([web_input_header, website_input, url_input])
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
    )
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
            id={'type': 'dynamic-delete', 'element': 'bracket'},
            color='danger',
            n_clicks=0,
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
        id={'type': 'dynamic-add', 'element': 'bracket'},
        color='info',
        n_clicks=0
    )],
    className='d-grid col-6 mx-auto'
)
add_bracket_section = html.Div(
    [
        html.Div(
            [
                dbc.Button(
                    [
                        html.I(className='fa-solid fa-plus me-3'),
                        "New Bracket"
                    ],
                    id='add-bracket-button',
                    n_clicks=0
                )
            ],
            className='d-flex w-75 justify-content-center py-4',
            style={
                'border': 'dashed',
                'border-radius': '50rem',
                'border-color': 'var(--bs-border-color)'
            }
        )
    ],
    className='d-flex justify-content-center'
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

# ---- Form ----
manual_bracket_form = dbc.Form([manual_input_header, manual_display_option, add_bracket_section])
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
        manual_input_container
    )
)


add_bracket_section = html.Div(
    [
        html.Div(
            [
                dbc.Button(
                    [
                        html.I(className='fa-solid fa-plus me-3'),
                        "New Bracket"
                    ],
                    id='add-bracket-button',
                    n_clicks=0
                )
            ],
            className='d-flex w-75 justify-content-center py-4',
            style={
                'border': 'dashed',
                'border-radius': '50rem',
                'border-color': 'var(--bs-border-color)'
            }
        )
    ],
    className='d-flex justify-content-center'
)


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
        maxlength=constants.MAX_NAME_LENGTH,
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
def make_delete_round_button(round_index):
    btn = dbc.Button(
        [html.I(className='fa-solid fa-minus me-2'), "Delete Round"],
        id={'type': 'delete-round-button', 'round': round_index},
        color='danger',
        size='sm',
        n_clicks=0,
        className='ms-auto'
    )
    msg = ("Are you sure you wish to delete this round? All matches associated "
           "with this round will also be deleted. This action cannot be undone.")

    return html.Div(
        [
            dbc.Collapse(
                dcc.ConfirmDialogProvider(
                    btn,
                    id={'type': 'delete-round-confirm', 'round': round_index},
                    message=msg
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


def make_round_accordion_item(round_index, round_number=None):
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
        id={'type': 'round-accordion-item', 'round': round_index}, # update round num
        title= html.Div(f'Round {round_number}', className='fs-5') if round_number else '',
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

bracket_type_select = html.Div(
    [
        dbc.Label("Select Bracket Type"),
        dbc.Select(
            id='bracket-type-select',
            options=[
                {'label': 'Main', 'value': 'Main'},
                {'label': 'Upper Bracket', 'value': 'Upper'},
                {'label': 'Lower Bracket', 'value': 'Lower'},
                {'label': 'Winner\'s Bracket', 'value': 'Winner\'s'},
                {'label': 'Loser\'s Bracket', 'value': 'Loser\'s'}
            ]
        )
    ]
)

#bracket_input_container = html.Div(
#    [
#        bracket_type_select,
#        bracket_data_accordion
#    ]
#)

#manual_input_container = html.Div(
#    [
#        bracket_input_container,
#        add_bracket_section,
#    ]
#)

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
        dbc.CardBody(html.P(id='card-content'))
    ]
)

def get_card_tabs_dcc():
    children = [
        dcc.Tab("")
    ]

DYNAMIC_FIELDS = {
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
TAB_CONTENT = {
    "website-tab": website_content,
    "manual-tab": manual_content
}


# ===========================
# ========= Layout ==========
# ===========================
# Layout
def get_tournament_input_layout():
    children = html.Div([
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