# Import Packages
import dash
from dash import Dash, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from melee_db import df
from melee_db import TeamInfo
from melee_db import MatchInfo
from melee_db import MatchNode
import melee_db as melee_db

dash.register_page(__name__)

# overflowX in style property in a div can enable horizontal scrollbar
# Note: fix single line spacing!!!!!!!!

# ======== Match Scores ========
player_name_border = 'border border-2 rounded-start-3 border-end-0'
player_score_border = 'border border-2 rounded-end-3 border-start-0'
bg_fill_class = 'bg-light border border-2'

# single (aka match_single)
def make_team_score(team_info:TeamInfo, add_margin_bot:bool):
    """
    Make a dbc.ListGroup for a single team's name and score
    :param add_margin_bot: should a bottom margin be included?
    :param team_info: team info dict
    :return:
    """
    return dbc.ListGroup(
        [
            dbc.ListGroupItem(team_info['name'], class_name='flex-fill ' + player_name_border),
            dbc.ListGroupItem(team_info['score'], color='success' if team_info['winner'] else 'danger', class_name=player_score_border)
        ],
        horizontal=True,
        class_name='mb-2' if add_margin_bot else '',
    )

# double (aka match_pair or get_flex_match_single)
def make_match_score(team_1:TeamInfo, team_2:TeamInfo, add_space_top=False, add_space_bot=False):
    """
    Return a div containing team 1 and 2 scores
    :param team_1:
    :param team_2:
    :param add_space_top:
    :param add_space_bot:
    :return:
    """
    return html.Div(
        html.Div(
            [
                make_team_score(team_1, True),
                make_team_score(team_2, False)
            ],
            className='flex-fill my-2'
        ),
        className='flex-fill d-flex align-items-center'
    )

def make_match_score2(team_1:TeamInfo, team_2:TeamInfo=None):
    pass

# ======== Connectors ========
base_border_class = 'flex-grow-1 border border-2'
border_top_class = 'border-start-0 border-end-0 border-bottom-0'
border_bottom_class = 'border-start-0 border-end-0 border-top-0'

connector_merge = html.Div(
    [
        html.Div(
            [
                html.Div(className=base_border_class + ' ' + border_bottom_class), # bot
                html.Div(className=base_border_class + ' border-start-0 border-bottom-0'), # top and end
                html.Div(className=base_border_class + ' border-start-0 border-top-0'), # bot and end
                html.Div(className=base_border_class + ' ' + border_top_class) # top
            ],
            className='h-100 d-flex flex-column',
        )
    ],
    className='flex-grow-1'
)

connector_single = html.Div(
    [
        html.Div(
            [
                html.Div(className='flex-grow-1'), # none
                html.Div(className=base_border_class + ' ' + border_bottom_class), # bot
                html.Div(className=base_border_class + ' ' + border_top_class), # top
                html.Div(className='flex-grow-1') # none
            ],
            className='h-100 d-flex flex-column',
        )
    ],
    className='flex-grow-1'
)

connector_merge_grid = html.Div(
    [
        connector_merge,
        connector_single
    ],
    className='flex-grow-1 d-flex flex-row',
)

connector_single_grid = html.Div(
    [
        connector_single,
        connector_single
    ],
    className='flex-grow-1 d-flex flex-row'
)


# ============= Utility ==================
col_visual = dbc.Col(
    width=1,
    class_name='bg-light border border-2'
)

# ======= Final Layout ==============
match_width = 3
con_width = 1
first_match_class = 'd-flex flex-column justify-content-evenly'
match_class = 'd-flex flex-column h-100'
conn_class = 'd-flex flex-column h-100 justify-content-evenly'

def add_match(match_cols:list[html.Div], connector_cols:list[html.Div], node:MatchNode):
    """
    Recursive method to construct list of matches and list of columns.
    Will immediately return if node is None
    :param match_cols: list containing html.Divs for matches
    :param connector_cols: list containing html.Divs for connectors
    :param node: the current MatchNode to be added
    :return: None
    """
    # check for valid node
    if node is None:
        return

    # add match to column
    match_cols[node.round_num - 1].children.append(make_match_score(node.team_1, node.team_2))

    # don't need connector col before first round
    if node.round_num > 1:
        if node.top_node is not None or node.bottom_node is not None:
            # insert merge or single connector
            if node.top_node is not None and node.bottom_node is not None:
                connector_cols[node.round_num - 2].children.append(connector_merge_grid)  # insert double connector
            else:
                connector_cols[node.round_num - 2].children.append(connector_single_grid)  # insert single connector

    # add top and bottom node matches
    add_match(match_cols, connector_cols, node.top_node)
    add_match(match_cols, connector_cols, node.bottom_node)
    return

def get_match_content(match_data:list[MatchNode]) -> tuple[list[html.Div], list[html.Div]]:
    """
    Construct a list of match columns and a list of connector columns for a match
    :param match_data: list of head match nodes
    :return: List of match columns, list of connector columns
    """
    round_num = match_data[0].round_num
    connector_cols = []

    # init match column list
    match_cols = [html.Div([], className=first_match_class if i == 0 else match_class) for i in range(round_num)]

    # connectors are only needed if bracket has more than 1 round
    if round_num > 1:
        # subtract 1 bc last round doesn't need connectors
        connector_cols = [html.Div([], className=conn_class) for _ in range(round_num - 1)]

    # call add_match on all head nodes
    for node in match_data:
        add_match(match_cols, connector_cols, node)

    # return lists of divs for match cols and connectors
    return match_cols, connector_cols

def build_bracket(bracket_id):
    """
    Build a bracket grid with data from given bracket id
    :param bracket_id:
    :return: a bracket_grid
    """
    # get data
    data = melee_db.get_bracket_info(bracket_id)
    matches, connectors = get_match_content(data)

    content = []
    for i in range(len(matches)):
        # different class name for first column
        class_name = 'pe-0' if i == 0 else 'ps-0 pe-0'

        # add match column
        content.append(dbc.Col(matches[i], width=match_width, className=class_name))

        # add connector column if needed
        if i < len(connectors):
            content.append(dbc.Col(connectors[i], width=con_width, className=class_name))

    bracket_grid = html.Div(content, className='d-flex flex-row')

    # should return a bracket_grid
    return bracket_grid

def layout(bracket_id=None, **kwargs):
    if bracket_id is not None:
        return dbc.Container([
            dbc.Row(dbc.Col(html.Div(f"Bracket {bracket_id} Results", className='text-center h1 mt-5 mb-0'))),
            html.Hr(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(build_bracket(bracket_id), width=8, className='ps-0 pe-0')
                ],
                align='center',
            )
        ])
    else:
        return dbc.Container([])
