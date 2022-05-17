from graphviz import render
from matplotlib.pyplot import table
from src.flaskApp import app
from flask import redirect, render_template, url_for, request
from src.DataScripts.CleanData import *
from src.DataScripts.analysis import *
from src.DataScripts.GetData import *
import pandas as pd
from src.flaskApp.forms import UserNameForm, LoadForm
import time


user = ""
current_user = ""
region = ""
wins = 0
losses = 0
wr = 0
total_games = 0
rank = ""
n = 0

data = ""


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

    global wins
    global losses 
    global wr 
    global total_games 
    global rank
    global n   
    global data
    global current_user

    
    no_games = 500
    n = 10
    
    if user != "test":
        current_user = user
        df = get_match_details(user, region, no_games)
        df = col_to_string(df, "WinLoss")
        df["WinLoss"] = df["WinLoss"].map(encode_true_false)
        df = impute_mode_lane(df)
        df = encode_categorical(df, "Lane")
        df.to_csv("./newdata")
        data = "newdata"
    
    else:
        current_user = "Incursio"
        region = "OC1"
        df = pd.read_csv("./TestData_Cleaned")
        df = pd.DataFrame(df)
        data = "TestData_Cleaned"
    
    #wins, losses, win-rate
    results = user_win_loss_wr(df, current_user)
    wins = results[0]
    losses = results[1]
    wr = results[2]
    total_games = wins + losses
    #Rank
    rank = get_rank(current_user, region)

    
    
    return redirect(url_for('overview'))

    
    

    



@app.route("/overview")
def overview():
    
    global current_user
    global region 
    global wins
    global losses 
    global wr 
    global total_games 
    global rank
    global n   
    global data

 
    n = int(n)
    data_loc = f"./{data}"
    df = pd.read_csv(data_loc)
    df = pd.DataFrame(df)
    
    #Top champs by winrate
    top_wr_champs = top_champs_by_wr(df, n, current_user)
    labels_wr = []
    win_rates = []
    for champs in top_wr_champs:
        labels_wr.append(champs["Name"])
        win_rates.append(champs["Win Rate"])

    #Top champs by played
    labels_top = []
    games = []
    top_played = top_n_occurences(df, "Champion",current_user, n = n, to_dict=True)
    for champs in top_played:
        labels_top.append(champs["Name"])
        games.append(champs["Games"])

    
    #Logistic regression results
    
    df = df[df["SummonerName"] == current_user]
    y = "WinLoss"
    X = ['Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp','Damage','Shielding','Healing','TotalDamageTaken','Vision Score','Game Time seconds','Total time CCing','Time spend dead','Kill participation','Team damage percentage','Skillshots hit','Skillshots dodged','Solo kills','Turret plates taken']

    model = build_logit_model(df, y, X, 0.05)
    coefs = get_model_coefs(model)

    return render_template("overview.html", labels_wr = labels_wr, win_rates = win_rates, labels_top = labels_top, \
        games = games,n = n,  wins = wins, losses = losses, wr = wr, total_games = total_games, user = current_user, rank = rank, coefs = coefs)

@app.route("/stats")
def stats():
    
    data_loc = f"./{data}"
    df = pd.read_csv(data_loc)
    df = pd.DataFrame(df)
    stats_variable_list = ['Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp',\
        'Damage','Shielding','Healing','TotalDamageTaken','WardsPlace','WardsKilled','Vision Score','Game Time seconds',\
            'Total time CCing','Time spent dead','Kill participation','Team damage percentage','Skillshots hit',\
                'Skillshots dodged','Solo kills','Turret plates taken']

    top = get_user_top_stats(df, current_user, stats_variable_list)
    bottom = get_user_bottom_stats(df, current_user, stats_variable_list)
    
    #Top stats

    top_vars = top.index.to_list()
    top_user = top["User"].to_list()
    top_other = top["Non-user"].to_list()

    top_vars_1 = top_vars[0]
    top_user_1 = top_user[0]
    top_other_1 = top_other[0]

    top_vars_2 = top_vars[1]
    top_user_2 = top_user[1]
    top_other_2 = top_other[1]
    
    top_vars_3 = top_vars[2]
    top_user_3 = top_user[2]
    top_other_3 = top_other[2]
    
    top_vars_4 = top_vars[3]
    top_user_4 = top_user[3]
    top_other_4 = top_other[3]
    
    top_vars_5 = top_vars[4]
    top_user_5 = top_user[4]
    top_other_5 = top_other[4]

    #Bottom stats
    bottom_vars = bottom.index.to_list()
    bottom_user = bottom["User"].to_list()
    bottom_other = bottom["Non-user"].to_list()

    bottom_vars_1 = bottom_vars[0]
    bottom_user_1 = bottom_user[0]
    bottom_other_1 = bottom_other[0]

    bottom_vars_2 = bottom_vars[1]
    bottom_user_2 = bottom_user[1]
    bottom_other_2 = bottom_other[1]
    
    bottom_vars_3 = bottom_vars[2]
    bottom_user_3 = bottom_user[2]
    bottom_other_3 = bottom_other[2]
    
    bottom_vars_4 = bottom_vars[3]
    bottom_user_4 = bottom_user[3]
    bottom_other_4 = bottom_other[3]
    
    bottom_vars_5 = bottom_vars[4]
    bottom_user_5 = bottom_user[4]
    bottom_other_5 = bottom_other[4]


    
    
 
    return render_template("stats2.html",  user = current_user, wins = wins, losses = losses, wr = wr, \
        total_games = total_games, rank = rank,

        top_vars_1 = top_vars_1, top_user_1 = top_user_1, top_other_1 = top_other_1,\
        top_vars_2 = top_vars_2, top_user_2 = top_user_2, top_other_2 = top_other_2,
        top_vars_3 = top_vars_3, top_user_3 = top_user_3, top_other_3 = top_other_3,   
        top_vars_4 = top_vars_4, top_user_4 = top_user_4, top_other_4 = top_other_4,
        top_vars_5 = top_vars_5, top_user_5 = top_user_5, top_other_5 = top_other_5,
        
        bottom_vars_1 = bottom_vars_1, bottom_user_1 = bottom_user_1, bottom_other_1 = bottom_other_1,\
        bottom_vars_2 = bottom_vars_2, bottom_user_2 = bottom_user_2, bottom_other_2 = bottom_other_2,
        bottom_vars_3 = bottom_vars_3, bottom_user_3 = bottom_user_3, bottom_other_3 = bottom_other_3,   
        bottom_vars_4 = bottom_vars_4, bottom_user_4 = bottom_user_4, bottom_other_4 = bottom_other_4,
        bottom_vars_5 = bottom_vars_5, bottom_user_5 = bottom_user_5, bottom_other_5 = bottom_other_5
        
        )
