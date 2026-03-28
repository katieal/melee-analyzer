# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import json
import melee_data
import datetime
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
    msg = ""

    if website == "Challonge":
        return dbc.Col(
            html.Iframe(
                src=url + '/module',
                title='Embedded View of Bracket from External Site',
                className='flex-fill'
            ),
            width=12,
            className='d-flex vh-100'
        )
    elif website == "Start.gg":
        msg = "Sorry, brackets from Start.gg can't be embedded :("
    else:
        msg = "Sorry, this website is not currently supported :("

    return html.Div(
        [
            dbc.Stack(
                [
                    html.H4(msg, className='align-self-center mt-4 text-white'),
                    dbc.Button(
                        [
                            f"View on {website}",
                            html.I(className='ms-2 fa-solid fa-angles-right')
                        ],
                        href=url,
                        external_link=True,
                        target='_blank',
                        size='lg',
                        className='align-self-center shadow mb-3'
                    )
                ],
                gap=3
            )
        ],
        className='w-50 shadow bg-danger rounded'
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

def make_date_card(date):
    date = datetime.date.fromisoformat(date)
    date_str = datetime.datetime.strftime(date, '%B %d, %Y')

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5("Date", className='card-title text-center '),
                html.P(date_str, className='text-center mb-1')
            ]
        ),
        color='primary',
        className='shadow rounded-3'
    )

def make_winner_card(winner):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.I(
                            className='fa-solid fa-trophy fa-2xl align-self-center position-absolute start-0',
                            style={'color': 'yellow'}
                        ),
                        html.H4(f"Winner: {winner}", className='card-title text-center align-self-center mb-0')
                    ],
                    className='d-flex flex-row justify-content-center position-relative'
                )

            ]
        ),
        color='primary',
        className = 'shadow rounded-3'
    )
    return card

def get_info_card(title:str, body:str):
    content = []

    if title is not None and title != '':
        content.append(html.H5(title, className='card-title text-center '))

    if body is not None and body != '':
        content.append(html.P(body, className='text-center mb-1'))

    return dbc.Card(
        dbc.CardBody(content),
        color='primary',
        className = 'shadow rounded-3'
    )

def make_info_cards(bracket_data):
    # date, location, format, theme, winner

    info_row_1 = dbc.Row(
        [
            #dbc.Col(get_info_card("Date", bracket_data['date']), width=3)
            dbc.Col(make_date_card(bracket_data['date']), width=3),
            dbc.Col(get_info_card("Location", bracket_data['location']), width=3),
            dbc.Col(get_info_card("Format", melee_data.get_format_string(bracket_data['format'])), width=3)
        ],
        justify='center',
        className='my-3'
    )


    info_row_2 = dbc.Row(
        [
            #dbc.Col(get_info_card(("Winner: " + bracket_data['winner']), ''), width=5),
            dbc.Col(make_winner_card(bracket_data['winner']), width=5),
        ],
        justify='center',
        className='mb-3'
    )

    data = html.Div(
        [
            info_row_1,
            info_row_2
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
            #html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [make_info_cards(data)],
                        width=9,
                        className='shadow border border-dark border-2 bg-info rounded-3'
                    )
                ],
                justify='center'
            ),
            html.Hr(),
            dbc.Row(
                [
                    make_embed(data['website'], data['url']),
                ],
                justify='center',
            )
        ])