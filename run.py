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
    
    """
    current_user = "Proosia"
    region = "NA1"
    df = pd.read_csv("TestData_Cleaned_2")
    df = pd.DataFrame(df)
  
    df_user = df[df["SummonerName"] == current_user]

    df_mid = df_user[df_user["UTILITY"] == 1]

    x = get_wr_cumulative(df_mid)
    y = get_column_cumulative(df_mid, "Game Time seconds")

    y = [val/3600 for val in y]
    y = [round(val,2) for val in y]
    
    #print(x)
    #print(y)

    time_overall = get_column_cumulative(df_user, "Game Time seconds")
    time_overall = [val/3600 for val in time_overall]
    time_overall = [round(val,4) for val in time_overall]
    print(time_overall)
    
    current_user = "Frommoh"
    region = "OC1"
    df = pd.read_csv("newdata")
    df = pd.DataFrame(df)
  
    df_user = df[df["SummonerName"] == current_user]

    y = "WinLoss"
    X = ['Q casts','W casts','E casts','R casts','ChampLevel','CS',\
        'Damage','Shielding','Healing','TotalDamageTaken','WardsPlace','WardsKilled','Game Time seconds',\
            'Total time CCing','Time spent dead','Skillshots hit',\
                'Skillshots dodged','Solo kills','Turret plates taken']

    model = build_logit_model(df_user, y, X, 0.05)
    coefs = get_model_coefs(model)
    model_names = coefs[0]
    model_values = coefs[1]
    model_names_neg = coefs[2]
    model_values_neg = coefs[3]

    print(model_names)
    print(model_names_neg)

    
    current_user = "Proosia"
    region = "NA1"
    df = get_match_details(current_user, region, 5000)
    df = col_to_string(df, "WinLoss")
    df["WinLoss"] = df["WinLoss"].map(encode_true_false)
    df = impute_mode_lane(df)
    df = encode_categorical(df, "Lane")
    df.to_csv("./TestData_Cleaned_2")
    
 

    
    


    

 

    df = pd.read_csv("TestData_Cleaned2")
    df = pd.DataFrame(df)
  
    df_user = df[df["SummonerName"] == current_user]

    y = "WinLoss"
    X = ['Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp','Damage','Shielding','Healing','TotalDamageTaken','Vision Score','Game Time seconds','Total time CCing','Time spend dead','Kill participation','Team damage percentage','Skillshots hit','Skillshots dodged','Solo kills','Turret plates taken']

    model = build_logit_model(df_user, y, X, 0.05)
    print(model.summary())
    coefs = get_model_coefs(model)
    #print(coefs[0])
    #print(coefs[1])
     #Number of champs to get for each role
    n = 3

    #Top champs by winrate bottom
    df_bottom = df_user[df_user["TOP"] == 1]

    top_wr_champs = top_champs_by_wr(df_bottom, n, current_user)
    bottom_labels = []
    bottom_rates = []
    for champs in top_wr_champs:
        bottom_labels.append(champs["Name"])
        bottom_rates.append(champs["Win Rate"])

    print(bottom_rates)
    print(bottom_labels)

 





    

    """
 