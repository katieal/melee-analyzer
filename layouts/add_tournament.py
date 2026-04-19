# Import Packages
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import datetime as dt
import calendar

from utils.data_utils import stringify_id
import layouts.constants as constants
from layouts.constants import ElementType as EleType
import layouts.add_tournament_forms.info_form as info_fields
import layouts.add_tournament_forms.website_form as website_fields
import layouts.add_tournament_forms.bracket_form as bracket_fields

# constants
label_width = 3
input_width = 9
margin = 'mb-4'

missing_feedback = dbc.FormFeedback("Field is required", type='invalid')

# utility method
def get_id(element_type: constants.ElementType, name:str):
    return constants.APP_IDS['add_tournament'][str(element_type)][name]

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
                    website_fields.website_content,
                    bracket_fields.manual_content
                ],
                id='card-content'
            )
        )
    ]
)


DYNAMIC_FIELDS = {
    "theme": {
        "input": info_fields.theme_input_field,
        "add_button": info_fields.add_theme_button
    },
    "website": {
        #"input": web_form,
        "input": website_fields.web_section,
        "add_button": website_fields.add_web_button
    },
    "bracket": {
        #"input": manual_bracket_form,
        "input": bracket_fields.manual_bracket_section,
        "add_button": bracket_fields.add_manual_button
    }
}

# invalid field alert box
invalid_alert = dbc.Row(
    dbc.Col(
        dbc.Alert(
            "Submission Failed: Missing or invalid fields!",
            id=get_id(EleType.MISC, 'invalid_alert'),
            color='danger',
            dismissable=True,
            is_open=False,
        ),
        width=8
    ),
    justify='center',
    className='mt-4'
)

# ===========================
# ========= Layout ==========
# ===========================

def make_input_section(title, content):
    return dbc.Row(
        dbc.Col(
            [
                html.Div(title, className='text-center h3 mt-3 mb-3'),
                content
            ],
            width=8,
            className='px-5 border border-3 rounded-3'
        ),
        justify='center',
        className='mb-3'
    )

def make_next_button(btn_id):
    return dbc.Row(
        html.Div(
            dbc.Button(
                ["Next", html.I(className='fa-solid fa-right-long ms-3')],
                id=btn_id,
                size='lg',
                color='secondary',
                n_clicks=0
            ),
            className='d-grid col-3 ms-auto'
        ),
        justify='center',
        className='mt-4'
    )

# Layout
def get_info_layout():
    children = [
        make_input_section("Tournament Information", info_fields.tournament_info_section),
        invalid_alert,
        make_next_button(get_id(EleType.BUTTON, 'submit_info')),
    ]
    return html.Form(
        children,
        id=get_id(EleType.MISC, 'info_form'),
        noValidate=True,
        name='tournament-info-form',
    )

def get_website_layout():
    children = [
        make_input_section("Add Website URL", website_fields.website_content),
        invalid_alert,
        make_next_button(get_id(EleType.BUTTON, 'submit_website')),
    ]
    return html.Form(
        children,
        id=get_id(EleType.MISC, 'website_form'),
        noValidate=True,
        name='website-form',
    )

def get_bracket_layout():
    children = [
        make_input_section("Add Bracket Manually", bracket_fields.manual_content),
        invalid_alert,
        make_next_button(get_id(EleType.BUTTON, 'submit_bracket')),
    ]
    return html.Form(
        children,
        id=get_id(EleType.MISC, 'bracket_form'),
        noValidate=True,
        name='bracket-form',
    )