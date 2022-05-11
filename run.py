from re import U
from src.GetData import get_match_details
from src.analysis import logit_model
import pandas as pd

if __name__ == "__main__":
    #user = "Drakuns"
    #region = "OC1"
    #no_games = 10000
    #df = get_match_details(user, region, no_games)
    #df.to_csv("./TestData")
    
    df = pd.read_csv("./TestData_Cleaned")
    df = pd.DataFrame(df)
    x_list = ['Spell1Casts','SummonerSpell2','Spell2Casts','Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp','Damage','TotalDamageTaken','WardsPlace','WardsKilled','BOTTOM','JUNGLE','MIDDLE','TOP','UTILITY']
    model = logit_model(df, "WinLoss", x_list)
    print(model.summary2())