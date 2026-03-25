# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx, set_props
import dash_bootstrap_components as dbc
import pandas as pd
import json
import re
import melee_data
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

# IDs
def stringify_id(id_):
    if isinstance(id_, dict):
        return json.dumps(id_, sort_keys=True, separators=(",", ":"))
    return id_

# TO do:
# input box style changes when using browser autocomplete?

# ========= Input Components =========
missing_feedback = dbc.FormFeedback("Field is required", type='invalid')
max_url_length = 100
max_input_length = 30
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

type_id = {'type': 'alt-input-field', 'element': 'source-radio'}
bracket_type_input = html.Div(
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
#url_id= {'type': 'url-field', 'element': 'url-input'}
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
    className='mb-3'
)
# ----- Tournament Info Inputs -----
label_width = 3
input_width = 9
margin = 'mb-4'
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
mode_id = {'type': 'input-field', 'element': 'mode-select', 'key': 'mode'}
mode_input = dbc.Row(
    [
        dbc.Label("Tournament Mode", html_for=stringify_id(mode_id), size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Select(
                    id=mode_id,
                    options=[
                        {'label': "Single Elimination", 'value': "single_elim"},
                        {'label': "Double Elimination", 'value': "double_elim"},
                        {'label': "Round Robin", 'value': "robin"},
                    ],
                    # placeholder text in this field doesn't have the same muted appearance as the placeholders
                    # in input fields which looks weird so omitting it for now
                    # placeholder="Select tournament mode"
                ),
                missing_feedback
            ],
            width=input_width
        )
    ],
    className=margin
)
#theme_id = {'type': 'checkbox-field', 'element': 'theme-checkbox'}
theme_input_id = {'type': 'input-field', 'element': 'theme-input', 'key': 'theme'}
theme_input = dbc.Row(
    [
        dbc.Label("Tournament Theme", html_for='theme-checkbox', size='lg', width=label_width),
        dbc.Col(
            [
                dbc.Checkbox(id='theme-checkbox', label="Check if tournament has a special theme", value=False),
                dbc.Input(type='text', id=theme_input_id, maxlength=max_input_length, placeholder="Enter theme", disabled=True),
                missing_feedback
            ],
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

# URL input form
bracket_url_form = dbc.Form([bracket_type_input, url_input])
# Tournament details input form
bracket_info_form = dbc.Form([name_input, date_input, location_input, mode_input, theme_input, winner_input])

# submit button
submit_button = html.Div(
    dbc.Button("Submit", id='submit-button', size='lg', color='secondary'),
    className='d-grid col-6 mx-auto my-3'
)

# invalid field alert box
invalid_alert = dbc.Alert(
    "Submission Failed: Missing or invalid fields!",
    id='invalid-alert',
    color='danger',
    dismissable=True,
    is_open=False
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
        dbc.Row(
            dbc.Col(invalid_alert, width=8),
            justify='center',
            className='mt-4'
        ),
        dbc.Row(submit_button, className='mt-4'),
        dcc.Location(id='url-redirect', refresh='callback-nav')
    ],
    fluid=True,
)

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
    Output({'type': 'input-field', 'element': 'theme-input', 'key': 'theme'}, 'disabled'),
    Output({'type': 'input-field', 'element': 'theme-input', 'key': 'theme'}, 'invalid', allow_duplicate=True),
    Input('theme-checkbox', 'value'),
    prevent_initial_call=True
)
def toggle_theme_input(is_checked):
    # enable/disable the custom theme input field based on if this box is checked

    # clear error message if box is unchecked
    return not is_checked, False if not is_checked else dash.no_update

# callback to detect valid URL
@callback(
    Output('url-input', 'invalid'),
    Output('url-input', 'disabled'),
    inputs={
        'url': Input('url-input', 'value'),
        'website': Input({'type': 'alt-input-field', 'element': 'source-radio'}, 'value'),
    },
    prevent_initial_call=True
)
def validate_url(url, website):
    # url box is only enabled after website is selected
    if website is None or website == '':
        raise PreventUpdate
    else:
        if url is None or url == '':
            # enable url input field
            return dash.no_update, False
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
            # input field is already enabled so send dash.no_update for 2nd arg
            # set invalid to true if url does NOT match pattern, false if it DOES match
            return is_invalid, dash.no_update


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
    inputs={
        'n_clicks': Input('submit-button', 'n_clicks'),
        'inputs': {
            'values': State({'type': 'input-field', 'element': ALL, 'key': ALL}, 'value'),
            'ids': State({'type': 'input-field', 'element': ALL, 'key': ALL}, 'id'),
        },
        'alt_inputs': {
            'url_value': State('url-input', 'value'),
            'url_invalid': State('url-input', 'invalid'),
            'source-value': State({'type': 'alt-input-field', 'element': 'source-radio'}, 'value'),
            'date_value': State({'type': 'alt-input-field', 'element': 'date-picker'}, 'date'),
            'theme_checkbox': State('theme-checkbox', 'value'),
        },
    },
    prevent_initial_call=True
)
def submit_form_pattern(n_clicks, inputs, alt_inputs):
    if n_clicks > 0:
        # track if form is ready to submit
        is_form_valid = True
        # build data dict
        data = {}

        # Check for null values in input fields
        missing_fields = []
        for i, val in enumerate(inputs['values']):
            # custom logic for theme field
            if inputs['ids'][i]['key'] == 'theme':
                # if box for custom theme is not checked, theme field isn't required
                if not alt_inputs['theme_checkbox']:
                    # if tournament doesn't have a custom theme
                    if is_form_valid: data['theme'] = "N/A"
                    continue

            if val is None or val == '':
                # find all fields with empty values
                missing_fields.append(i)
                # flag that form has an invalid field
                is_form_valid = False
            if is_form_valid:
                # add to data dict if form is still valid
                data[inputs['ids'][i]["key"]] = val
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
                data["link"] = alt_inputs['url_value']
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

        if is_form_valid:
            print("Submission successful!")
            melee_data.add_tournament(data)
            # submit data and display success screen
            return '/bracket-history'
        else:
            print("Submission failed!")
            # display error screen
            set_props('invalid-alert', {'is_open': True})
            return dash.no_update
    else:
        raise PreventUpdate
