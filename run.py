from re import U


from flask import render_template

from src.DataScripts.analysis import *
from src.DataScripts.GetData import *
from src.DataScripts.CleanData import *
import pandas as pd
from src.flaskApp import app
from src.flaskApp import routes

if __name__ == "__main__":
    #user = "Drakuns"
    #region = "OC1"
    #no_games = 10000
    #df = get_match_details(user, region, no_games)
    #df.to_csv("./TestData")
    
    df = pd.read_csv("./TestData_Cleaned")
    df = pd.DataFrame(df)

    y = "WinLoss"
    x_list = ['Spell1Casts','SummonerSpell2','Spell2Casts','Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp','Damage','TotalDamageTaken','WardsPlace','WardsKilled']
    
    model = build_logit_model(df, y, x_list, 0.05)

    #app.run()