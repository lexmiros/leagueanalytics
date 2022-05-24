
from ntpath import join
from re import match

import pandas

from src.flaskApp import app, routes
from src.DataScripts.analysis import *
from src.DataScripts.CleanData import *
from src.DataScripts.GetData import *


if __name__ == "__main__":
    app.run(debug=True) 
 
    
   
   
   
    """
    
     
    dfs = get_time_series_cs(user, region)
    cs = dfs[0]
    exp = dfs[1]
    gold = dfs[2]
    damage = dfs[3]

    cs.to_csv("./TestData_cs.csv")
    exp.to_csv("./TestData_exp.csv")
    gold.to_csv("./TestData_gold.csv")
    damage.to_csv("./TestData_dmg.csv")
    

    

    
    with open("output.txt", "w") as f:
        print(x, file=f)

    x = match_detail['info']['frames'][15]['participantFrames'][userId]['minionsKilled']
    print(x)
    """

    
    
    
    
    



 