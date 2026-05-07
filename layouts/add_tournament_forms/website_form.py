# Import Packages
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import datetime as dt
import calendar

from utils.data_utils import stringify_id
import layouts.constants as constants
from layouts.constants import ElementType as EleType

label_width = 3
input_width = 9
margin = 'mb-4'

missing_feedback = dbc.FormFeedback("Field is required", type='invalid')
# utility method
def get_id(element_type: constants.ElementType, name:str):
    return constants.APP_IDS['add_tournament'][str(element_type)][name]

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
            type='button',
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
        type='button',
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
            name='website',
            options=[
                {'label': "Start.gg", "value": "Start.gg"},
                {'label': "Challonge", "value": "Challonge"},
                {'label': "Other", "value": "Other"}
            ],
            #required=True,
            #placeholder="Select Website"
        ),
        missing_feedback
    ],
    className='mb-3'
)
url_input = html.Div(
    [
        dbc.Label("Bracket URL", html_for='url-input', size='lg', className='mb-1'),
        #dbc.Input(type='url', id='url-input',maxlength=constants.MAX_URL_LENGTH,inputmode='url', placeholder="Enter bracket URL",required=True,disabled=True ),
        make_input('url', 'url', "Enter bracket URL", disabled=True),
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
    className='mb-3 opacity-50'
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

def get_layout():
    return html.Div(
        [web_input_header, website_input, url_input],
    )