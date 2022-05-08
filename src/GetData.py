from matplotlib.pyplot import get
from src import *

"""
Return the user accountID for the given username and region
"""
def get_account_id(user, region):
    account_ID = watcher.summoner.by_name(region, user)
    account_ID = account_ID['accountId']
    return account_ID

"""
Return the user puuId for the given username and region
"""
def get_puuid(user, region):
    puuid = watcher.summoner.by_name(region, user)
    puuid = puuid["puuid"]
    return puuid

"""
Return the user ID for the given username and region
"""
def get_id(user, region):
    id = watcher.summoner.by_name(region, user)
    id = id["id"]
    return id

"""
Get the account summary information for the user
"""
def get_account_info(user, region):
    id = get_id(user, region)
    ranked_info = watcher.league.by_summoner(region, id)
    return(ranked_info)

"""
Get a list of match IDs for the match hisotry of the user and region
"""
def get_match_history(user, region):
    puiid = get_puuid(user, region)
    my_match_ids = watcher.match.matchlist_by_puuid(region,puiid, count=100)
    return my_match_ids


"""
Get a match ID for the last match played for the user and region
"""
def get_last_match_history(user, region):
    match_id = get_match_history(user,region)
    return match_id[0]

"""
Get a match ID for the first match played for the user and region that is available
"""
def get_first_match_history(user, region):
    match_id = get_match_history(user,region)
    return match_id[-1]


"""
Get a timeline for a match
"""
def get_match_timeline(user, region):
    first_match_id = get_first_match_history(user, region)
    first_match_timeline = watcher.match.timeline_by_match(region,first_match_id)
    return first_match_timeline



"""
Given a user and a region, returns a dataframe filled with information for the given users games
"""
def get_match_details(user, region):
    #Gets a list of match_ids 
    match_ids = get_match_history(user, region)
    #Creates an empty list to populate with dictionaries
    #Each element of the list will be one game
    participants = []

    #For each match ID in the list of match_ids
    for id in match_ids:

        #Gets the information for the match
        match_detail = watcher.match.by_id(my_region, id)
        
        #For each participant in the match
        for row in match_detail['info']['participants']:
            #If the participant is the user, create a dictionary and populate
            if row['summonerName'] == user:
                participants_row = {}
                participants_row['SummonerName'] = row['summonerName']
                participants_row['WinLoss']    = row['win']
                participants_row['Lane'] = row['individualPosition']
                participants_row['Champion'] = row['championName']
                participants_row['SummonerSpell1'] = row['summoner1Id']
                participants_row['Spell1Casts'] = row['summoner1Casts']
                participants_row['SummonerSpell2'] = row['summoner2Id']
                participants_row['Spell2Casts'] = row['summoner2Casts']
                participants_row['Q casts'] = row['spell1Casts']
                participants_row['W casts'] = row['spell2Casts']
                participants_row['E casts'] = row['spell3Casts']
                participants_row['R casts'] = row['spell4Casts']
                participants_row['ChampLevel'] = row['champLevel']
                participants_row['CS']    = row['totalMinionsKilled']
                participants_row['Kills']    = row['kills']
                participants_row['Deaths']    = row['deaths']
                participants_row['Assists']    = row['assists']
                participants_row['Exp']    = row['champExperience']
                participants_row['Damage'] = row['totalDamageDealtToChampions']
                participants_row['TotalDamageTaken'] = row['totalDamageTaken']
                participants_row['WardsPlace']    = row['wardsPlaced']
                participants_row['WardsKilled']    = row['wardsKilled']

                #Append the dictionary to the list
                participants.append(participants_row)
    #Create a dataframe from the list of dictionaries             
    df = pd.DataFrame(participants)

    return df
