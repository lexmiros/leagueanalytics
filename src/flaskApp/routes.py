from graphviz import render
from src.flaskApp import app
from flask import redirect, render_template, url_for, request
from src.DataScripts.CleanData import *
from src.DataScripts.analysis import *
from src.DataScripts.GetData import *
import pandas as pd
from src.flaskApp.forms import UserNameForm, LoadForm
import time
user = ""
region = ""
wins = 0
losses = 0
wr = 0
total_games = 0
rank = ""
n = 0
df = ""


@app.route("/", methods = ["POST", "GET"])
def home():
    form = UserNameForm()

    global user
    global region 

    if form.validate_on_submit():
        #If the user enters a name get data and save in .csv
        if form.user.data != "":
            user = form.user.data
            region = form.region.data
            user = user.capitalize()

            
            
        
        #If user doesnt enter a name, use test data
        else:
            user = "test"
            region = "OC1"

        return redirect(url_for('loading', user = user, region = region))
    

    return render_template("landingPage.html", form = form)

@app.route("/loading/<user>/<region>", methods=["POST","GET"])
def loading(user, region):

    form = LoadForm()

    global wins
    global losses 
    global wr 
    global total_games 
    global rank
    global n   
    global df
    
    no_games = 500
    n = 10


    
    if user != "test":
 
        df = get_match_details(user, region, no_games)
        df = col_to_string(df, "WinLoss")
        df["WinLoss"] = df["WinLoss"].map(encode_true_false)
        df = impute_mode_lane(df)
        df = encode_categorical(df, "Lane")
        df.to_csv("./newdata")
        data = "newdata"
    
    else:
        user = "Drakuns"
        region = "OC1"
        df = pd.read_csv("./TestData_Cleaned")
        df = pd.DataFrame(df)
        data = "TestData_Cleaned"
    
    #wins, losses, win-rate
    results = user_win_loss_wr(df, user)
    wins = results[0]
    losses = results[1]
    wr = results[2]
    total_games = wins + losses
    #Rank
    rank = get_rank(user, region)

    
    
    return render_template("loading.html", form = form, user = user, region = region, data = data, wins = wins, losses = losses, wr = wr, total_games = total_games, rank = rank, n = n)

    
    

    



@app.route("/overview/<user>/<region>/<data>/<wins>/<losses>/<wr>/<total_games>/<rank>/<n>")
def overview(user,region,data,wins,losses,wr,total_games,rank,n):
    n = int(n)
    data_loc = f"./{data}"
    df = pd.read_csv(data_loc)
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

    print(top_played)
    #Logistic regression results
    
    df = df[df["SummonerName"] == user]
    y = "WinLoss"
    X = ['Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp','Damage','Shielding','Healing','TotalDamageTaken','Vision Score','Game Time seconds','Total time CCing','Time spend dead','Kill participation','Team damage percentage','Skillshots hit','Skillshots dodged','Solo kills','Turret plates taken']
    
    
    model = build_logit_model(df, y, X, 0.05)
    coefs = get_model_coefs(model)

    return render_template("overview.html", labels_wr = labels_wr, win_rates = win_rates, labels_top = labels_top, \
        games = games,n = n, coefs = coefs, wins = wins, losses = losses, wr = wr, total_games = total_games, user = user, rank = rank)

@app.route("/stats")
def stats():

    return render_template("stats.html",  user = user, wins = wins, losses = losses, wr = wr, total_games = total_games, rank = rank)
