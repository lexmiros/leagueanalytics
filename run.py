
from src.flaskApp import app, routes


if __name__ == "__main__":

    app.run()


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
    



 