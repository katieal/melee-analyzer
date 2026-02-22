# Import Packages
import dash
from dash import Dash, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from melee_db import df

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
    rowData=df.to_dict('records'),
    columnSize="responsiveSizeToFit",
    dashGridOptions= {
        'pagination': True,
        'paginationPageSizeSelector': False,
        'paginationAutoPageSize': True,
    },
    style={ 'height': 430 },
    className="ag-theme-alpine"
)

# layout
layout = dbc.Container([
    dbc.Row(html.Div("Past Bracket Results", className='text-center h1 p-2 m-3')),
    html.Div([dbc.Container([grid], className="dbc dbc-ag-grid")])
])
