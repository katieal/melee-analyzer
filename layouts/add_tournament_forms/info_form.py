# Import Packages
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import datetime as dt
import calendar

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

def make_input(field_name: str, input_type, placeholder: str, required=True, disabled=False):
    return dbc.Input(
        id=get_id(EleType.INPUT, field_name),
        name=field_name,
        type=input_type,
        maxlength=constants.MAX_INPUT_LENGTH if input_type != 'url' else constants.MAX_URL_LENGTH,
        placeholder=placeholder,
        required=required,
        disabled=disabled,
    )

# =============================================
# ========= Tournament Info Fields =========
# =============================================
# Name
name_input = dbc.Row(
    [
        dbc.Label("Tournament Name", html_for=stringify_id(get_id(EleType.INPUT, 'name')), size='lg', width=label_width),
        #html.Label("Tournament Name", html_for=stringify_id(get_id(EleType.INPUT, 'name')),),
        dbc.Col(
            [
                #dbc.Input(type='text', id=get_id(EleType.INPUT, 'name'), maxlength=constants.MAX_INPUT_LENGTH, placeholder="Enter tournament name", required=True),
                make_input('name', 'text', "Enter tournament name"),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)


def make_month_select():
    month = dt.date.today().month

    return dbc.Select(
        id=get_id(EleType.INPUT, 'month'),
        name='month',
        options= [
            {'label': name, 'value': num} for i, (num, name) in enumerate(constants.MONTH_STR.items())
        ],
        value=str(month) if month > 10 else ('0' + str(month)),
        required=True,
    )

def make_day_select():
    today = dt.date.today()
    z, days = calendar.monthrange(today.year, today.month)

    return dbc.Select(
        id=get_id(EleType.INPUT, 'day'),
        name='day',
        options=list(range(0, days + 1)),
        value=today.day,
        required=True,
    )

def make_year_select():
    min_year = 2020
    max_year = dt.date.today().year + 2

    return dbc.Select(
        id=get_id(EleType.INPUT, 'year'),
        name='year',
        options=list(range(min_year, max_year + 1)),
        value=dt.date.today().year,
        required=True,
    )

date_picker = dbc.Row(
    [
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Month"),
            make_month_select(),
        ])),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Day"),
            make_day_select(),
        ]), width=3),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Year"),
            make_year_select(),
        ]))
    ]
)

dcc_datepicker = dcc.DatePickerSingle(
    id=get_id(EleType.INPUT, 'date'),
    month_format='MMMM YYYY',
    display_format='MMMM DD, YYYY',
    clearable=True
),

# Date
date_input = dbc.Row(
    [
        dbc.Label("Date", html_for=stringify_id(get_id(EleType.INPUT, 'date')), size='lg', width=label_width),
        dbc.Col([
                date_picker,
                # dbc.Input(type='hidden', id={'type': 'input-hidden', 'element': 'date-picker'}),
                # missing_feedback
            ],
            width=input_width,
            #className='dbc'
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
                #dbc.Input(type='text', id=get_id(EleType.INPUT, 'location'), maxlength=constants.MAX_INPUT_LENGTH, placeholder="Enter location", required=True),
                make_input('location', 'text', "Enter location"),
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
                    name='format',
                    options=[
                        {'label': "Single Elimination", 'value': "single_elim"},
                        {'label': "Double Elimination", 'value': "double_elim"},
                        {'label': "Round Robin", 'value': "robin"},
                    ],
                    required=True,
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
        #dbc.Input( type='text',id=get_id(EleType.INPUT, 'theme'),maxlength=constants.MAX_INPUT_LENGTH, placeholder="Enter theme", required=True,),
        make_input('theme', 'text', "Enter theme"),
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
                #dbc.Input(type='text', id=get_id(EleType.INPUT, 'winner'), maxlength=constants.MAX_INPUT_LENGTH, placeholder="Enter name of tournament winner", required=True),
                make_input('winner', 'text', "Enter name of tournament winner"),
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