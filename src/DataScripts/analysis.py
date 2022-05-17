import pandas as pd

from src.DataScripts.CleanData import encode_categorical, encode_true_false, col_to_string, top_n_occurences
import statsmodels.api as sm

def build_logit_model(df, y, x_list, p_value):
    """
    Creates a logistic regression model
    Uses recursion to remove all x until all x have p < p_value
    Arguments: 
        df : A pandas dataframe containg the data
        y  : The name of the column housing the y or prediction values
             Should be 1 for True, 0 for False
        x  : A list of variable names for the predictor values
    Returns:
        A statsmodel model
    """
    y = df[[y]]
    X = df[df.columns & x_list]

    logit_model = sm.Logit(y,X)
    model = logit_model.fit()

    significant_x = model.pvalues < p_value
    p_05 = significant_x.all()
    if p_05 == True:
        return model
    else:
        try:
            y = "WinLoss"
            significant_x = significant_x[significant_x]
            x = significant_x.index.tolist()
            return build_logit_model(df = df,y = y, x_list = x, p_value= p_value)
        except ValueError:  #raised if `y` is empty.
            return model



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

    
def user_win_loss_wr(df, user):
    win_df = df[(df["WinLoss"] == 1) & (df["SummonerName"] == user)]
    loss_df = df[(df["WinLoss"] == 0) & (df["SummonerName"] == user)]
    wr_df = df[df["SummonerName"] == user]

    wins = len(win_df)
    losses = len(loss_df)
    wr =  round(100*wins / len(wr_df),2)

    return wins, losses, wr

def top_champs_by_wr(df,n, user):
    """
    Finds the highest n champions by win-rate
    Arguments:
        df: A pandas dataframe with a Champion column
        n: An integer for how many champions to return
    Returns:
        A list of dictionaries where Name is the champion and Win Rate is the win rate
    """
    df = df[df["SummonerName"] == user]
    counts = df["Champion"].value_counts()


    if len(counts) > 100:
    #Counts is equal to all champs with at least z games
        counts = counts[counts > 10]
    elif len(counts) > 50:
        counts = counts[counts > 5]
    elif len(counts) > 15:
        counts = counts[counts > 2]

         
    
    
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
        A dictionary 
            Spell : the spell name
            Casts : number of uses of that spell
    """
    df_champ = df[df["Champion"] == champ]
    casts = {}
    casts["Q"] = df_champ["Q casts"].sum()
    casts["W"] = df_champ["W casts"].sum()
    casts["E"] = df_champ["E casts"].sum()
    casts["R"] = df_champ["R casts"].sum()

    
    max_casts = {"Spell" : max(casts, key=casts.get), "Casts" :  casts[max(casts, key=casts.get)]}

    return max_casts

def top_cast_top_n_champs(df, n):
    """
    Finds the most casted ability for the top n played champions
    Arguments:
        df: A pandas dataframe with Q casts,W casts,E casts,R casts, Champion columns
        n: An integer representing the top n champs to find casts for 
    Returns:
        A dictionary 
            Name  : Champions name
            Spell : the spell name
            Casts : number of uses of that spell
    """
    n_champs = top_n_occurences(df,"Champion", n, True)
    
    cast_dict = []
    for champ in n_champs:
        x = top_cast_champ(df, champ)
        cast_dict.append({"Name" : champ, "Spell" : x["Spell"], "Casts": x["Casts"] })
       

    return cast_dict


def top_cast_top_wr_champs(df, n):
    """
    Finds the most casted ability for the champions with the top n highest win rates
    Arguments:
        df: A pandas dataframe with Q casts,W casts,E casts,R casts, Champion columns
        n: An integer representing the top n champs to find casts for 
    R eturns:
        A dictionary 
            Name  : Champions name
            Spell : the spell name
            Casts : number of uses of that spell
    """
    n_champs = top_champs_by_wr(df, n)

    champ_list = []
    for i in range(0, len(n_champs)):
        champ_list.append(n_champs[i]["Name"])
    
    cast_dict = []
    for champ in champ_list:
        x = top_cast_champ(df, champ)
        cast_dict.append({"Name" : champ, "Spell" : x["Spell"], "Casts": x["Casts"] })
       

    return cast_dict

def get_model_coefs(model):
    """
    Finds the top 5 highest coefficients of a statsmodel model
    Arguments:
        model : a statsmodel model
    Returns:
       A list of coefficients in descending order
    """
    x = model.params
    x = x.sort_values(ascending = False)
    x = x.index
    print(x)
    coef_list = []
    for i in range(0,5):
        coef_list.append(x[i])
    return coef_list

def get_user_avg(df, user, col_name):
    """
    Gets the avg for a column where summonername is the user
    Arguments:  
        df : a pandas dataframe
        user : string for summonername within the df 
        col_name : the column name of interest
    Returns:
        avg : a float average rounded to 2 decimal places
            
    """

    df = df[df["SummonerName"] == user]
    avg = df[col_name].mean()
    avg = round(avg,2)
    return avg

def get_non_user_avg(df, user, col_name):
    """
    Gets the avg for a column where summonername is NOT the user
    Arguments:  
        df : a pandas dataframe
        user : string for summonername within the df
        col_name : the column name of interest
    Returns:
        avg : a float average rounded to 2 decimal places
            
    """

    df = df[df["SummonerName"] != user]
    avg = df[col_name].mean()
    avg = round(avg,2)
    return avg
    
def get_user_stats(df, user, variables_list):
    """
    Gets the avg for a list of columns for a given user
    Arguments:  
        df : a pandas dataframe
        user : string for summonername within the df
        varibale_list : list of column names of interest
    Returns:
        Dictionary:
            Variable name : average
    """
    user_stats = {}
    for variable in variables_list:
        avg = get_user_avg(df, user, variable)
        user_stats[variable] = avg
    
    return user_stats

def get_non_user_stats(df, user, variables_list):
    """
    Gets the avg for a list of columns for a everyone bar the given user
    Arguments:  
        df : a pandas dataframe
        user : string for summonername within the df
        varibale_list : list of column names of interest
    Returns:
        Dictionary:
            Variable name : average
    """
    user_stats = {}
    for variable in variables_list:
        avg = get_non_user_avg(df, user, variable)
        user_stats[variable] = avg
    
    return user_stats

def played_role_count(df, role):
    df = df[df[role] == 1]
    count = len(df)
    return count

def role_wins(df, role):
    df = df[(df[role] == 1) & (df["WinLoss"] == 1)]
    count = len(df)
    return count       

def role_losses(df, role):
    df = df[(df[role] == 1) & (df["WinLoss"] == 0)]
    count = len(df)
    return count   

def add(row):
    ratio = (row[0] / row[1])
    return ratio

def get_user_top_stats(df, user, variable_list):

    user_stats = get_user_stats(df, user, variable_list )
    non_user_stats = get_non_user_stats(df, user, variable_list )

    new_df = pd.DataFrame()
    new_df["User"] = user_stats.values()
    new_df["Non-user"] = non_user_stats.values()
    new_df.index = user_stats.keys()

    new_df['Ratio'] = new_df.apply(add, axis=1)

    new_df = new_df.sort_values("Ratio", ascending=False)
    top_df = new_df[0:5]

    return top_df

def get_user_bottom_stats(df, user, variable_list):

    user_stats = get_user_stats(df, user, variable_list )
    non_user_stats = get_non_user_stats(df, user, variable_list )

    new_df = pd.DataFrame()
    new_df["User"] = user_stats.values()
    new_df["Non-user"] = non_user_stats.values()
    new_df.index = user_stats.keys()

    new_df['Ratio'] = new_df.apply(add, axis=1)

    new_df = new_df.sort_values("Ratio", ascending=True)
    bottom_df = new_df[0:5]

    return bottom_df

def win_ratio_str_formatted(df, col_name, target):
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
    win_rate = str(win_rate)
    win_rate = f"{win_rate}%"
    return win_rate


if __name__ == "__main__":
    """"""
 

    

    
    
    
    

    


    
  
  
    
   
    
    
