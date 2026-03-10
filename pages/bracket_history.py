# Import Packages
import dash
from dash import Dash, html, Input, Output, callback, dcc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import json
import melee_db as melee_db
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

# grid
columnDefs = [
    { 'field': 'date' }, # , 'filter': 'agDateColumnFilter'
    { 'field': 'location', 'filter': True },
    { 'field': 'name' },
    { 'field': 'winner' }
]
grid = dag.AgGrid(
    id='past-bracket-data',
    columnDefs=columnDefs,
    rowData=melee_db.df.to_dict('records'),
    columnSize='responsiveSizeToFit',
    getRowId='params.data.bracket_id',
    dashGridOptions= {
        'pagination': True,
        'paginationPageSizeSelector': False,
        'paginationAutoPageSize': True,
        #'rowSelection': {'mode': 'singleRow', 'enableClickSelection': False}
    },
    style={ 'height': 430 },
    className="ag-theme-alpine"
)

# add tournament button
add_btn = html.Div(
    [
        dbc.Button("Add Tournament", id="add-button", href='/bracket-add', n_clicks=0),
    ],
    className='d-flex justify-content-end me-4 mb-2'
)

# layout
layout = dbc.Container([
    dbc.Row(dbc.Col(html.Div("Past Brackets", className='text-center h1 pt-2 mt-3'))),
    dbc.Row(dbc.Col(add_btn)),
    html.Div([dbc.Container([grid], className='dbc dbc-ag-grid')]),
    dcc.Location(id='url_redirect', refresh='callback-nav')
])

@callback(
    Output('url_redirect', 'href'),
    Input('past-bracket-data', 'cellDoubleClicked'),
    prevent_initial_call=True,
)
def navigate_cell_clicked(cell):
    if cell:
        return f"/bracket-view?bracket_id={cell["rowId"]}"
    else:
        raise PreventUpdate