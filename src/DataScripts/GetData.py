from unittest import skip
from matplotlib.pyplot import get
from src.DataScripts import *
import time
import pandas as pd

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
Get a list of match IDs for the match hisotry of the user and region given a specific start-point
"""
def get_match_history_start(user, region, start_index):
    puiid = get_puuid(user, region)
    my_match_ids = watcher.match.matchlist_by_puuid(region,puiid, start=start_index,  count=100)
    return my_match_ids

def get_rank(user, region):
    account_info = get_account_info(user, region)
    tier = ""
    rank = ""
    for row in account_info:
        #try:
        tier = row['tier']
        rank = row['rank']
        #except:
           # pass

    current_rank = tier + " " + rank

    return current_rank

"""
Given a user and a region, returns a dataframe filled with information for the given users games
"""
def get_match_details(user, region, number_games):
    #Gets a list of match_ids 
    i = 0
    j = 0
    #Creates an empty list to populate with dictionaries
    #Each element of the list will be one game
    participants_1 = []
   
    while i < number_games: 
        match_ids = get_match_history_start(user, region, start_index=i)
        
        if match_ids == []:
            print("Found all matches")
            break
        else:
        
            #For each match ID in the list of match_ids
            for id in match_ids:    
                #Gets the information for the match
                match_detail = watcher.match.by_id(region, id)
                #print(len(match_detail))
                #For each participant in the match
                for row in match_detail['info']['participants']:
                    #If the participant is the user, create a dictionary and populate
                    #if row['summonerName'] == user:
                        #try:
                            participants_row = {}
                            participants_row['SummonerName'] = row['summonerName']
                            participants_row['WinLoss']    = row['win']
                            participants_row['Lane'] = row['individualPosition']
                            participants_row['Champion'] = row['championName']
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
                            participants_row['Shielding'] = row['totalDamageShieldedOnTeammates']
                            participants_row['Healing'] = row['totalHeal']
                            participants_row['Total Damage Taken'] = row['totalDamageTaken']
                            participants_row['Wards Placed']    = row['wardsPlaced']
                            participants_row['Wards Killed']    = row['wardsKilled']
                            participants_row['Vision Score']    = row['visionScore']
                            participants_row['Penta Kills']    = row['pentaKills']
                            participants_row['Game Time seconds']    = row['timePlayed']
                            participants_row['Crowd Control']    = row['totalTimeCCDealt']
                            participants_row['Time spent dead']    = row['totalTimeSpentDead']
                            try:
                                participants_row['Kill participation'] = row["challenges"]["killParticipation"]
                            except:
                                participants_row['Kill participation'] = 0
                            try:
                                participants_row['Team damage percentage']    = row["challenges"]['teamDamagePercentage']
                            except:
                                participants_row['Team damage percentage']    = 0
                            try:
                                participants_row['Skillshots hit']    = row["challenges"]['skillshotsHit']
                            except:
                                participants_row['Skillshots hit']    = 0 
                            try:
                                participants_row['Skillshots dodged']    = row["challenges"]['skillshotsDodged']
                            except:
                                participants_row['Skillshots dodged']    = 0
                            try:
                                participants_row['Solo kills']    = row["challenges"]['soloKills']
                            except:
                                participants_row['Solo kills']    = 0 
                            try:
                                participants_row['Turret plates taken']    = row["challenges"]['turretPlatesTaken']
                            except:
                                participants_row['Turret plates taken']    = 0 
                            
                            #Append the dictionary to the list
                            participants_1.append(participants_row)
                        #except:
                          #  pass

                j = j + 1
                print(j)
               

        #time.sleep(120)
        i = i + 100
        
        #Create a dataframe from the list of dictionaries             
    df = pd.DataFrame(participants_1)

    return df
