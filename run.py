from re import U
from src.GetData import get_match_details, get_puuid, get_account_id, get_id, get_account_info, get_match_history, get_match_timeline
from src import my_region

if __name__ == "__main__":
    user = "Frommoh"
    region = my_region

    df = get_match_details(user, region)
    print(df)