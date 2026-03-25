# Import Packages
import dash
from dash import Dash, html, Input, Output, callback, dcc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import json
import melee_data
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

# grid
columnDefs = [
    { 'field': 'date' }, # , 'filter': 'agDateColumnFilter'
    { 'field': 'location', 'filter': True },
    { 'field': 'name' },
    { 'field': 'winner' }
]

# add tournament button
add_btn = html.Div(
    [
        dbc.Button("Add Tournament", id="add-button", href='/bracket-add-manual', n_clicks=0),
    ],
    className='d-flex justify-content-end me-4 mb-2'
)
# links to add by url or add manually pages
add_bracket_dropdown = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem(
            "Add by URL",
            href='/bracket-add-url'
        ),
        dbc.DropdownMenuItem(
            "Add Manually",
            href='/bracket-add-manual'
        )
    ],
    label="Add New Tournament",
    color='secondary',
    menu_variant='dark',
    align_end=True
)

def get_grid():
    return dag.AgGrid(
        id='past-bracket-data',
        columnDefs=columnDefs,
        rowData=melee_data.db.df_no_index.to_dict('records'),
        columnSize='responsiveSizeToFit',
        getRowId='params.data.bracket_id',
        dashGridOptions= {
            'pagination': True,
            'paginationPageSizeSelector': False,
            'paginationAutoPageSize': True,
        },
        style={ 'height': 430 },
        className="ag-theme-alpine"
    )

# layout
def layout(**kwargs):
    # refresh database
    melee_data.db.refresh()

    # build page
    return dbc.Container([
        dbc.Row(dbc.Col(html.Div("Past Tournaments", className='text-center h1 mt-5 mb-0'))),
        html.Hr(),
        dbc.Row(
            dbc.Col(add_bracket_dropdown, width='auto', className='me-4 mb-2'),
            justify='end'
        ),
        html.Div([dbc.Container([get_grid()], className='dbc dbc-ag-grid')]),
        dcc.Location(id='url_redirect', refresh='callback-nav')
    ])

@callback(
    Output('url_redirect', 'href'),
    Input('past-bracket-data', 'cellDoubleClicked'),
    prevent_initial_call=True,
)
def navigate_cell_clicked(cell):
    if cell:
        if melee_data.use_bracket_embed(cell["rowId"]):
            # redirect to embed page if bracket data has a link
            return f"/bracket-view-embed?bracket_id={cell["rowId"]}"
        else:
            # otherwise, redirect to manual bracket view
            return f"/bracket-view?bracket_id={cell["rowId"]}"
    else:
        raise PreventUpdate
