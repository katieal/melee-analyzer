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


loc_frame = df_bracket.loc[20, 'matches']
print("list cont type: ", type(loc_frame[0]))
print(type(loc_frame[0]['results']))


def get_bracket_info(bracket_id):
    bracket_id = int(bracket_id)

    # get matches from the bracket
    matches = df_bracket.loc[bracket_id, 'matches']

    # find number of rounds
    rounds = 1
    for match in matches:
        if match['round'] > rounds:
            rounds = match['round']

    # add one list to match data for every round
    match_data = []
    for x in range(rounds - 1):
        match_data.append([])

    # add matches to match data, starting with the last round
    for round_num in range(rounds, 1, -1):
        for match in matches:
            if match['round'] == round_num:
                results = match['results']
                # make sure results has 2 entries
                if len(results) == 2:
                    match_data[round_num - 1].append(
                        {
                            'player_1': {
                                'name': results[0]['name'],
                                'score': results[0]['score'],
                                'winner': results[0]['winner'],
                            },
                            'player_2': {
                                'name': results[1]['name'],
                                'score': results[1]['score'],
                                'winner': results[1]['winner'],
                            }
                        }
                    )
                else:
                    raise Exception("bracket ", bracket_id, " round ", round_num, " has incorrect number of results")
                    return

    return match_data


class MeleeMatch(object):
    def __init__(self, bracket_id):
        self.bracket_id = int(bracket_id)