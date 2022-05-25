
from ntpath import join
from re import match

from src.flaskApp import app, routes





if __name__ == "__main__":
   
    
    app.run(debug=True) 
    

    #user = "Ausfreak"
    #region = "OC1"
    #get_match_details(user, region, 400)

   
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

    
    
    
    
    



 