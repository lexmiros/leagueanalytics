from turtle import pu
from src import pd
from src.DataScripts import watcher
from src.DataScripts.analysis import user_win_loss_wr
from src.DataScripts.CleanData import *
import csv
from csv import DictWriter


def get_account_id(user: str, region:str) -> str:
    """
    Return the user accountID for the given username and region

    Account IDs are an ID for the Riot Games account, 
    and are unique per region

    Parameteres:
    -----------
    user : str
        The summoner name
    region : str
        The region associated with the account

    Returns
    -------
    str
        The account's ID
    
    """

    account_ID = watcher.summoner.by_name(region, user)
    account_ID = account_ID['accountId']
    return account_ID

def get_puuid(user: str, region: str) -> str:
    """
    Return the user puuID for the given username and region

    puuIDs are IDs for a Riot Games account and are unique 
    globally 

    Parameteres:
    -----------
    user : str
        The summoner name
    region : str
        The region associated with the account

    Returns
    -------
    str
        The account's puuID
    
    """
    puuid = watcher.summoner.by_name(region, user)
    puuid = puuid["puuid"]
    return puuid

def get_id(user: str, region: str) -> str:
    """
    Return the user ID for the given username and region

    ID is the ID for a league of legends summoner,
    and is unique per region

    Parameteres:
    -----------
    user : str
        The summoner name
    region : str
        The region associated with the summoner

    Returns
    -------
    str
        The summoner's ID
    
    """
    id = watcher.summoner.by_name(region, user)
    id = id["id"]
    return id


def get_account_info(user: str, region: str) -> list:
    """
    Return the user's account information based on their
    summoner name and region

    Inlcudes their rankes for queue types, wins, losses,
    if they're clasified as a veteran, freshblood, on a hotsteak, 
    inactive

    Parameteres:
    -----------
    user : str
        The summoner name
    region : str
        The region associated with the account

    Returns
    -------
    list
        List of summoner's summary information
    
    """
    id = get_id(user, region)
    ranked_info = watcher.league.by_summoner(region, id)
    return(ranked_info)




def get_match_history_start(user: str, region: str, start_index: int) -> list:
    """
    Return a list of match IDs that the summoner has played in,
    beggining from the start_index

    Parameteres:
    -----------
    user : str
        The summoner name
    region : str
        The region associated with the account
    start_index : int
        Offset the search and start from the given index

    Returns
    -------
    list
        A list of 100 match IDs 
    
    """
    puiid = get_puuid(user, region)
    my_match_ids = watcher.match.matchlist_by_puuid(region,puiid, start=start_index,  count=100)
    return my_match_ids



def get_rank(user: str, region: str) -> str:
    """
    Returns the rank for a user in a region

    Parameteres:
    -----------
    user : str
        The summoner name
    region : str
        The region associated with the account

    Returns
    -------
    str
        The rank of the summoner
    
    """
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

def get_match_details(user, region, number_games):
    """
    Create a dataframe containing details from the user's
    match history

    Finds the match history of a user, and populates a pandas
    dataframe with summary information for the user, and all 
    other players in the user's games. 

    Terminates if an empty list of match histories is found,
    meaning all matches available from the Riot server has been
    found

    Parameteres:
    -----------
    user : str
        The username of the account
    region : str
        The region associated with the account
    int : number_games
        The number of games to search for

    Returns
    -------
    Pandas Dataframe
        A df of summary information for all players in the
        user's games
    
    """


    #Gets a list of match_ids 
    i = 0
    j = 0

    #Column headings for the CSV file
    headersCSV = ['SummonerName','WinLoss','Lane','Champion','Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp','Damage','Shielding','Healing','Total Damage Taken','Wards Placed','Wards Killed','Vision Score','Penta Kills','Game Time seconds','Crowd Control','Time spent dead','Kill participation','Team damage percentage','Skillshots hit','Skillshots dodged','Solo kills','Turret plates taken']
    
    #Create CSV file with headings
    with open(f"./newdata{user}.csv", 'w', newline='', encoding="utf-8") as newcsv:
        writer = csv.writer(newcsv)
        writer.writerow(headersCSV)

    #Iterate over each batch of 100 games
    while i < number_games: 
        match_ids = get_match_history_start(user, region, start_index=i)
        
        #Check of match_Ids returned are empty therefore found all games
        if match_ids == []:
            print("Found all matches")
            break
        else:
            #For each match ID in the list of match_ids
            for id in match_ids:    
                #Gets the information for the match
                match_detail = watcher.match.by_id(region, id)

                for row in match_detail['info']['participants']:

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
                        with open(f'./newdata{user}.csv', 'a', newline='', encoding="utf-8") as f_object:
                            # Pass the CSV  file object to the Dictwriter() function
                            # Result - a DictWriter object
                            dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
                            # Pass the data in the dictionary as an argument into the writerow() function
                            dictwriter_object.writerow(participants_row)
                            # Close the file object
                            f_object.close()
                        print(j)
                        j += 1

        #Iterate over next 100 games
        i = i + 100
    
    #Read in final csv to df and clean
    df = pd.read_csv(f"./newdata{user}.csv")
    df = pd.DataFrame(df)
    df = col_to_string(df, "WinLoss")
    df["WinLoss"] = df["WinLoss"].map(encode_true_false)
    df = impute_mode_lane(df)
    df = encode_categorical(df, "Lane")

    #Save back to csv
    df.to_csv(f"./newdata{user}.csv")

    return 


            
    

def webpage_transfer(user, region, test):

    if test == "False":
        data_loc = f"./newdata{user}.csv"
        df = pd.read_csv(data_loc)
        df = pd.DataFrame(df)
    else:
        data_loc = f"./TestData_Cleaned_2.csv"
        df = pd.read_csv(data_loc)
        df = pd.DataFrame(df)
    
    #Get top nav bar info
    results = user_win_loss_wr(df, user)
    rank = get_rank(user, region)
  
    #Build topnav info
    wins = results[0]
    losses = results[1]
    wr = results[2]
    total_games = wins + losses

    return(df, rank, wins, losses, wr, total_games)

def get_time_series_user_id(user:str, region:str, match_detail:dict) -> str:
    """
    Finds the puuid for a user and matches it against timeline
    record data to find the user's participant iD within
    the match

    Parameters:
    -----------
    user : str
        The username of the account
    region : str
        The region associated with the account
    match_detail : dict
        The match details returend from 
        riotWatcher.match.timeline_by_match
    Returns:
    --------
    str:
        user's participant ID for the match as a string
    """
    puiid = get_puuid(user, region)

    puuid_list = match_detail['info']['participants']
    for row in puuid_list:
        if row['puuid'] == puiid:
            userId = row['participantId']
            userId = str(userId)

    return userId


def get_time_series_user(user: str, region: str) -> pd.DataFrame:
    """
    Get minute-by-minute cs, dmg, exp, gold for 100 games 

    For the user, get four dataframes that contain elapsed time
    in minutes as the index, a metric per game as the column

    Parameters:
    -----------
    user : str
        The username of the account
    region : str
        The region associated with the account
    
    Returns:
    --------
    Pandas dataframe
    """
    
    #Get puuid for user
    puiid = get_puuid(user, region)

    #Get timeline match information
    my_match_ids = watcher.match.matchlist_by_puuid(region, puiid, start=0,  count=100)    
    
    #Initialise dataframes for each metric
    df_cs = pd.DataFrame()
    df_cs_temp = pd.DataFrame()

    df_xp = pd.DataFrame()
    df_xp_temp = pd.DataFrame()

    df_gold = pd.DataFrame()
    df_gold_temp = pd.DataFrame()

    df_dmg = pd.DataFrame()
    df_dmg_temp = pd.DataFrame()
    
    #For each match found
    for match_id in my_match_ids:

        #Empty list for each metric
        participants_cs = []
        participants_xp = []
        participants_gold = []
        participants_dmg = []

        #Get timeline data for the match 
        match_detail = watcher.match.timeline_by_match(region, match_id)
        
        #Match user puuid to match information data to find user participant ID
        userId = get_time_series_user_id(user, region, match_detail)
        data = match_detail['info']['frames']
        
        #For each minute in the game
        for row in data:
            #CS
            participants_row_cs = {}
            minion_kills = row['participantFrames'][userId]['minionsKilled']
            jg_camps = row['participantFrames'][userId]['jungleMinionsKilled']
            total_cs_point = minion_kills + jg_camps

            participants_row_cs["Minion Kills"] = total_cs_point
            participants_cs.append(participants_row_cs)

            #exp
            participants_row_xp = {}
            xp = row['participantFrames'][userId]['xp']
            participants_row_xp["xp"] = xp
            participants_xp.append(participants_row_xp)

            #gold
            participants_row_gold = {}
            gold = row['participantFrames'][userId]['totalGold']
            participants_row_gold["Gold"] = gold
            participants_gold.append(participants_row_gold)

            #damage
            participants_row_dmg = {}
            dmg = row['participantFrames'][userId]['damageStats']['totalDamageDoneToChampions']
            participants_row_dmg["Damage"] = dmg
            participants_dmg.append(participants_row_dmg)



        #Merge main df with temp, reset temp

        #CS
        df_cs_temp = pd.DataFrame(participants_cs)
        df_cs = pd.merge(df_cs, df_cs_temp, how='outer', left_index=True, right_index=True)
        df_cs_temp = pd.DataFrame()

        #xp
        df_xp_temp = pd.DataFrame(participants_xp)
        df_xp = pd.merge(df_xp, df_xp_temp, how='outer', left_index=True, right_index=True)
        df_xp_temp = pd.DataFrame()

        #gold
        df_gold_temp = pd.DataFrame(participants_gold)
        df_gold = pd.merge(df_gold, df_gold_temp, how='outer', left_index=True, right_index=True)
        df_gold_temp = pd.DataFrame()

        #damage
        df_dmg_temp = pd.DataFrame(participants_dmg)
        df_dmg = pd.merge(df_dmg, df_dmg_temp, how='outer', left_index=True, right_index=True)
        df_dmg_temp = pd.DataFrame()




 

    return df_cs, df_xp, df_gold, df_dmg

def get_time_series_non_user(user: str, region: str) -> pd.DataFrame:
    """
    Get minute-by-minute cs, dmg, exp, gold for 100 games 

    For everyone except the user, get four dataframes that contain elapsed time
    in minutes as the index, a metric per game as the column. Average each non-user's
    metric and return the average as a single point in time

    Parameters:
    -----------
    user : str
        The username of the account
    region : str
        The region associated with the account
    
    Returns:
    --------
    Pandas dataframe
    """
    
    #Get puuid for user
    puiid = get_puuid(user, region)

    #Get timeline match information
    my_match_ids = watcher.match.matchlist_by_puuid(region, puiid, start=0,  count=100)    
    
    #Initialise dataframes for each metric
    df_cs = pd.DataFrame()
    df_cs_temp = pd.DataFrame()

    df_xp = pd.DataFrame()
    df_xp_temp = pd.DataFrame()

    df_gold = pd.DataFrame()
    df_gold_temp = pd.DataFrame()

    df_dmg = pd.DataFrame()
    df_dmg_temp = pd.DataFrame()
    
    #For each match found
    for match_id in my_match_ids:

        #Empty list for each metric
        participants_cs = []
        participants_xp = []
        participants_gold = []
        participants_dmg = []

        #Get timeline data for the match 
        match_detail = watcher.match.timeline_by_match(region, match_id)
        
        #Match user puuid to match information data to find user participant ID
        userId = get_time_series_user_id(user, region, match_detail)
        data = match_detail['info']['frames']

        #Get a list of 1 - 10 (participant IDs for 10 players)
        all_ids = list(range(1,11))
        all_ids = [str(x) for x in all_ids]
        #Remove user from all participant IDs
        all_ids.remove(userId)

        #For each minute in the game
        for row in data:
            #CS
            cs_avg_list = []
            for userId in all_ids:
                participants_row_cs = {}
                minion_kills = row['participantFrames'][userId]['minionsKilled']
                jg_camps = row['participantFrames'][userId]['jungleMinionsKilled']
                total_cs_point = minion_kills + jg_camps
                #participants_row_cs["Minion Kills"] = total_cs_point
                cs_avg_list.append(total_cs_point)
            
            #Remove lowest two numbers from average
            #LIEKLY to be two in players in support role
            #Who do not traditionally CS
            cs_avg_list.sort()
            cs_avg_list.pop(0)
            cs_avg_list.pop(0)

            cs_avg = sum(cs_avg_list) / len(cs_avg_list)

            participants_row_cs["Minion Kills"] = cs_avg

            participants_cs.append(cs_avg)

            #exp
            xp_avg_list = []
            for userId in all_ids:
                participants_row_xp = {}
                xp = row['participantFrames'][userId]['xp']
                xp_avg_list.append(xp)

            xp_avg = sum(xp_avg_list) / len(xp_avg_list)
            participants_row_xp["Experience"] = xp_avg
            participants_xp.append(xp_avg)
            

            #gold
            gold_avg_list = []
            for userId in all_ids:
                participants_row_gold = {}
                gold = row['participantFrames'][userId]['totalGold']
                gold_avg_list.append(gold)
            
            #Remove lowest two numbers from average
            #LIEKLY to be two in players in support role
            #Who traditionally do not generate much gold
            gold_avg_list.sort()
            gold_avg_list.pop(0)
            gold_avg_list.pop(0)

            gold_avg = sum(gold_avg_list) / len(gold_avg_list)
            participants_row_gold["Experience"] = gold_avg
            participants_gold.append(gold_avg)

            #damage
            dmg_avg_list = []
            for userId in all_ids:
                participants_row_dmg = {}
                dmg = row['participantFrames'][userId]['damageStats']['totalDamageDoneToChampions']
                dmg_avg_list.append(dmg)
            
            #Remove lowest two numbers from average
            #LIEKLY to be two in players in support role
            #Who traditioanlly don't deal a lot of damage
            dmg_avg_list.sort()
            dmg_avg_list.pop(0)
            dmg_avg_list.pop(0)

            dmg_avg = sum(dmg_avg_list) / len(dmg_avg_list)
            participants_row_dmg["Experience"] = dmg_avg
            participants_dmg.append(gold_avg)




        #Merge main df with temp, reset temp

        #CS
        df_cs_temp = pd.DataFrame(participants_cs)
        df_cs = pd.merge(df_cs, df_cs_temp, how='outer', left_index=True, right_index=True)
        df_cs_temp = pd.DataFrame()

        #xp
        df_xp_temp = pd.DataFrame(participants_xp)
        df_xp = pd.merge(df_xp, df_xp_temp, how='outer', left_index=True, right_index=True)
        df_xp_temp = pd.DataFrame()

        #gold
        df_gold_temp = pd.DataFrame(participants_gold)
        df_gold = pd.merge(df_gold, df_gold_temp, how='outer', left_index=True, right_index=True)
        df_gold_temp = pd.DataFrame()

        #damage
        df_dmg_temp = pd.DataFrame(participants_dmg)
        df_dmg = pd.merge(df_dmg, df_dmg_temp, how='outer', left_index=True, right_index=True)
        df_dmg_temp = pd.DataFrame()




 

    return df_cs, df_xp, df_gold, df_dmg

    