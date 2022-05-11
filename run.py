from re import U
from src.GetData import get_match_details, get_puuid, get_account_id, get_id, get_account_info, get_match_history, get_match_details
import pandas as pd

if __name__ == "__main__":
    user = "Drakuns"
    region = "OC1"
    no_games = 10000
    df = get_match_details(user, region, no_games)
    df.to_csv("./TestData")
  