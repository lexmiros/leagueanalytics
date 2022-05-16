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
    app.run()
    #current_user = "Incursio"
    #region = "OC1"


    
    
    

 





    """
    
    df = get_match_details(user, region, 5000)
    df = col_to_string(df, "WinLoss")
    df["WinLoss"] = df["WinLoss"].map(encode_true_false)
    df = impute_mode_lane(df)
    df = encode_categorical(df, "Lane")
    df.to_csv("./TestData_Cleaned")
    """
 