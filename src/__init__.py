
from riotwatcher import LolWatcher, ApiError
import pandas as pd
from flask import Flask, render_template

api_key = 'RGAPI-9ff75d61-f717-458b-bf9d-7e2f0c9aeed6'
watcher = LolWatcher(api_key)


app = Flask(__name__)
app.config["DEBUG"] = True