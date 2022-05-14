from enum import unique
from re import U


from flask import render_template

from src.DataScripts.analysis import *
from src.DataScripts.GetData import *
from src.DataScripts.CleanData import *
import pandas as pd
from src.flaskApp import app
from src.flaskApp import routes

if __name__ == "__main__":
    user = "Drakuns"
    region = "OC1"
    #no_games = 5000
    #df = get_match_details(user, region, no_games)
    #df.to_csv("./TestData_1")
    
    #df = pd.read_csv("TestData_1")
    #df = pd.DataFrame(df)
    #print(df.head())    
    #df = col_to_string(df, "WinLoss")
    #df["WinLoss"] = df["WinLoss"].map(encode_true_false)
    #df = impute_mode_lane(df)
    #df = encode_categorical(df, "Lane")
    #df.to_csv("TestData_1_cleaned")

    df = pd.read_csv("./TestData_1_cleaned")
    df = pd.DataFrame(df)
    print(df.dtypes)

    df = df[df["SummonerName"] == user]
    print(df)
   

    y = "WinLoss"
    #X = ['ChampLevel','CS','Kills','Deaths','Assists','Exp','Damage','Shielding','Healing','TotalDamageTaken','WardsPlace','WardsKilled','Vision Score','Penta Kills','Game Time seconds','Total time CCing','Time spend dead','Kill participation','Team damage percentage','Skillshots hit','Skillshots dodged','Solo kills','Turret plates taken']
    X = ['Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp','Damage','Shielding','Healing','TotalDamageTaken','Vision Score','Game Time seconds','Total time CCing','Time spend dead','Kill participation','Team damage percentage','Skillshots hit','Skillshots dodged','Solo kills','Turret plates taken']


    
    model = build_logit_model(df, y, X, 0.05)
    print(model.summary())
    


    #app.run()