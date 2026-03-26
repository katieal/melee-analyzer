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


def make_embed(website, url):
    """
    Return a html.Iframe with the embedded bracket
    :param website:
    :param url:
    :return:
    """

    link = url if website == "Start.gg" else url + '/module'

    return html.Iframe(
        src=link,
        title='Embedded View of Bracket from External Site',
        className='flex-fill'
    )

def make_header(name, website, url):
    return html.Div(
        [
            html.Div(f"{name} Results", className='text-center h1 mb-0'),
            dbc.Button(
                [
                    f"View on {website}",
                    html.I(className='ms-2 fa-solid fa-angles-right')
                ],
               href=url,
               external_link=True,
               target='_blank',
               className='position-absolute end-0 align-self-center mb-0'
            )
        ],
        className='d-flex flex-row justify-content-center position-relative mt-5 mb-0'
    )

cards = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody([
                html.H5("Date", className='card-title text-center'),
                html.Div("MM/DD/YYYY", className='card-text text-center')
            ]),
            color='primary'
        ),
        dbc.Card(
            dbc.CardBody([
                html.H5("Time", className='card-title text-center'),
                html.Div("00:00 PM", className='card-text text-center')
            ]),
            color='primary'
        ),
        dbc.Card(
            dbc.CardBody([
                html.H5("Location", className='card-title text-center'),
                html.Div("PhoThai", className='card-text text-center')
            ]),
            #color='primary'
        )
    ],
    className='w-75'
)

card_1 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Date", className='card-title text-center'),
            html.P("MM/DD/YYYY", className='text-center mb-1')
        ],
    ),
    color='primary',
    #className = 'border rounded-3'
)

card_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Location", className='card-title text-center'),
            html.P("AmyFest", className='text-center mb-1')
        ]
    ),
    color='primary',
)

card_3 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Format", className='card-title text-center'),
            html.P("Double Elimination", className='text-center mb-1')
        ]
    ),
    color='primary',
)

card_4 = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Winner:     eemee    ", className='card-title text-center mb-1 '),
            #html.P("eemee", className='text-center mb-1')
        ]
    ),
    color='primary',
)


def make_info_view():
    # date, location, format, theme, winner
    data = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(card_1, width=3),
                    dbc.Col(card_2, width=3),
                    dbc.Col(card_3, width=3)
                ],
                justify='center',
                className='my-3'
            ),
            dbc.Row(
                dbc.Col(
                    [
                        card_4
                    ],
                    width=5
                ),
                justify='center',
                className='mb-3'
            )
        ]
    )
    return data


def layout(bracket_id=None, **kwargs):
    if bracket_id is None:
        return dbc.Container()
    else:
        # get bracket data from melee db
        data = melee_data.get_bracket_url(bracket_id)
        return dbc.Container([
            make_header(data['name'], data['website'], data['url']),
            html.Hr(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(

                           [ make_info_view()],
                        width=9,
                        className='bg-info'
                    )
                ],
                justify='center'
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            make_embed(data['website'], data['url']),
                        ],
                        width=12,
                        className='d-flex vh-100'
                    )
                ],
                align='center',
            )
        ])