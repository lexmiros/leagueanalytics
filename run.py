from enum import unique
from re import U


from flask import render_template
from numpy import average
from src.DataScripts.analysis import *
from src.DataScripts.GetData import *
from src.DataScripts.CleanData import *
import pandas as pd
from src.flaskApp import app
from src.flaskApp import routes

if __name__ == "__main__":
    app.run()
    #user = "Incursio"
    #region = "OC1"

    #df = pd.read_csv('./TestData_Cleaned')
    #df = pd.DataFrame(df)
    #stats_variable_list = ['Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp','Damage','Shielding','Healing','TotalDamageTaken','WardsPlace','WardsKilled','Vision Score','Game Time seconds','Total time CCing','Time spent dead','Kill participation','Team damage percentage','Skillshots hit','Skillshots dodged','Solo kills','Turret plates taken']
    #x = get_user_stats(df, user, stats_variable_list)
 





    """
    
    df = get_match_details(user, region, 5000)
    df = col_to_string(df, "WinLoss")
    df["WinLoss"] = df["WinLoss"].map(encode_true_false)
    df = impute_mode_lane(df)
    df = encode_categorical(df, "Lane")
    df.to_csv("./TestData_Cleaned")
    """
 