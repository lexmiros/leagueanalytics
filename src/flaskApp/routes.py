from src import pd
from src.flaskApp import app
from flask import redirect, render_template, url_for

from src.DataScripts.GetData import get_account_id, get_match_details, get_rank
from src.DataScripts.CleanData import encode_true_false, col_to_string, encode_categorical, top_n_occurences, impute_mode_lane
from src.DataScripts.analysis import  build_logit_model, get_model_coefs, get_user_top_stats, get_user_bottom_stats, get_column_cumulative, get_wr_cumulative, role_losses, role_wins, top_champs_by_wr, user_win_loss_wr, win_ratio_str_formatted, get_wr_cumulative, win_ratio_str_formatted, user_win_loss_wr, top_champs_by_wr,  role_wins, role_losses


from src.flaskApp.forms import UserNameForm


#Global variables 
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

#Landing page
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

            #Check to see if user exists
            try:
                get_account_id(user, region)
            except:
                error_msg = "Account / Region combination not found!"
                return render_template("landingPage.html", form = form, error_msg = error_msg)

        
        #If user doesnt enter a name, use test data
        else:
            user = "test"
            region = "OC1"

        return redirect(url_for('loading', user = user, region = region))
    
    return render_template("landingPage.html", form = form)

#Loading data function
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

    
    no_games = 2000
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
        current_user = "Frommoh"
        region = "OC1"
        df = pd.read_csv("./TestData_Cleaned_2")
        df = pd.DataFrame(df)
        data = "TestData_Cleaned_2"
    
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
    
    #subset df on user v non-user
    df_user = df[df["SummonerName"] == current_user]
    df_other = df[df["SummonerName"] != current_user]

    #model variables
    y = "WinLoss"
    X = ['Q casts','W casts','E casts','R casts','ChampLevel','CS',\
        'Damage','Shielding','Healing','Total Damage Taken','Wards Placed','Wards Killed','Game Time seconds',\
            'Crowd Control','Time spent dead','Skillshots hit',\
                'Skillshots dodged','Solo kills','Turret plates taken']

    #build models and get coefficients
    #user
    model = build_logit_model(df_user, y, X, 0.1)
    coefs = get_model_coefs(model)

    model_names = coefs[0]
    model_values = coefs[1]
    model_names_neg = coefs[2]
    model_values_neg = coefs[3]
    
    pos_max = max(model_values)
    pos_min = min(model_values)

    neg_max = max(model_values_neg)
    neg_min = min(model_values_neg)

    #Check that the model found at least 3 variables
    show_radar_pos = True
    show_radar_neg = True
    if len(model_names) < 3:
        show_radar_pos = False
    if len(model_names_neg) < 3:
        show_radar_pos = False



    return render_template("overview.html", labels_wr = labels_wr, win_rates = win_rates, labels_top = labels_top, \
        games = games,n = n,  wins = wins, losses = losses, wr = wr, total_games = total_games, user = current_user, rank = rank,
        model_values = model_values, model_names = model_names, model_names_neg = model_names_neg, model_values_neg = model_values_neg,
        pos_max = pos_max, pos_min = pos_min, neg_max = neg_max, neg_min = neg_min,
        show_radar_neg = show_radar_neg, show_radar_pos = show_radar_pos)

@app.route("/stats")
def stats():
    
    data_loc = f"./{data}"
    df = pd.read_csv(data_loc)
    df = pd.DataFrame(df)
    stats_variable_list = ['Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp',\
        'Damage','Shielding','Healing','Total Damage Taken','Wards Placed','Wards Killed','Vision Score','Game Time seconds',\
            'Crowd Control','Time spent dead','Kill participation','Team damage percentage','Skillshots hit',\
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


    return render_template("stats2.html",  
        user = current_user, wins = wins, losses = losses, wr = wr, total_games = total_games, rank = rank,

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

@app.route("/roles")
def roles():
    """
    """
    #Set up dataframe
    data_loc = f"./{data}"
    df = pd.read_csv(data_loc)
    df = pd.DataFrame(df)

    #Df for user only
    df_user = df[df["SummonerName"] == current_user]

    #Dataframes per role
    df_top = df_user[df_user["TOP"] == 1]
    df_jungle = df_user[df_user["JUNGLE"] == 1]
    df_middle = df_user[df_user["MIDDLE"] == 1]
    df_bottom = df_user[df_user["BOTTOM"] == 1]
    df_support = df_user[df_user["UTILITY"] == 1]

    #Role win-rates
    bottom_wr = win_ratio_str_formatted(df_user, "BOTTOM", 1)
    jungle_wr = win_ratio_str_formatted(df_user, "JUNGLE", 1)
    middle_wr = win_ratio_str_formatted(df_user, "MIDDLE", 1)
    top_wr = win_ratio_str_formatted(df_user, "TOP", 1)
    support_wr = win_ratio_str_formatted(df_user, "UTILITY", 1)

    #Total wins per role
    bottom_wins = role_wins(df_user, "BOTTOM")
    jungle_wins = role_wins(df_user, "JUNGLE")
    middle_wins = role_wins(df_user, "MIDDLE")
    top_wins = role_wins(df_user, "TOP")
    support_wins = role_wins(df_user, "UTILITY")

    #Total losses per role
    bottom_losses = role_losses(df_user, "BOTTOM")
    jungle_losses = role_losses(df_user, "JUNGLE")
    middle_losses = role_losses(df_user, "MIDDLE")
    top_losses = role_losses(df_user, "TOP")
    support_losses = role_losses(df_user, "UTILITY")

    #Find the max Y value for stacked bar chart to stop label clipping the legend
    win_max = max(bottom_wins, top_wins, jungle_wins, middle_wins, support_wins) 
    loss_max = max(bottom_losses, top_losses, jungle_losses, middle_losses, support_losses)
    y_max = win_max + loss_max

    #Number of champs to get for each role
    n = 3

    #Top champs by winrate bottom

    top_wr_champs = top_champs_by_wr(df_bottom, n, current_user)
    bottom_labels = []
    bottom_rates = []
    for champs in top_wr_champs:
        bottom_labels.append(champs["Name"])
        bottom_rates.append(champs["Win Rate"])
    
    #Top champs by winrate jungle
    
    top_wr_champs = top_champs_by_wr(df_jungle, n, current_user)
    jungle_labels = []
    jungle_rates = []
    for champs in top_wr_champs:
        jungle_labels.append(champs["Name"])
        jungle_rates.append(champs["Win Rate"])

    #Top champs by winrate middle
    
    top_wr_champs = top_champs_by_wr(df_middle, n, current_user)
    middle_labels = []
    middle_rates = []
    for champs in top_wr_champs:
        middle_labels.append(champs["Name"])
        middle_rates.append(champs["Win Rate"])

    #Top champs by winrate top
    
    top_wr_champs = top_champs_by_wr(df_top, n, current_user)
    top_labels = []
    top_rates = []
    for champs in top_wr_champs:
        top_labels.append(champs["Name"])
        top_rates.append(champs["Win Rate"])

    #Top champs by winrate support
    
    top_wr_champs = top_champs_by_wr(df_support, n, current_user)
    support_labels = []
    support_rates = []
    for champs in top_wr_champs:
        support_labels.append(champs["Name"])
        support_rates.append(champs["Win Rate"])
    
    labels_1 = []
    data_1 = []
    labels_2 = []
    data_2 = []
    labels_3 = []
    data_3 = []

    labels_list = [top_labels, jungle_labels, middle_labels, bottom_labels, support_labels]
    rates_list = [top_rates, jungle_rates, middle_rates, bottom_rates, support_rates]

    #Add first champ to labels, data lists
    for list in labels_list:
        try:
            labels_1.append(list[0])
        except:
            pass
       
    for list in rates_list:
        try:
            data_1.append(list[0])
        except:
            pass
    #Add second champ to labels, data lists
    for list in labels_list:
        try:
            labels_2.append(list[1])
        except:
            pass
    for list in rates_list:
        try:
            data_2.append(list[1])
        except:
            pass
    #Add third champ to labels, data lists
    for list in labels_list:
        try:
            labels_3.append(list[2])
        except:
           pass
    for list in rates_list:
        try:
            data_3.append(list[2])
        except:
            pass
    

    #Get cumulative times
    time_top = get_column_cumulative(df_top, "Game Time seconds")
    time_top = [val/3600 for val in time_top]
    time_top = [round(val,4) for val in time_top]

    time_jungle = get_column_cumulative(df_jungle, "Game Time seconds")
    time_jungle = [val/3600 for val in time_jungle]
    time_jungle = [round(val,4) for val in time_jungle]

    time_middle = get_column_cumulative(df_middle, "Game Time seconds")
    time_middle = [val/3600 for val in time_middle]
    time_middle = [round(val,4) for val in time_middle]

    time_bottom = get_column_cumulative(df_bottom, "Game Time seconds")
    time_bottom = [val/3600 for val in time_bottom]
    time_bottom = [round(val,4) for val in time_bottom]

    time_support = get_column_cumulative(df_support, "Game Time seconds")
    time_support = [val/3600 for val in time_support]
    time_support = [round(val,4) for val in time_support]
    
    time_overall = get_column_cumulative(df_user, "Game Time seconds")
    time_overall = [val/3600 for val in time_overall]
    time_overall = [round(val,4) for val in time_overall]


    #Get cumulative WRs
    cum_wr_top = get_wr_cumulative(df_top)
    cum_wr_jungle = get_wr_cumulative(df_jungle)
    cum_wr_middle = get_wr_cumulative(df_middle)
    cum_wr_bottom = get_wr_cumulative(df_bottom)
    cum_wr_support = get_wr_cumulative(df_support)
    cum_wr_overall = get_wr_cumulative(df_user)

    return render_template("roles.html",
        y_max = y_max, 

        user = current_user, wins = wins, losses = losses, wr = wr, total_games = total_games, rank = rank,
        
        bottom_wr = bottom_wr, jungle_wr = jungle_wr, middle_wr = middle_wr , top_wr = top_wr ,support_wr = support_wr ,
        
        bottom_wins = bottom_wins,jungle_wins = jungle_wins ,middle_wins = middle_wins ,top_wins = top_wins ,support_wins = support_wins,
        
        bottom_losses = bottom_losses ,jungle_losses = jungle_losses ,middle_losses = middle_losses ,top_losses = top_losses ,support_losses = support_losses,                    
        
        labels_1 = labels_1, data_1 = data_1, labels_2 = labels_2, data_2 = data_2, labels_3 = labels_3, data_3 = data_3,

        time_top = time_top, time_jungle = time_jungle, time_middle = time_middle, time_bottom = time_bottom, time_support = time_support,

        cum_wr_top = cum_wr_top, cum_wr_jungle = cum_wr_jungle, cum_wr_middle = cum_wr_middle, cum_wr_bottom = cum_wr_bottom, cum_wr_support = cum_wr_support,

        time_overall = time_overall, cum_wr_overall = cum_wr_overall
        )

