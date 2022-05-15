from src.flaskApp import app
from flask import render_template
from src.DataScripts.analysis import *
from src.DataScripts.GetData import *
import pandas as pd


user = "Drakuns"
df = pd.read_csv("./TestData_1_cleaned")
df = pd.DataFrame(df)

@app.route("/")
def home():
    return render_template("landingPage.html")

@app.route("/overview")
def graph():
    n = 10

    user = "Drakuns"
    df = pd.read_csv("./TestData_1_cleaned")
    df = pd.DataFrame(df)

    #Top champs by winrate
    top_wr_champs = top_champs_by_wr(df, n, user)
    labels_wr = []
    win_rates = []
    for champs in top_wr_champs:
        labels_wr.append(champs["Name"])
        win_rates.append(champs["Win Rate"])

    #Top champs by played
    labels_top = []
    games = []
    top_played = top_n_occurences(df, "Champion",user, n = n, to_dict=True)
    for champs in top_played:
        labels_top.append(champs["Name"])
        games.append(champs["Games"])

    #Logistic regression results
    df = df[df["SummonerName"] == user]
    y = "WinLoss"
    X = ['Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp','Damage','Shielding','Healing','TotalDamageTaken','Vision Score','Game Time seconds','Total time CCing','Time spend dead','Kill participation','Team damage percentage','Skillshots hit','Skillshots dodged','Solo kills','Turret plates taken']
    model = build_logit_model(df, y, X, 0.05)
    coefs = get_model_coefs(model)

    #wins, losses, win-rate
    results = user_win_loss_wr(df, user)
    wins = results[0]
    losses = results[1]
    wr = results[2]
    total_games = wins + losses

    rank = get_rank(user, region)

    


    return render_template("overview.html", labels_wr = labels_wr, win_rates = win_rates, labels_top = labels_top, \
        games = games,n = n, coefs = coefs, wins = wins, losses = losses, wr = wr, total_games = total_games, user = user, rank = rank)

