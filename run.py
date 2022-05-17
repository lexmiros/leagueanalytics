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
    #app.run()
    current_user = "Incursio"
    #region = "OC1"

    df = pd.read_csv("TestData_Cleaned")
    df = pd.DataFrame(df)
    n = 3
    df = df[df["SummonerName"] == current_user]
    
  
    

    """
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

 





    
    df = get_match_details(user, region, 5000)
    df = col_to_string(df, "WinLoss")
    df["WinLoss"] = df["WinLoss"].map(encode_true_false)
    df = impute_mode_lane(df)
    df = encode_categorical(df, "Lane")
    df.to_csv("./TestData_Cleaned")
    """
 