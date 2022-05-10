import pandas as pd
from sqlalchemy import over
from CleanData import encode_categorical, encode_true_false, col_to_string
import statsmodels.api as sm

def logit_model(df, y, x_list):
    """
    Creates a logistic regression model
    Arguments: 
        df : A pandas dataframe containg the data
        y  : The name of the column housing the y or prediction values
             Should be 1 for True, 0 for False
        x  : A list of variable names for the predictor values
    Returns:
        A statsmodel model
    """
    y = df[[y]]
    X = df[x_list]
    logit_model=sm.Logit(y,X)
    result=logit_model.fit()
    return result


def top_n_occurences(df, col_name, n = 3):
    """
    Returns the top n occurnces of a column in a data frame
    Arguments:
        df: A pandas dataframe
        col_name: The column name for the results of interest in the dataframe
        n: An integer value for how many of the top occurences you want returned 
    Returns:
        A pandas data frame with the top n occurnces
    """
    values = df[col_name].value_counts()
    nlargest = values.nlargest(n)
    return nlargest

def top_n_win(df, col_name, n = 3):
    """
    Returns the top n occuring values in a column where the game was a win
    Arguments:
        df: A pandas dataframe
        col_name: The column name for the results of interest in the dataframe
        n: An integer value for how many of the top occurences you want returned 
    Returns
        A pandas data frame with the top n occurnces
    """
    df = df[df["WinLoss"] == 1]
    nlargest = top_n_occurences(df, col_name, n)
    return nlargest
    

def column_mean(df, col_name):
    """
    Finds the average (mean) of a numerical column in a pandas df
    Arguments:
        df: A pandas dataframe
        col_name: the column name to find the average for
    Returns:
        An average (mean) of type float
    """
    total = sum(df[col_name])
    n = len(df[col_name])
    avg = total / n
    return avg

def win_ratio_str(df, col_name, target):
    """
    Finds the winrate for a given column and target
    Must be used on a column with string values 
    Arguments:
        df: A pandas dataframe
        col_name: A string of the column name to find the win rate for
        target: A string of the attribute to find the win rate for
    Returns:
        A two decimal floating point number
    """
    win_df = df[(df["WinLoss"] == 1) & (df[col_name] == target)]
    total_df = df[df[col_name] == target]

    wins = len(win_df)
    total = len(total_df)

    win_rate = wins / total * 100

    win_rate = round(win_rate,2)

    return win_rate

def overall_win_ratio(df):
    """
    Finds the overall win rate for the given df
    Arguments:
        df: A pandas dataframe
    Returns:
        A two decimal floating point number
    """

    wins = df["WinLoss"]
    total_wins = sum(wins)
    total = len(df)

    win_rate = total_wins / total * 100
    win_rate = round(win_rate,2)

    return win_rate



if __name__ == "__main__":

    df = pd.read_csv('./TestData')
    df = pd.DataFrame(df)
    df = col_to_string(df, "WinLoss")
    df['WinLoss'] = df['WinLoss'].map(encode_true_false)

    df = encode_categorical(df, "Lane")

    print(overall_win_ratio(df))
  
  
    
   
    
    
