from src.flaskApp import app
from flask import redirect, render_template, url_for
from src.DataScripts.analysis import *
from src.DataScripts.GetData import *
import pandas as pd
from src.flaskApp.forms import UserNameForm

#Globals
user = "Drakuns"
df = pd.read_csv("./TestData_1_cleaned")
df = pd.DataFrame(df)
n = 10

#wins, losses, win-rate
results = user_win_loss_wr(df, user)
wins = results[0]
losses = results[1]
wr = results[2]
total_games = wins + losses

#Rank
rank = get_rank(user, region)


@app.route("/", methods = ["POST", "GET"])
def home():
    form = UserNameForm()
    if form.validate_on_submit():
        
        return(redirect(url_for("overview")))

    return render_template("landingPage.html", form = form)

@app.route("/overview")
def overview():
    global df
    global n
    global user
    global wins
    global losses
    global wr
    global total_games

    
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

   


    return render_template("overview.html", labels_wr = labels_wr, win_rates = win_rates, labels_top = labels_top, \
        games = games,n = n, coefs = coefs, wins = wins, losses = losses, wr = wr, total_games = total_games, user = user, rank = rank)

