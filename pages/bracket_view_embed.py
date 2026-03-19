# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import json
import melee_db as melee_db
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

embed_bracket = html.Iframe(
    src='https://challonge.com/47a7kyvx/module',
    title='Embedded View of Bracket from External Site',
    className='flex-fill'
)


def get_bracket_embed(bracket_link):
    """
    Return a html.Iframe with the embedded bracket
    :param bracket_link:
    :return:
    """
    return html.Iframe(
        src=bracket_link + '/module',
        title='Embedded View of Bracket from External Site',
        className='flex-fill'
    )

def get_header(bracket_link):
    return html.Div(
        [
            html.Div("Bracket Results", className='text-center h1 mb-0'),
            dbc.Button("View on Challonge",
                       outline=True,
                       href=bracket_link,
                       className='position-absolute end-0 align-self-center mb-0')
        ],
        className='d-flex flex-row justify-content-center position-relative mt-5 mb-0'
    )

def layout(bracket_link=None, **kwargs):
    if bracket_link is None:
        return dbc.Container()
    else:
        return dbc.Container([
            get_header(bracket_link),
            html.Hr(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_bracket_embed(bracket_link),
                        ],
                        width=12,
                        className='d-flex vh-100'
                    )
                ],
                align='center',
            )
        ])