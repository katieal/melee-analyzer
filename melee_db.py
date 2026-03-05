from pymongo import MongoClient
import pandas as pd

# Import CRUD Module
from db_crud import MeleeAnalyzer

# Connect to database
username = "admin"
password = "AmyFest1"
db = MeleeAnalyzer(username, password)

# import data into dataframe
df = pd.DataFrame.from_records(data=db.read({}))
df.drop(columns=['_id'],inplace=True)

df_bracket = pd.DataFrame.from_records(data=db.read({}), index=['bracket_id'])
df_bracket.drop(columns=['_id'],inplace=True)

# ============ JSON Data Structure Info ============
# ----------- Tournament -----------
#   'bracket_id': int
#   'name': string
#   'date': string
#   'location': string
#   'mode': string
#   'theme': string
#   'winner': string(PlayerName)
#   'matches': list(MatchDict)
#
# ----------- MatchDict -----------
#   'bracket': string [Main/Upper/Lower/Winner's/Loser's]
#   'round': int
#   'team_1': TeamInfo
#   'team_2': TeamInfo
#
# ----------- TeamInfo -----------
#   'name': string
#   'player_names': list(string)
#   'score': int
#   'winner': boolean
#   'games': GameInfo
#

def get_bracket_info(bracket_id):
    """
    Given a bracket id, return a list of MatchNode head nodes,
     with one node for each match in the final round of a bracket. Each node is
     the head node for a linked list.
    :param bracket_id: the bracket_id field of the bracket
    :return: a list of MatchNode objects
    """
    bracket_id = int(bracket_id)

    # get matches from the bracket (list of dicts)
    matches = df_bracket.loc[bracket_id, 'matches']

    # find highest round number
    max_rounds = 1
    for match in matches:
        if match['round'] > max_rounds:
            max_rounds = match['round']

    # array of linked list nodes
    match_data = make_linked_list(matches[:], max_rounds)
    return match_data


def make_linked_list(match_list, round_num):
    """
    Create a head node for each match in the final round, then call
    make_node to link all previous matches to the node
    :param match_list: List of match dicts to draw from
    :param round_num: Round number of the final round in the bracket
    :return: List of head MatchNode objects
    """
    # list to hold head nodes
    match_nodes = []
    # get list of final matches
    final_matches = []
    for match in match_list:
        if match['round'] == round_num:
            final_matches.append(match)

    # add one node to list per match in final round
    for match in final_matches:
        # remove from list of matches
        match_list.remove(match)
        # create new node
        node = MatchNode(match)
        # check if there are previous rounds
        if round_num - 1 >= 1:
            # assign top and bottom nodes
            node.top_node, match_list = make_node(match_list, round_num - 1, match['team_1']['name'], node)
            node.bottom_node, match_list = make_node(match_list, round_num - 1, match['team_2']['name'], node)
        # add node to list
        match_nodes.append(node)

    print_nodes(match_nodes, match_list)

    return match_nodes

def make_node(match_list, round_num, name, next_node):
    """
    Search match_list for a match dict with specified round_num and name (can be team_1 or team_2).
    If found, create a new node for the match dict and call make_node to link previous matches.
    :param match_list: list of remaining unlinked match dicts
    :param round_num: current round number to search for
    :param name: current team name to search for
    :param next_node: node to assign to the next_node field of a new node
    :return: the completed MatchNode object
    """
    # search match_list for round_num and name
    prev_match = None
    node = None
    for match in match_list:
        if match['round'] == round_num:
            # if team's previous match is found
            if match['team_1']['name'] == name or match['team_2']['name'] == name:
                prev_match = match
                break
    # if found
    if prev_match is not None:
        # remove it from match list
        match_list.remove(prev_match)
        # make new node with result
        node = MatchNode(prev_match)
        node.next_node = next_node
        # check if there are previous rounds
        if round_num - 1 >= 1:
            # assign top and bottom nodes
            node.top_node, match_list = make_node(match_list, round_num - 1, prev_match['team_1']['name'], node)
            node.bottom_node, match_list = make_node(match_list, round_num - 1, prev_match['team_2']['name'], node)

    return node, match_list

def print_nodes(match_nodes, match_list):
    print("========== Linked List Info ==========")
    print("items left in list: ", len(match_list))
    print("head nodes in list: ", len(match_nodes))


class MatchNode(object):
    # pass in a match dict
    def __init__(self, match):
        self.round_num = match['round']
        self.team_1 = match['team_1']
        self.team_2 = match['team_2']
        self.top_node = None
        self.bottom_node = None
        self.next_node = None

    def print(self):
        print("========== Node Info ==========")
        print("round: ", self.round_num)
        print("player1: ", self.team_1)
        print("player2: ", self.team_2)
        print("top_node: ", self.top_node)
        print("bottom_node: ", self.bottom_node)
        print("next_node: ", self.next_node)