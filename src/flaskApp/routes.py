from src.flaskApp import app
from flask import render_template
from src.DataScripts.analysis import *
import pandas as pd

df = pd.read_csv("./TestData_cleaned")
df = pd.DataFrame(df)

@app.route("/")
def home():
    
    return render_template("landingPage.html")

@app.route("/overview")
def graph():
    n = 10

    #Top champs by winrate
    top_wr_champs = top_champs_by_wr(df, n)
    labels_wr = []
    win_rates = []
    for champs in top_wr_champs:
        labels_wr.append(champs["Name"])
        win_rates.append(champs["Win Rate"])

    #Top champs by played
    labels_top = []
    games = []
    top_played = top_n_occurences(df, "Champion", n = n, to_dict=True)
    for champs in top_played:
        labels_top.append(champs["Name"])
        games.append(champs["Games"])



    return render_template("overview.html", labels_wr = labels_wr, win_rates = win_rates, labels_top = labels_top, \
        games = games,n = n)

