import pandas as pd
from CleanData import encode_categorical, encode_true_false, col_to_string
import statsmodels.api as sm

def logit_model(df, y, x_list):
    y = df[[y]]
    X = df[x_list]
    logit_model=sm.Logit(y,X)
    result=logit_model.fit()
    return result


if __name__ == "__main__":

    df = pd.read_csv('./TestData')
    df = pd.DataFrame(df)
    df = col_to_string(df, "WinLoss")
    df['WinLoss'] = df['WinLoss'].map(encode_true_false)

    df = encode_categorical(df, "Lane")
    variables_of_interest = ["SummonerSpell1","Spell1Casts","SummonerSpell2","Spell2Casts","Q casts","W casts","E casts","R casts","ChampLevel","CS","Kills","Deaths","Assists","Exp","Damage","TotalDamageTaken","WardsPlace","WardsKilled"]
    
    model = logit_model(df, "WinLoss", variables_of_interest)
    print(model.summary2())

    
    
