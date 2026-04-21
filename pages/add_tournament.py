# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx, set_props, clientside_callback, ClientsideFunction
import dash_bootstrap_components as dbc
import pandas as pd
import json

import flask
import re
from dash.exceptions import PreventUpdate

from layouts.add_tournament import *

import layouts.constants as constants
from layouts.add_tournament_forms.bracket_form import make_bracket_container, make_round_accordion_item, get_match_row
from layouts.constants import ElementType as EleType

dash.register_page(__name__)

app_ref = dash.get_app()


# utility method
def get_id(element_type: constants.ElementType, name:str):
    return constants.APP_IDS['add_tournament'][str(element_type)][name]

# ========= Final Layout =========
def layout(**kwargs):

    return dbc.Container(
        [
            # title
            dcc.Store(id='form-store', data={"current_page": 1}),
            dbc.Row(dbc.Col(html.Div("Add a New Tournament", className='text-center h1 mt-5 mb-0'))),
            html.Hr(),
            # input
            html.Div(
                [
                    get_info_layout(),
                    get_website_layout(),
                    get_bracket_layout()
                ],
                id='form-container'
            ),
            html.Hr(),
            dbc.Button(
                "Test",
                id='data-test-button',
                n_clicks=0,
            ),
            html.Div("Sample Text", id='test-output-div'),
            dcc.Location(id='url-redirect', refresh='callback-nav')
        ],
        id='add-tournament-layout',
        fluid=True,
    )


# called when page loads
clientside_callback(
    ClientsideFunction(
        namespace='formValidation',
        function_name='validate_info_form'
    ),
    Output('add-tournament-layout', 'id'),
    Input('add-tournament-layout', 'id'),
)

@callback(
    Input('data-test-button', 'n_clicks'),
    State('form-store', 'data'),
    prevent_initial_call=True
)
def print_data(clicks, data):
    print("--------------")
    print("Stored Data: ")
    print(data)
    print("--------------")


# =========== Form Submission ===========
@callback(
    Input('form-store', 'data'),
    prevent_initial_call=True,
)
def store_updated(data):
    print("updated")
    print(data)
    update_form_display(1, 2)


def submit_form(form_dict):
    # combine into a single date field
    date = form_dict['year'] + '-' + form_dict['month'] + '-' + form_dict['day']
    form_dict['date'] = date
    del form_dict['month']
    del form_dict['year']
    del form_dict['day']

# =========== Navigation ===========
#@callback(
    #Output('card-content', 'children'),
#    Input('card-tabs', 'active_tab'),
#)
#def update_tab(active_tab):
#    if active_tab == 'website-tab':
#        set_props({'type': 'card-content', 'element': 'website-tab'}, {'class_name': ''}),
#        set_props({'type': 'card-content', 'element': 'manual-tab'}, {'class_name': 'd-none'}),
#    elif active_tab == 'manual-tab':
#        set_props({'type': 'card-content', 'element': 'website-tab'}, {'class_name': 'd-none'}),
#        set_props({'type': 'card-content', 'element': 'manual-tab'}, {'class_name': ''}),
forms_dict = {
    1: get_id(EleType.MISC, 'info_form'),
    2: get_id(EleType.MISC, 'website_form'),
    3: get_id(EleType.MISC, 'bracket_form')
}
def update_form_display(old_index:int, new_index:int):
    set_props(forms_dict[old_index], {'className': 'd-none'})
    set_props(forms_dict[new_index], {'className': ''})

@callback(
    Output({'type': 'round-info-collapse', 'bracket': MATCH, 'round': MATCH}, 'is_open'),
    Output({'type': 'round-collapse-button', 'bracket': MATCH, 'round': MATCH}, 'children'),
    Input({'type': 'round-collapse-button', 'bracket': MATCH, 'round': MATCH}, 'n_clicks'),
    State({'type': 'round-info-collapse', 'bracket': MATCH, 'round': MATCH}, 'is_open'),
    prevent_initial_call=True
)
def toggle_round_collapse(n_clicks, is_open):
    if n_clicks:
        closed = html.I(className='fa-solid fa-angle-down')
        opened = html.I(className='fa-solid fa-angle-left')

        return not is_open, closed if is_open else opened
    else:
        raise PreventUpdate

# =========== Date Input ===========
@callback(
    Output(get_id(EleType.INPUT, 'day'), 'options'),
    Output(get_id(EleType.INPUT, 'day'), 'value'),
    Input(get_id(EleType.INPUT, 'month'), 'value'),
    Input(get_id(EleType.INPUT, 'year'), 'value'),
    State(get_id(EleType.INPUT, 'day'), 'value'),
    prevent_initial_call=True
)
def update_day_options(month, year, selected_day):
    z, days = calendar.monthrange(int(year), int(month))

    # check if current selected day is a valid value for new month/year
    if int(selected_day) > days:
        # if invalid, clear day selection
        return list(range(days + 1)), None
    else:
        return list(range(days + 1)), selected_day


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
        patched_children.append(DYNAMIC_FIELDS[element]['input'])
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
        patched_children.append(DYNAMIC_FIELDS[element]['add_button'])
        return patched_children
    else:
        raise PreventUpdate

# ========= URL Field Callbacks =========
@callback(
    Output('url-input', 'disabled'),
    Output('url-input-container', 'className'),
    Input(get_id(EleType.INPUT, 'website'), 'value'),
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

# URL Field Validation
def update_url_error(is_empty):
    """
    Update the URL input field's form feedback to display the correct error message.
    Will display 'Field is required' or 'Invalid format'
    :param is_empty: Is the URL input field empty/null?
    """
    msg = "Field is required" if is_empty else "Invalid website format"
    # set correct message for form feedback
    dash.set_props('url-form-feedback', {'children': msg})

@callback(
    Output('url-input', 'invalid'),
    inputs={
        'url': Input('url-input', 'value'),
        'website': Input(get_id(EleType.INPUT, 'website'), 'value'),
    },
    prevent_initial_call=True
)
def validate_url(url, website):
    """
    Validate URL based on currently selected website and defined URL patterns
    """
    # url box is only enabled after website is selected
    if website is None or website == '' or url is None or url == '':
        raise PreventUpdate
    else:
        # check url against website patterns
        is_invalid = True
        for pattern in constants.INPUT_PATTERNS[website]:
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



# ========================
# Manual Bracket Builder
# ========================
# Add Bracket
@callback(
    Output(get_id(EleType.BUTTON, 'add_bracket'), 'disabled'),
    Input(get_id(EleType.INPUT, 'bracket_type'), 'value'),
    prevent_initial_call=True
)
def enable_add_bracket_button(bracket_type):
    if bracket_type is None or bracket_type == '':
        raise PreventUpdate
    else:
        # enable add bracket button after a type has been selected
        return False

# Update round numbers
@callback(
    Output({'type': 'round-accordion-item', 'bracket': MATCH, 'round': ALL}, 'title'),
    Input({'type': 'bracket-accordion', 'bracket': MATCH}, 'children'),
    prevent_initial_call=True
)
def update_round_numbers(items):
    # generate list of updated round number titles
    titles_list = [html.Div(f'Round {i + 1}', className='fs-5') for i in range(len(items))]
    return titles_list

# Add/delete bracket
@callback(
    Output('bracket-input-container', 'children', allow_duplicate=True),
    Input('add-bracket-button', 'n_clicks'),
    State(get_id(EleType.INPUT, 'bracket_type'), 'value'),
    prevent_initial_call=True
)
def add_bracket(n_clicks, bracket_type):
    if n_clicks > 0:
        patched_children = Patch()
        patched_children.append(make_bracket_container(n_clicks, bracket_type))
        return patched_children
    else:
        raise PreventUpdate

@callback(
    Output('bracket-input-container', 'children', allow_duplicate=True),
    Input({'type': 'confirm-dialog', 'element': 'delete-bracket', 'bracket': ALL}, 'submit_n_clicks'),
    prevent_initial_call=True
)
def delete_bracket(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        # get index of triggered button
        index = 0
        for i, button in enumerate(ctx.inputs_list[0]):
            if button['id'] == ctx.triggered_id:
                index = i
                break

        # ensure corresponding button was clicked
        if n_clicks[index]:
            # remove bracket at index
            patched_children = Patch()
            del patched_children[index]
            return patched_children
        else:
            raise PreventUpdate


# Add/delete Round
@callback(
    Output({'type': 'bracket-accordion', 'bracket': MATCH}, 'children', allow_duplicate=True),
    Input({'type': 'add-round-button', 'bracket': MATCH}, 'n_clicks'),
    prevent_initial_call=True
)
def add_round(n_clicks):
    if n_clicks > 0:
        patched_children = Patch()
        patched_children.append(make_round_accordion_item(ctx.triggered_id.bracket, n_clicks))
        return patched_children
    else:
        return PreventUpdate


@callback(
    Output({'type': 'bracket-accordion', 'bracket': MATCH}, 'children', allow_duplicate=True),
    Input({'type': 'confirm-dialog', 'element': 'delete-round', 'bracket': MATCH, 'round': ALL}, 'submit_n_clicks'),
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

        # ensure corresponding button was clicked
        if submit_n_clicks[index]:
            # remove row at index
            patched_children = Patch()
            del patched_children[index]
            return patched_children
        else:
            raise PreventUpdate

# Add/delete Match
@callback(
    Output({'type': 'match-container', 'bracket': MATCH, 'round': MATCH} , 'children', allow_duplicate=True),
    Input({'type': 'add-match-button', 'bracket': MATCH, 'round': MATCH}, 'n_clicks'),
    prevent_initial_call=True
)
def add_match(n_clicks):
    #print("add match triggered")
    if n_clicks > 0:
        patched_children = Patch()
        bracket_index = ctx.triggered_id.bracket
        round_index = ctx.triggered_id.round
        patched_children.append(get_match_row(bracket_index, round_index, n_clicks))
        return patched_children
    else:
        raise PreventUpdate


@callback(
    Output({'type': 'match-container', 'bracket': MATCH, 'round': MATCH}, 'children', allow_duplicate=True),
    Input({'type': 'delete-match-button', 'bracket': MATCH, 'round': MATCH, 'element': ALL}, 'n_clicks'),
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