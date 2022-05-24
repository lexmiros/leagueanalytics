
from re import match
from src.flaskApp import app, routes
from src.DataScripts.analysis import *
from src.DataScripts.CleanData import *
from src.DataScripts.GetData import *


if __name__ == "__main__":
    #app.run(debug=True) 
    
    user = "Frommoh"
    region = "OC1"

    #Get puuid for user
    puiid = get_puuid(user, region)

    #Get timeline match information
    my_match_ids = watcher.match.matchlist_by_puuid(region,puiid, start=1,  count=1)
    match_detail = watcher.match.timeline_by_match(region, my_match_ids[0])

    #Match user puuid to match information data to find user participant ID
    puuid_list = match_detail['info']['participants']
    for row in puuid_list:
        if row['puuid'] == puiid:
            userId = row['participantId']
            userId = str(userId)
    
    x = match_detail['info']['frames']
    participants = []

    for row in x:
        participants_row = {}
        minion_kills = row['participantFrames'][userId]['minionsKilled']
        jg_camps = row['participantFrames'][userId]['jungleMinionsKilled']
        total_cs_point = minion_kills + jg_camps

        participants_row["Minion Kills"] = total_cs_point


        participants.append(participants_row)
    df = pd.DataFrame(participants)

    print(df)
        

    
    with open("output.txt", "w") as f:
        print(x, file=f)

    #x = match_detail['info']['frames'][15]['participantFrames'][userId]['minionsKilled']
    #print(x)

    
    
    
    
    



 