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
    top_wr_champs = top_champs_by_wr(df, n)
    labels = []
    win_rates = []
    for champs in top_wr_champs:
        labels.append(champs["Name"])
        win_rates.append(champs["Win Rate"])

    return render_template("overview.html", labels = labels, win_rates = win_rates, n = n)