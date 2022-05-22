from src import pd
from src.DataScripts import watcher
from src.DataScripts.analysis import user_win_loss_wr


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
                        participants_1.append(participants_row)
                j = j + 1
                print(j)
               

        #time.sleep(120)
        i = i + 100
        
    #Create a dataframe from the list of dictionaries             
    df = pd.DataFrame(participants_1)

    return df

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