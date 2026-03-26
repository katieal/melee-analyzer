# Import Packages
import dash
from dash import Dash, html, callback, Input, Output, State, dcc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

# initialize dash app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR, dbc.icons.FONT_AWESOME, dbc_css], use_pages=True)

# ======================
# ===== App Layout =====
# ======================

# new tournament submission successful modal
success_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            "Tournament added!",
            class_name='bg-secondary border rounded-3'
        ),
    ],
    id='success-modal',
    size='sm',
    is_open=False,
    backdrop_class_name='bg-transparent'
)

# layout
app.layout = dbc.Container(
    [
        dcc.Store(id='data-store', data={}),
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Brackets", href=dash.page_registry['pages.bracket_history']['path'])),
                dbc.NavItem(dbc.NavLink("Bracket View", href=dash.page_registry['pages.bracket_view']['path'])),
                dbc.NavItem(dbc.NavLink("testing", href=dash.page_registry['pages.testing']['path'])),
            ],
            brand="Melee Analyzer",
            brand_href=dash.page_registry['pages.home']['path'],
            color='primary',
            dark=True,
            className='mx-5'
        ),
        success_modal,
        dbc.Row(
            dbc.Col(dash.page_container, width=10),
            justify='center'
        ),
        html.Div(className='my-5'),
        html.Footer(
            [
            ],
            id='footer',
            className='mx-5 p-4 bg-primary')
    ],
    fluid=True,
    className='px-5'
)

@callback(
    Output('success-modal', 'is_open'),
    Input('data-store', 'data')
)
def open_success_modal(data):
    # display success modal when store value changes to True
    # no update if no data is stored
    if data is None or data == {}:
        return dash.no_update
    # check for correct key in data
    elif "success_modal" in data.keys():
        if data["success_modal"]:
            return True

    return dash.no_update

@callback(
    Output('data-store', 'data', allow_duplicate=True),
    Input('success-modal', 'is_open'),
    prevent_initial_call=True
)
def update_store(is_open):
    # update value in store when modal is closed
    if not is_open:
        return {"success_modal": False}
    return dash.no_update

if __name__ == "__main__":
    app.run(debug=True)