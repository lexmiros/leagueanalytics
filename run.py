
from ntpath import join
from re import match

import pandas
from src.flaskApp import app, routes
from src.DataScripts.analysis import *
from src.DataScripts.CleanData import *
from src.DataScripts.GetData import *


if __name__ == "__main__":
    #app.run(debug=True) 
    
    user = "Frommoh"
    region = "OC1"

    
    puiid = get_puuid(user, region)

    #Get timeline match information
    my_match_ids = watcher.match.matchlist_by_puuid(region,puiid, start=0,  count=1)
  
    match_detail = watcher.match.timeline_by_match(region, my_match_ids[0])
    x = match_detail['info']['frames'][15]['participantFrames']['2']['damageStats']['totalDamageDoneToChampions']
    print(x)

    dfs = get_time_series_cs(user, region)
    print(dfs[0])
    print(dfs[1])
    print(dfs[2])
    print(dfs[3])
    
   
    """
    
    

    

    
    with open("output.txt", "w") as f:
        print(x, file=f)

    x = match_detail['info']['frames'][15]['participantFrames'][userId]['minionsKilled']
    print(x)
    """

    
    
    
    
    



 