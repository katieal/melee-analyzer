# Import Packages
import dash
from dash import html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx, clientside_callback, ClientsideFunction, get_app
import dash_bootstrap_components as dbc
from flask import request
import flask
import pandas as pd
from dash.exceptions import PreventUpdate
import json

dash.register_page(__name__)

# overflowX in style property in a div can enable horizontal scrollbar
bracket_link = 'https://www.start.gg/tournament/pho-tai-melee-134/event/melee-singles/brackets/2210582/3211219'

label_width = 3
input_width = 9
margin = 'mb-4'
missing_feedback = dbc.FormFeedback("Field is required", type='invalid')

input_1 = dbc.Row(
    [
        dbc.Label("Tournament Name", html_for='input-1', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='text', id='input-1', placeholder="Enter tournament name", required=True),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)
input_2 = dbc.Row(
    [
        dbc.Label("Input 2", html_for='input-2', width=label_width),
        dbc.Col(
            [
                dbc.Input(type='number', id='input-2', required=True),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)
input_3 = dbc.Row(
    [
        dbc.Label("Input 3", html_for='input-3', width=label_width),
        dbc.Col(
            [
                dbc.Select(
                    id='input-3',
                    options=[
                        {'label': 'Option 1', 'value': 1},
                        {'label': 'Option 2', 'value': 2},
                    ],
                    required=True
                ),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)

test_form = dbc.Form(
    [
        input_1,
        input_2,
        input_3,
        dbc.Button(
            "Submit",
            id='submit',
            type='submit',
            n_clicks=0,
        )
    ],
    class_name='needs-validation'
)

test_form_html = html.Form(
    [
        html.Div(
            [
                dbc.Label("First name", html_for='validationCustom01'),
                dbc.Input(type='text', id='validationCustom01', value="Mark", name='first_name', required=True, className='was-validated'),
                html.Div("Looks Good!", className='valid-feedback')
            ],
            className='col-md-4'
        ),
        html.Div(
            [
                dbc.Label("Last name", html_for='validationCustom02'),
                dbc.Input(type='text', id='validationCustom02', value="Otto", name='last_name', required=True),
                dbc.FormFeedback("Looks Good!", type='valid')
            ],
            className='col-md-4'
        ),
        html.Div(
            [
                dbc.Label("Username", html_for='validationCustomUsername'),
                dbc.Input(type='text', id='validationCustomUsername', name='username', required=True),
                dbc.FormFeedback("Please choose a username", type='invalid')
            ],
            className='col-md-4'
        ),
        html.Div(
            [
                dbc.Label("City", html_for='validationCustom03'),
                dbc.Input(type='text', id='validationCustom03', name='city', required=True),
                dbc.FormFeedback("Please provide a valid city", type='invalid')
            ],
            className='col-md-6'
        ),
        html.Div(
            [
                dbc.Checkbox(
                    id='invalidCheck',
                    label="Agree to terms and conditions",
                    value=False
                ),
                dbc.FormFeedback("You must agree before submitting.", type='invalid')
            ],
            className='col-12'
        ),
        html.Div(
            dbc.Button("Submit Form", id='html-form-submit', type='submit'),
            className='col-12'
        )
    ],
    id='test-form-html',
    noValidate=True,
    name='test-html-form',
    action='/testing/submit',
    method='POST',

    className='row g-3 needs-validation',
)


sample_js_output = html.Div(
    [
        dbc.Button(
            "Click me!",
            id='javascript-button',
            n_clicks=0,
        ),

    ]
)

layout = dbc.Container(
    [
        # title
        dbc.Row(dbc.Col(html.Div("Testing", className='text-center h1 mt-5 mb-0'))),

        test_form_html,

        html.Div(id='javascript-output')
    ],
    fluid=True,
    id='testing-layout'
)




myapp = dash.get_app()



@myapp.server.route('/testing/submit', methods=['POST'])
def submit_form():
    print("submitting form")
    datatype = request.content_type
    print(datatype)
    data = request.get_data()
    print("type: ", type(data))
    form_data = request.form
    print(form_data)

    return flask.make_response({"status": "success"}, 200)