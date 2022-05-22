
from src.flaskApp import app, routes
from src.DataScripts.analysis import *
from src.DataScripts.CleanData import *
from src.DataScripts.GetData import *


if __name__ == "__main__":

    app.run() 

    """
    user = "Ausfreak"
    print(user)
    region = "OC1"
    test = False

    #Set up passed in info from webpage
    info = webpage_transfer(user, region, test)


    df = info[0]
    df = pd.read_csv("./newdataAusfreak.csv")
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
    print(df_user)
    
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
    
    print(model_names)
    print(model_names_neg)
    
    current_user = "Ausfreak"
    region = "OC1"
    df = get_match_details(current_user, region, 5000)
    df = col_to_string(df, "WinLoss")
    df["WinLoss"] = df["WinLoss"].map(encode_true_false)
    df = impute_mode_lane(df)
    df = encode_categorical(df, "Lane")
    df.to_csv("./TestData_Cleaned_3")
    """
    



 