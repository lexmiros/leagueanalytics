import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

def encode_true_false(df_column):
    if df_column == 'True':
        return 1
    elif df_column == 'False':
        return 0 
    else:
        return "Error"

def col_to_string(df, col_name):
    df[col_name] = df[col_name].astype(str)
    return df

def encode_categorical(df, col_name):
    encoded = pd.get_dummies(df[col_name])
    df = pd.concat([df, encoded], axis = 1)
    df = df.drop(col_name, 1)
    return df

if __name__ == "__main__":

    df = pd.read_csv('./TestData')
    df = pd.DataFrame(df)
    df = col_to_string(df, "WinLoss")
    df['WinLoss'] = df['WinLoss'].map(encode_winloss)

    df = encode_categorical(df, "Lane")
    print(df)

    