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
    
    top_wr_champs = top_champs_by_wr(df, 10)
    labels = []
    win_rates = []
    for champs in top_wr_champs:
        labels.append(champs["Name"])
        win_rates.append(champs["Win Rate"])

    
    
    app.run()