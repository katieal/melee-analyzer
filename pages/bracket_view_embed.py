# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import json
import melee_data
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

embed_bracket = html.Iframe(
    src='https://challonge.com/47a7kyvx/module',
    title='Embedded View of Bracket from External Site',
    className='flex-fill'
)


def get_bracket_embed(website, link):
    """
    Return a html.Iframe with the embedded bracket
    :param website:
    :param link:
    :return:
    """

    url = link if website == "Start.gg" else link + '/module'

    return html.Iframe(
        src=url,
        title='Embedded View of Bracket from External Site',
        className='flex-fill'
    )

def get_header(name, website, link):
    return html.Div(
        [
            html.Div(f"{name} Results", className='text-center h1 mb-0'),
            dbc.Button(
                [
                    f"View on {website}",
                    html.I(className='ms-2 fa-solid fa-angles-right')
                ],
               href=link,
               external_link=True,
               target='_blank',
               className='position-absolute end-0 align-self-center mb-0'
            )
        ],
        className='d-flex flex-row justify-content-center position-relative mt-5 mb-0'
    )


def layout(bracket_id=None, **kwargs):
    if bracket_id is None:
        return dbc.Container()
    else:
        # get bracket data from melee db
        name, website, link = melee_data.get_bracket_link(bracket_id)
        return dbc.Container([
            get_header(name, website, link),
            html.Hr(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_bracket_embed(website, link),
                        ],
                        width=12,
                        className='d-flex vh-100'
                    )
                ],
                align='center',
            )
        ])