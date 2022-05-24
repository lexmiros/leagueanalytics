
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

    df = get_time_series_cs(user, region)
    print(df)

    """
    #Get puuid for user
    puiid = get_puuid(user, region)

    #Get timeline match information
    my_match_ids = watcher.match.matchlist_by_puuid(region,puiid, start=0,  count=1)
  
    match_detail = watcher.match.timeline_by_match(region, my_match_ids[0])
    x = match_detail['info']['frames'][1]['participantFrames']['2']
    print(x)

    
    with open("output.txt", "w") as f:
        print(x, file=f)

    x = match_detail['info']['frames'][15]['participantFrames'][userId]['minionsKilled']
    print(x)
    """

    
    
    
    
    



 