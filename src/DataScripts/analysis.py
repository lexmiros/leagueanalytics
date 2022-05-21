import pandas as pd

from src.DataScripts.CleanData import  top_n_occurences
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

    X = ( X-  X.mean()) / X.std()

    logit_model = sm.Logit(y,X)
    #model = logit_model.fit_regularized(method='l1', alpha=1.0, L1_wt=0.3)
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


    if len(counts) > 300:
    #Counts is equal to all champs with at least z games
        counts = counts[counts > 10]
    else:
        counts = counts[counts > 5]

         
    
    
    wr_list = []
    
    for champ in counts.index:
        entry = {"Name" : champ, "Win Rate":win_ratio_str(df,"Champion", champ)}
        wr_list.append(entry)
    
    sorted_wr = sorted(wr_list, key=lambda d: d['Win Rate'], reverse=True)
    sorted_wr = sorted_wr[:n] 

    return sorted_wr



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

    names = x.index.tolist()
    values = x.tolist()
    
    coef_names_pos = []
    coef_values_pos = []
    coef_names_neg = []
    coef_values_neg = []
    for i in range(len(names)):
        if values[i] > 0.0001:
            coef_names_pos.append(names[i])
            coef_values_pos.append(values[i])
        elif values[i] < 0.0001:
            values[i] = values[i] * (-1) 
            coef_names_neg.append(names[i])
            coef_values_neg.append(values[i])
    
    return coef_names_pos, coef_values_pos, coef_names_neg, coef_values_neg

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

def get_column_cumulative(df, col_name):
    """
    Finds the cumulative values for a column at each point
    Arguments:
        df: A pandas dataframe
        col_name: string of the column of interest
    Returns:
        A list of the cumulative values
    """
    sum_list = []

    for i in range(len(df.index)):
        cumulative_point = df[col_name].iloc[:i].sum()
        sum_list.append(cumulative_point)

    return sum_list

def get_wr_cumulative(df):
    """
    Finds the cumulative values for a column at each point
    Arguments:
        df: A pandas dataframe
        col_name: string of the column of interest
    Returns:
        A list of the cumulative values
    """
    sum_list = []

    for i in range(1, len(df.index)):
        cumulative_df = df.iloc[:i]
        wr = overall_win_ratio(cumulative_df)
        sum_list.append(wr)

    return sum_list


    

    
    
    
    

    


    
  
  
    
   
    
    
