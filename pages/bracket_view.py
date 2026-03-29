# Import Packages
import dash
from dash import Dash, html, Input, Output, State, callback, dcc, ALL, MATCH, Patch, ctx
import dash_bootstrap_components as dbc
import melee_data
from dash.exceptions import PreventUpdate
import bracket_view_builder as builder

dash.register_page(__name__)


def make_header(name, website, url):
    """
    Return a html.Div with tournament name and link to original site if applicable
    """
    content = []
    # add name if applicable
    if name is not None:
        content.append(html.Div(f"{name} Results", className='text-center h1 mb-0'))

    # add link to original website if applicable
    if url:
        site = "Original Website" if website == "Other" else website
        content.append(dbc.Button(
            [
                f"View on {site}",
                html.I(className='ms-2 fa-solid fa-angles-right')
            ],
            href=url,
            external_link=True,
            target='_blank',
            className='position-absolute end-0 align-self-center mb-0'
        ))

    return html.Div(
        content,
        className='d-flex flex-row justify-content-center position-relative mt-5 mb-0'
    )


def make_date_card(date):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.I(className='fa-regular fa-calendar align-self-center position-absolute start-0'),
                        html.H5("Date", className='card-title text-center'),
                    ],
                    className='d-flex flex-row justify-content-center position-relative'
                ),
                html.P(date, className='text-center mb-1')
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

def make_info_card(title:str, body:str):
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

def make_info_cards(info):
    info_row_1 = dbc.Row(
        [
            dbc.Col(make_date_card(info['date']), width=3),
            dbc.Col(make_info_card("Location", info['location']), width=3),
            dbc.Col(make_info_card("Format", info['format']), width=3)
        ],
        justify='center',
        className='my-3'
    )
    info_row_2 = dbc.Row(
        [
            dbc.Col(make_winner_card(info['winner']), width=5),
        ],
        justify='center',
        className='mb-3'
    )

    return html.Div([info_row_1, info_row_2])


def make_bracket_view(info):
    """
    Build bracket view with either custom match info or embedded url
    """
    if info['show_custom'] and info['match_data'] is not None:
        # show custom match data if applicable
        bracket = builder.make_custom_view(info['match_data'], info['match_sizes'])
        return dbc.Col(bracket, width=8, className='ps-0 pe-0')
    else:
        if info['url'] is not None:
            # show embedded bracket if applicable
            return builder.make_embed_view(info['website'], info['url'])
        else:
            # if bracket has neither match info nor url, show missing info msg
            return html.Div([ "There is no match information currently associated with this tournament."])


def layout(bracket_id=None, **kwargs):
    if bracket_id is None:
        return dbc.Container()
    else:
        # get bracket info from melee db
        info = melee_data.get_bracket_info(bracket_id)

        return dbc.Container([
            make_header(info['name'], info['website'], info['url']),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [make_info_cards(info)],
                        width=9,
                        className='shadow border border-dark border-2 bg-info rounded-3'
                    )
                ],
                justify='center'
            ),
            html.Hr(),
            dbc.Row(
                [
                    #make_embed(info),
                    make_bracket_view(info)
                ],
                justify='center',
            )
        ])