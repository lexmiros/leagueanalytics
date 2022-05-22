from enum import unique
from re import U


from flask import render_template
from numpy import average
from src.DataScripts.analysis import *
from src.DataScripts.GetData import *
from src.DataScripts.CleanData import *
import pandas as pd
from src.flaskApp import app
from src.flaskApp import routes

if __name__ == "__main__":

    #app.run()

    df = pd.read_csv("./TestData_Cleaned_2")
    df = pd.DataFrame(df)
    user = "Frommoh"

    x = top_n_occurences(df, "Champion", user)
    print(x)
    print(type(x))

    x = top_n_occurences(df, "Champion", user, to_dict=True)
    print(x)
    print(type(x))

    """
    current_user = "Ausfreak"
    region = "OC1"
    df = get_match_details(current_user, region, 5000)
    df = col_to_string(df, "WinLoss")
    df["WinLoss"] = df["WinLoss"].map(encode_true_false)
    df = impute_mode_lane(df)
    df = encode_categorical(df, "Lane")
    df.to_csv("./TestData_Cleaned_3")
    """
    



 