# Import Packages
import dash
from dash import Dash, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from melee_db import df

dash.register_page(__name__)

graph_container = html.Div(
    style={"backgroundColor": "white"}, className="flex-grow-1"
)

content = html.Div(
    [
        html.Div(
            style={"backgroundColor": "red"}, className="flex-grow-1"
        ),
        html.Div(
            style={"backgroundColor": "orange"}, className="flex-grow-1"
        ),
        html.Div(
            style={"backgroundColor": "yellow"}, className="flex-grow-1"
        ),
        graph_container,
    ],
    className="h-100 d-flex flex-column",
)

page_structure = [
    dbc.Row(
        [
            dbc.Col(
                html.P("This is column 1"),
                style={"background-color": "cyan"},
                class_name="border",
                xs=12,
                md=2,
            ),
            dbc.Col(
                [content],
                style={"backgroundColor": "green", "height": "100vh"},
                class_name="border",

                width=3
            ),
        ],
        class_name="g-0",
    )
]

layout  = dbc.Container(
    id="root",
    children=page_structure,
    fluid=True,
    class_name="g-0",
)