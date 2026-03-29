# Import Packages
import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from melee_data import TeamInfo
from melee_data import MatchInfo
from melee_data import MatchNode
import melee_data

# Helper class for building bracket views

# =============================
# === Embedded Bracket View ===
# =============================
def make_embed_view(website, url):
    """
    Return a html.Iframe with the embedded bracket
    :param website: website name (Challonge, Start.gg, Other)
    :param url: url to bracket
    :return: html.Div with embedded bracket
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

# =============================
# === Custom Bracket View ===
# =============================

_match_width = 3
_con_width = 1
_first_match_class = 'd-flex flex-column justify-content-evenly'
_match_class = 'd-flex flex-column h-100'
_conn_class = 'd-flex flex-column h-100 justify-content-evenly'

def make_custom_view(match_data, match_size):
    """
    Build a bracket grid with data from given bracket id
    :param match_data: list of head match nodes
    :param match_size: list of match sizes
    :return: html.Div with a bracket_grid
    """
    # construct lists for match and connector columns
    matches, connectors = _get_match_content(match_data, match_size)

    content = []
    for i in range(len(matches)):
        # different class name for first column
        class_name = 'pe-0' if i == 0 else 'ps-0 pe-0'

        # add match column
        content.append(dbc.Col(matches[i], width=_match_width, className=class_name))

        # add connector column if needed
        if i < len(connectors):
            content.append(dbc.Col(connectors[i], width=_con_width, className=class_name))

    bracket_grid = html.Div(content, className='d-flex flex-row')

    # should return a bracket_grid
    return bracket_grid

def _get_match_content(match_data:list[MatchNode], match_size:list[int]) -> tuple[list[html.Div], list[html.Div]]:
    """
    Construct a list of match columns and a list of connector columns for a match
    :param match_data: list of head match nodes
    :param match_size: list of match sizes
    :return: List of match columns, list of connector columns
    """
    # get starting round num
    round_num = match_data[0].round_num
    connector_cols = []

    # init match column list
    match_cols = [html.Div([], className=_first_match_class if i == 0 else _match_class) for i in range(round_num + 1)]

    # connectors are only needed if bracket has more than 1 round
    if round_num > 0:
        # subtract 1 bc last round doesn't need connectors
        connector_cols = [html.Div([], className=_conn_class) for _ in range(round_num)]

    # call add_match on all head nodes
    for node in match_data:
        _add_match(match_size, match_cols, connector_cols, node, False, False)

    # return lists of divs for match cols and connectors
    return match_cols, connector_cols

def _add_match(match_size:list[int], match_cols:list[html.Div], connector_cols:list[html.Div],
              node:MatchNode, add_margin_top:bool, add_margin_bottom:bool):
    """
    Recursive method to construct list of matches and list of columns.
    Will immediately return if node is None
    :param match_size:
    :param add_margin_bottom:
    :param add_margin_top:
    :param match_cols: list containing html.Divs for matches
    :param connector_cols: list containing html.Divs for connectors
    :param node: the current MatchNode to be added
    :return: None
    """
    # check for valid node
    if node is None:
        return

    # don't need connector col before first round
    if node.round_num > 0:
        if node.top_node is not None or node.bottom_node is not None:
            # insert merge or single connector
            if node.top_node is not None and node.bottom_node is not None:
                # insert match with default height
                match_cols[node.round_num].children.append(
                    _make_match_score(node.team_1, node.team_2, add_margin_top, add_margin_bottom))
                # insert merge connector
                connector_cols[node.round_num - 1].children.append(_get_connector(False))  # insert double connector
            else:
                # calculate height percentage to be same as height of match in prev round
                height = (2 / match_size[node.round_num - 1]) * 100
                # cap at 100%
                height = 100 if height > 100 else height
                h_percent = str(int(height)) + "%"

                # insert match with custom height
                match_cols[node.round_num].children.append(
                    _make_match_score(node.team_1, node.team_2, add_margin_top, add_margin_bottom, h_percent))
                # insert single connector with custom height
                connector_cols[node.round_num - 1].children.append(_get_connector(True, h_percent))  # insert single connector
    else:
        # add match with default height
        match_cols[node.round_num].children.append(
            _make_match_score(node.team_1, node.team_2, add_margin_top, add_margin_bottom))

    # add top and bottom node matches
    _add_match(match_size, match_cols, connector_cols, node.top_node, True, False)
    _add_match(match_size, match_cols, connector_cols, node.bottom_node, False, True)
    return

# ======== Connectors ========
_base_border_class = 'flex-grow-1 border border-2'
_border_top_class = 'border-start-0 border-end-0 border-bottom-0'
_border_bottom_class = 'border-start-0 border-end-0 border-top-0'

_connector_merge = html.Div(
    [
        html.Div(
            [
                html.Div(className=_base_border_class + ' ' + _border_bottom_class), # bot
                html.Div(className=_base_border_class + ' border-start-0 border-bottom-0'), # top and end
                html.Div(className=_base_border_class + ' border-start-0 border-top-0'), # bot and end
                html.Div(className=_base_border_class + ' ' + _border_top_class) # top
            ],
            className='h-100 d-flex flex-column',
        )
    ],
    className='flex-grow-1'
)

_connector_single = html.Div(
    [
        html.Div(
            [
                html.Div(className='flex-grow-1'), # none
                html.Div(className=_base_border_class + ' ' + _border_bottom_class), # bot
                html.Div(className=_base_border_class + ' ' + _border_top_class), # top
                html.Div(className='flex-grow-1') # none
            ],
            className='h-100 d-flex flex-column',
        )
    ],
    className='flex-grow-1'
)

def _get_connector(is_single:bool, height:str=None) -> html.Div:

    flex_class = '' if height else 'flex-grow-1 '

    return html.Div(
        [
            _connector_single if is_single else _connector_merge,
            _connector_single
        ],
        className=flex_class + ' d-flex flex-row',
        style={
            'height': height if height else 'auto'
        }
    )

# ======== Match Scores ========
_player_name_border = 'border border-2 rounded-start-3 border-end-0'
_player_score_border = 'border border-2 rounded-end-3 border-start-0'
_bg_fill_class = 'bg-light border border-2'

# single (aka match_single)
def _make_team_score(team_info:TeamInfo, add_margin_bot:bool):
    """
    Make a dbc.ListGroup for a single team's name and score
    :param add_margin_bot: should a bottom margin be included?
    :param team_info: team info dict
    :return:
    """
    margin = 'mb-2' if add_margin_bot else ''
    bg_color = ' bg-success ' if team_info['winner'] else ' bg-danger '
    return dbc.ListGroup(
        [
            dbc.ListGroupItem(team_info['name'], class_name='flex-fill ' + _player_name_border),
            dbc.ListGroupItem(team_info['score'], class_name=bg_color + _player_score_border)
        ],
        horizontal=True,
        class_name='flex-fill ' + margin
    )

# double (aka match_pair or get_flex_match_single)
def _make_match_score(team_1:TeamInfo, team_2:TeamInfo, add_space_top:bool, add_space_bot:bool, height=""):
    """
    Return a div containing team 1 and 2 scores
    :param height:
    :param team_1:
    :param team_2:
    :param add_space_top:
    :param add_space_bot:
    :return:
    """

    flex_class = ' flex-fill ' if height == "" else ''
    margin_top = ' mt-1 ' if add_space_top else ' '
    margin_bot = ' mb-1 ' if add_space_bot else ' '

    return html.Div(
        html.Div(
            [
                _make_team_score(team_1, True),
                _make_team_score(team_2, False)
            ],
            className='flex-fill my-2'
        ),
        className=flex_class + 'd-flex align-items-center' + margin_top + margin_bot,
        style={
            'height': height if height != "" else 'auto'
        }
    )