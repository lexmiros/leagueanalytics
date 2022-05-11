import pandas as pd

from CleanData import encode_categorical, encode_true_false, col_to_string, top_n_occurences
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

def top_champs_by_wr(df,n):
    """
    Finds the highest n champions by win-rate
    Arguments:
        df: A pandas dataframe with a Champion column
        n: An integer for how many champions to return
    Returns:
        A list of dictionaries where Name is the champion and Win Rate is the win rate
    """
    counts = df["Champion"].value_counts()
    counts = counts[counts > 10]
    
    
    wr_list = []
    
    for champ in counts.index:
        entry = {"Name" : champ, "Win Rate":win_ratio_str(df,"Champion", champ)}
        wr_list.append(entry)
    
    sorted_wr = sorted(wr_list, key=lambda d: d['Win Rate'], reverse=True)
    sorted_wr = sorted_wr[:n] 

    return sorted_wr

def top_cast_champ(df, champ):
    """
    Finds the most casted ability for a champ
    Arguments:
        df: A pandas dataframe with Q casts,W casts,E casts,R casts, Champion columns
        champ: String of the champion of interest 
    Returns:
        A dictionary where the key is the ability and the value is the number of casts
    """
    df_champ = df[df["Champion"] == champ]
    casts = {}
    casts["Q"] = df_champ["Q casts"].sum()
    casts["W"] = df_champ["W casts"].sum()
    casts["E"] = df_champ["E casts"].sum()
    casts["R"] = df_champ["R casts"].sum()

    max_casts = {}
    max_casts[max(casts, key=casts.get)] = casts[max(casts, key=casts.get)]

    return max_casts

def top_cast_top_n_champs(df, n):
    """
    Finds the most casted ability for a champ
    Arguments:
        df: A pandas dataframe with Q casts,W casts,E casts,R casts, Champion columns
        n: An integer representing the top n champs to find casts for 
    Returns:
        A dictionary where the key is the champion name, in order for most played champ
    """
    n_champs = top_n_occurences(df,"Champion", n, True)
    
    cast_dict = {}
    for champ in n_champs:
        cast_dict[champ] = top_cast_champ(df, champ)

    return cast_dict

if __name__ == "__main__":

    df = pd.read_csv('./TestData_Cleaned')
    df = pd.DataFrame(df)

    x = top_champs_by_wr(df, 5)
    print(x)

    

    
    
    
    

    


    
  
  
    
   
    
    
