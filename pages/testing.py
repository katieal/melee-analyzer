# Import Packages
import dash
from dash import Dash, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from melee_data import df
import melee_data as melee_db

dash.register_page(__name__)

# overflowX in style property in a div can enable horizontal scrollbar
bracket_link = 'https://www.start.gg/tournament/pho-tai-melee-134/event/melee-singles/brackets/2210582/3211219'

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

layout = dbc.Container([
    get_header("Test", "Start.gg", bracket_link),
    html.Hr(),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                [
                    get_bracket_embed("Start.gg", bracket_link),
                ],
                width=12,
                className='d-flex vh-100'
            )
        ],
        align='center',
    )
])