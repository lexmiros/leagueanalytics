from src import pd
from src.flaskApp import app
from flask import redirect, render_template, url_for
from src import filepath
import time

from src.DataScripts.GetData import get_account_id, get_match_details, get_time_series_non_user, get_time_series_user, webpage_transfer
from src.DataScripts.CleanData import top_n_occurences
from src.DataScripts.analysis import  build_logit_model, get_model_coefs, get_user_top_stats, get_user_bottom_stats, get_column_cumulative, get_wr_cumulative, role_losses, role_wins, top_champs_by_wr, win_ratio_str_formatted, get_wr_cumulative, win_ratio_str_formatted, user_win_loss_wr, top_champs_by_wr,  role_wins, role_losses


from src.flaskApp.forms import UserNameForm

#Landing page
@app.route("/", methods = ["POST", "GET"])
def home():
   
    form = UserNameForm()

    if form.validate_on_submit():
        #If the user enters a name get data and save in .csv
        if form.user.data != "":
            user = form.user.data
            region = form.region.data
            user = user.capitalize()
             #Check to see if user exists
            try:
                get_account_id(user, region)
                return redirect(url_for('loading', user = user, region = region))

           
            except:
                error_msg = "Account / Region combination not found!"
                return render_template("landingPage.html", form = form, error_msg = error_msg)

        
        #If user doesnt enter a name, use test data
        else:
            user = "Frommoh"
            region = "OC1"
            test = "True"
            return redirect(url_for('overview', user = user, test = test, region = region))

       
        
    
    return render_template("landingPage.html", form = form)

@app.route("/readme")
def readme():
    """"""

    return render_template("readme.html")

#Loading data function
@app.route("/loading/<user>/<region>", methods=["POST","GET"])
def loading(user, region):
    
    user = user
    region = region
    start_index = 0
    test = False
    
    try:
        next_batch = get_match_details(user, region, start_index, final_set=False)
        print("Batch 1")
        return redirect(url_for('loading2', user = user,  region = region, next_batch = next_batch))
    except:
        form = UserNameForm()
        error_msg = "Riot Sever currently 'Busy' (error 503). Please search again in a few minutes "
        return redirect(url_for("home", form = form, error_msg = error_msg))
        
    

   

#Loading data function
@app.route("/loading2/<user>/<region>/<next_batch>", methods=["POST","GET"])
def loading2(user, region, next_batch):
    
    user = user
    region = region
    start_index = 200 
    test = False

    try:   
        next_batch = get_match_details(user, region, start_index, final_set=False)
        print("Batch 2")
        if next_batch == "True":
            return redirect(url_for('loading3', user = user, region = region, next_batch = next_batch))
        else:
            return redirect(url_for('loading_timeseries_user', user = user, test = test, region = region))
    except:
        time.sleep(30)
        print('batch 2 skipped')
        return redirect(url_for('loading3', user = user, region = region, next_batch = next_batch))
        #return redirect(url_for('loading2', user = user,  region = region, next_batch = next_batch))

    

#Loading data function
@app.route("/loading3/<user>/<region>/<next_batch>", methods=["POST","GET"])
def loading3(user, region, next_batch):
    
    user = user
    region = region
    start_index = 400 
    test = False
    print(next_batch)

   
        
    try:   
        next_batch = get_match_details(user, region, start_index, final_set=False)
        print("Batch 3")
        if next_batch == "True":
            return redirect(url_for('loading4', user = user, region = region, next_batch = next_batch))
        else:
            return redirect(url_for('loading_timeseries_user', user = user, test = test, region = region))
    except:
        time.sleep(30)
        print('batch 3 skipped')
        return redirect(url_for('loading4', user = user, region = region, next_batch = next_batch))
        #return redirect(url_for('loading3', user = user, region = region, next_batch = next_batch))
    

    

#Loading data function
@app.route("/loading4/<user>/<region>/<next_batch>", methods=["POST","GET"])
def loading4(user, region, next_batch):
    
    user = user
    region = region
    start_index = 600 
    test = False
      
    try:   
        next_batch = get_match_details(user, region, start_index, final_set=False)
        print('batch 4')
        if next_batch == "True":
            return redirect(url_for('loading5', user = user, region = region, next_batch = next_batch))
        else:
            return redirect(url_for('loading_timeseries_user', user = user, test = test, region = region))
    except:
        time.sleep(30)
        print('batch 4 skipped')
        return redirect(url_for('loading5', user = user, region = region, next_batch = next_batch))
        #return redirect(url_for('loading4', user = user, region = region, next_batch = next_batch))
    
    


#FINAL
#Loading data function
@app.route("/loading5/<user>/<region>/<next_batch>", methods=["POST","GET"])
def loading5(user, region, next_batch):
    
    user = user
    region = region
    start_index = 800
    test = False 

   
    try:    
        get_match_details(user, region, start_index, final_set=True)
    
        print("Batch 5")
    except:
        return redirect(url_for('loading5', user = user, region = region, next_batch = next_batch))

    return redirect(url_for('loading_timeseries_user', user = user, test = test, region = region))


@app.route("/loading_timeseries_user/<user>/<region>/<test>")
def loading_timeseries_user(user, region, test):

    #Checks to see if time series data needs to be downloaded
    try:
        if test != "True":
            #Downloads and saves time-series data
            dfs_user = get_time_series_user(user, region)
            print("User Data loaded")

            data_cs = dfs_user[0]
            print("User cs loaded")
            data_exp = dfs_user[1]
            print("User exp loaded")
            data_gold = dfs_user[2]
            print("User gold loaded")
            data_dmg = dfs_user[3]
            print("User dmg loaded")

            data_cs.to_csv(f"{filepath}{user}_cs.csv")
            print("User cs to csv loaded")
            data_exp.to_csv(f"{filepath}{user}_exp.csv")
            print("User exp to csv loaded")
            data_gold.to_csv(f"{filepath}{user}_gold.csv")
            print("User gold to csv loaded")
            data_dmg.to_csv(f"{filepath}{user}_dmg.csv")
            print("User dmg to csv loaded")

            return redirect(url_for('loading_timeseries_non_user', user = user, test = test, region = region))
    except:
        return redirect(url_for('loading_timeseries_user', user = user, test = test, region = region))

    


@app.route("/loading_timeseries_non_user/<user>/<region>/<test>")
def loading_timeseries_non_user(user, region, test):

    try:
        dfs_non_user = get_time_series_non_user(user, region)
        print("User NON Data loaded")

        data_non_cs = dfs_non_user[0]
        print("NON User cs loaded")
        data_non_exp = dfs_non_user[1]
        print("NON User exp loaded")
        data_non_gold = dfs_non_user[2]
        print("NON User gold loaded")
        data_non_dmg = dfs_non_user[3]
        print("NON User dmg loaded")

        data_non_cs.to_csv(f"{filepath}_non_{user}_cs.csv")
        print("NON User cs to csv loaded")
        data_non_exp.to_csv(f"{filepath}_non_{user}_exp.csv")
        print("NON User exp to csv loaded")
        data_non_gold.to_csv(f"{filepath}_non_{user}_gold.csv")
        print("NON User gold to csv loaded")
        data_non_dmg.to_csv(f"{filepath}_non_{user}_dmg.csv")
        print("NON User dmg to csv loaded")

        return redirect(url_for('overview', user = user, test = test, region = region))
    except:
        return redirect(url_for('loading_timeseries_non_user', user = user, test = test, region = region))

    
@app.route("/overview/<user>/<region>/<test>")
def overview(user, region, test):
    
    user = user
    region = region
    test = test

    #Set up passed in info from webpage
    info = webpage_transfer(user, region, test)

    df = info[0]
    rank = info[1]
    wins = info[2]
    losses = info[3]
    wr = info[4]
    total_games = info[5]
    
    
    #Top champs by winrate
    top_wr_champs = top_champs_by_wr(df, 10, user)
    labels_wr = []
    win_rates = []
    for champs in top_wr_champs:
        labels_wr.append(champs["Name"])
        win_rates.append(champs["Win Rate"])

    #Top champs by played
    labels_top = []
    games = []
    top_played = top_n_occurences(df, "Champion",user, n = 10, to_dict=True)
    for champs in top_played:
        labels_top.append(champs["Name"])
        games.append(champs["Games"])

    
    #Logistic regression results
    #subset df on user v non-user
    df_user = df[df["SummonerName"] == user]
    df_non_user = df[df["SummonerName"] != user]
    
    #model_user variables
    y = "WinLoss"
    X = ['Q casts','W casts','E casts','R casts','ChampLevel','CS',\
        'Damage','Shielding','Healing','Total Damage Taken','Wards Placed','Wards Killed','Game Time seconds',\
            'Crowd Control','Time spent dead','Skillshots hit',\
                'Skillshots dodged','Solo kills','Turret plates taken']

    #build models and get coefficients
    #user
    model_user = build_logit_model(df_user, y, X, 0.1)
    coefs_user = get_model_coefs(model_user)

    #Non-user
    model_non_user = build_logit_model(df_non_user, y, X, 0.1)
    coefs_non_user = get_model_coefs(model_non_user)

    #Model names & values for user
    model_names_user = coefs_user[0]
    model_values_user = coefs_user[1]
    model_names_neg_user = coefs_user[2]
    model_values_neg_user = coefs_user[3]

    #Model names & values for NON user
    model_names_non_user = coefs_non_user[0]
    model_values_non_user = coefs_non_user[1]
    model_names_neg_non_user = coefs_non_user[2]
    model_values_neg_non_user = coefs_non_user[3]
    
    pos_max = max(model_values_user + model_values_non_user)
    pos_min = min(model_values_user + model_values_non_user)

    neg_max = max(model_values_neg_user + model_values_neg_non_user)
    neg_min = min(model_values_neg_user + model_values_neg_non_user)


    #Check that the model_user found at least 3 variables
    show_radar_pos = True
    show_radar_neg = True
    if len(model_names_user) < 3:
        show_radar_pos = False
    if len(model_names_neg_user) < 3:
        show_radar_pos = False



    return render_template("overview.html", 
        labels_wr = labels_wr, win_rates = win_rates, labels_top = labels_top,

        games = games, wins = wins, losses = losses, wr = wr, total_games = total_games, user = user, rank = rank,

        model_values_user = model_values_user, model_names_user = model_names_user, model_names_neg_user = model_names_neg_user, 
        model_values_neg_user = model_values_neg_user, pos_max = pos_max, pos_min = pos_min, neg_max = neg_max, 
        neg_min = neg_min,

        model_values_non_user = model_values_non_user, model_names_non_user = model_names_non_user, model_names_neg_non_user = model_names_neg_non_user, 
        model_values_neg_non_user = model_values_neg_non_user,

        show_radar_neg = show_radar_neg, show_radar_pos = show_radar_pos, test = test, region = region)

@app.route("/stats/<user>/<region>/<test>")
def stats(user, region, test):

    #Set up passed in info from webpage
    user = user
    region = region
    test = test

    info = webpage_transfer(user, region, test)

    df = info[0]
    rank = info[1]
    wins = info[2]
    losses = info[3]
    wr = info[4]
    total_games = info[5]
    

    stats_variable_list = ['Q casts','W casts','E casts','R casts','ChampLevel','CS','Kills','Deaths','Assists','Exp',\
        'Damage','Shielding','Healing','Total Damage Taken','Wards Placed','Wards Killed','Vision Score','Game Time seconds',\
            'Crowd Control','Time spent dead','Kill participation','Team damage percentage','Skillshots hit',\
                'Skillshots dodged','Solo kills','Turret plates taken']

    top = get_user_top_stats(df, user, stats_variable_list)
    bottom = get_user_bottom_stats(df, user, stats_variable_list)
    
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
        user = user, region = region, test = test, wins = wins, losses = losses, wr = wr, total_games = total_games, rank = rank,

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

@app.route("/roles/<user>/<region>/<test>")
def roles(user, region, test):
    
    #Set up passed in info from webpage
    user = user
    region = region
    test = test

    info = webpage_transfer(user, region, test)

    df = info[0]
    rank = info[1]
    wins = info[2]
    losses = info[3]
    wr = info[4]
    total_games = info[5]

    #Df for user only
    df_user = df[df["SummonerName"] == user]

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

    top_wr_champs = top_champs_by_wr(df_bottom, n, user)
    bottom_labels = []
    bottom_rates = []
    for champs in top_wr_champs:
        bottom_labels.append(champs["Name"])
        bottom_rates.append(champs["Win Rate"])
    
    #Top champs by winrate jungle
    
    top_wr_champs = top_champs_by_wr(df_jungle, n, user)
    jungle_labels = []
    jungle_rates = []
    for champs in top_wr_champs:
        jungle_labels.append(champs["Name"])
        jungle_rates.append(champs["Win Rate"])

    #Top champs by winrate middle
    
    top_wr_champs = top_champs_by_wr(df_middle, n, user)
    middle_labels = []
    middle_rates = []
    for champs in top_wr_champs:
        middle_labels.append(champs["Name"])
        middle_rates.append(champs["Win Rate"])

    #Top champs by winrate top
    
    top_wr_champs = top_champs_by_wr(df_top, n, user)
    top_labels = []
    top_rates = []
    for champs in top_wr_champs:
        top_labels.append(champs["Name"])
        top_rates.append(champs["Win Rate"])

    #Top champs by winrate support
    
    top_wr_champs = top_champs_by_wr(df_support, n, user)
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

        user = user, region = region, test = test, wins = wins, losses = losses, wr = wr, total_games = total_games, rank = rank,
        
        bottom_wr = bottom_wr, jungle_wr = jungle_wr, middle_wr = middle_wr , top_wr = top_wr ,support_wr = support_wr ,
        
        bottom_wins = bottom_wins,jungle_wins = jungle_wins ,middle_wins = middle_wins ,top_wins = top_wins ,support_wins = support_wins,
        
        bottom_losses = bottom_losses ,jungle_losses = jungle_losses ,middle_losses = middle_losses ,top_losses = top_losses ,support_losses = support_losses,                    
        
        labels_1 = labels_1, data_1 = data_1, labels_2 = labels_2, data_2 = data_2, labels_3 = labels_3, data_3 = data_3,

        time_top = time_top, time_jungle = time_jungle, time_middle = time_middle, time_bottom = time_bottom, time_support = time_support,

        cum_wr_top = cum_wr_top, cum_wr_jungle = cum_wr_jungle, cum_wr_middle = cum_wr_middle, cum_wr_bottom = cum_wr_bottom, cum_wr_support = cum_wr_support,

        time_overall = time_overall, cum_wr_overall = cum_wr_overall
        )

@app.route("/timeseries/<user>/<region>/<test>")
def timeseries(user, region, test):
    """"""
    #Set up passed in info from webpage
    user = user
    region = region
    test = test

    info = webpage_transfer(user, region, test)

    df = info[0]
    rank = info[1]
    wins = info[2]
    losses = info[3]
    wr = info[4]
    total_games = info[5]

    #Check if using test data
    if test == 'True':
        #Read in data
        data_cs = pd.read_csv(f"{filepath}TestData_cs.csv")
        data_cs = pd.DataFrame(data_cs)

        data_dmg = pd.read_csv(f"{filepath}TestData_dmg.csv")
        data_dmg = pd.DataFrame(data_dmg)

        data_exp = pd.read_csv(f"{filepath}TestData_exp.csv")
        data_exp = pd.DataFrame(data_exp)

        data_gold = pd.read_csv(f"{filepath}TestData_gold.csv")
        data_gold = pd.DataFrame(data_gold)

        data_non_cs = pd.read_csv(f"{filepath}TestData_non_cs.csv")
        data_non_cs = pd.DataFrame(data_non_cs)

        data_non_dmg = pd.read_csv(f"{filepath}TestData_non_dmg.csv")
        data_non_dmg = pd.DataFrame(data_non_dmg)

        data_non_exp = pd.read_csv(f"{filepath}TestData_non_exp.csv")
        data_non_exp = pd.DataFrame(data_non_exp)

        data_non_gold = pd.read_csv(f"{filepath}TestData_non_gold.csv")
        data_non_gold = pd.DataFrame(data_non_gold)
    else:
        data_cs = pd.read_csv(f"{filepath}{user}_cs.csv")
        data_exp = pd.read_csv(f"{filepath}{user}_exp.csv")
        data_gold = pd.read_csv(f"{filepath}{user}_gold.csv")
        data_dmg = pd.read_csv(f"{filepath}{user}_dmg.csv")

        data_non_cs = pd.read_csv(f"{filepath}_non_{user}_cs.csv")
        data_non_exp = pd.read_csv(f"{filepath}_non_{user}_exp.csv")
        data_non_gold = pd.read_csv(f"{filepath}_non_{user}_gold.csv")
        data_non_dmg = pd.read_csv(f"{filepath}_non_{user}_dmg.csv")


    #Subet data 3 due to limited activity before 3mins, 35 due to low games running past 35
    data_cs = data_cs.iloc[3:36,]
    data_dmg = data_dmg.iloc[3:36,]
    data_exp = data_exp.iloc[3:36,]
    data_gold = data_gold.iloc[3:36,]

    data_non_cs = data_non_cs.iloc[3:36,]
    data_non_dmg = data_non_dmg.iloc[3:36,]
    data_non_exp = data_non_exp.iloc[3:36,]
    data_non_gold = data_non_gold.iloc[3:36,]

    data_range = list(range(3,36))




    #Average each row for the dfs and turn to list
    avg_cs = data_cs.mean(axis=1, skipna=True).to_list()
    avg_dmg = data_dmg.mean(axis=1, skipna=True).to_list()
    avg_exp = data_exp.mean(axis=1, skipna=True).to_list()
    avg_gold = data_gold.mean(axis=1, skipna=True).to_list()

    avg_non_cs = data_non_cs.mean(axis=1, skipna=True).to_list()
    avg_non_dmg = data_non_dmg.mean(axis=1, skipna=True).to_list()
    avg_non_exp = data_non_exp.mean(axis=1, skipna=True).to_list()
    avg_non_gold = data_non_gold.mean(axis=1, skipna=True).to_list()
        

    return render_template('timeSeries.html', 
        user = user, region = region, test = test, wins = wins, losses = losses, wr = wr, total_games = total_games, rank = rank,

        avg_cs = avg_cs, avg_dmg = avg_dmg, avg_exp = avg_exp, avg_gold = avg_gold, data_range = data_range,
        
        avg_non_cs = avg_non_cs, avg_non_dmg = avg_non_dmg, avg_non_exp = avg_non_exp, avg_non_gold = avg_non_gold
        )

@app.route("/about/<user>/<region>/<test>")
def about(user, region, test):
    """"""
    
    
    return render_template("about.html", user = user, region = region, test = test)


