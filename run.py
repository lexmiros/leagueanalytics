from re import U

from flask import render_template
from src.GetData import get_match_details
from src.analysis import *
import pandas as pd
from src import app

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

    
    @app.route("/")
    def home():
        n = 10
        top_wr_champs = top_champs_by_wr(df, n)
        labels = []
        win_rates = []
        for champs in top_wr_champs:
            labels.append(champs["Name"])
            win_rates.append(champs["Win Rate"])

        return render_template("graph.html", labels = labels, win_rates = win_rates, n = n)
    
    app.run()