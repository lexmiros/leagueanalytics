import pandas as pd

from src.DataScripts.CleanData import  top_n_occurences
import statsmodels.api as sm

def build_logit_model(df: pd.DataFrame, y: str, x_list: list, p_value: float) -> sm.regression.linear_model:
    """
    Creates a logistic regression model
    Uses recursion to remove all coefficients until all have p < p_value

    Parameters
    ---------- 
    df: Pandas dataframe
        A pandas dataframe containg the data
    y: str
        The name of the column housing the y or prediction values
        Column values should be encoded to 1 / 0
    x_list: list
        A list of variable names for the predictor values
    p_value: float
        the desired p-value all coefficients should be
        less than
    Returns
    -------
    Statsmodel 
        The logistic regression model
    """
    #Set y and X
    y = df[[y]]
    X = df[df.columns & x_list]

    #Normalise X values
    X = ( X -  X.mean()) / X.std()

    #Build model
    logit_model = sm.Logit(y,X)
    model = logit_model.fit()

    #Check significance of X coefficients
    significant_x = model.pvalues < p_value
    p_05 = significant_x.all()

    #Recursively run to remove all x > p_value
    if p_05 == True:
        return model
    else:
        try:
            y = "WinLoss"
            significant_x = significant_x[significant_x]
            x = significant_x.index.tolist()
            return build_logit_model(df = df,y = y, x_list = x, p_value= p_value)
        except ValueError:  
            return model

def get_model_coefs(model: sm.regression.linear_model) -> tuple:
    """
    Finds positive and negative coefficients of a model

    Splits a models coefficients into positive and negative
    If a models coefficients is zero, it is ignored

    Parameters:
    -----------
    model : statsmodel
        The model to find the coefficients for
    Returns:
    --------
    Tuple of lists:
        Tuple of length 4:
            0 : list of positive coefficient names
            1 : list of positive coefficient values
            2 : list of negative coefficient names
            3 : list of negative coefficient values
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
        if values[i] > 0:
            coef_names_pos.append(names[i])
            coef_values_pos.append(values[i])
        elif values[i] < 0:
            values[i] = values[i] * (-1) 
            coef_names_neg.append(names[i])
            coef_values_neg.append(values[i])
    
    return coef_names_pos, coef_values_pos, coef_names_neg, coef_values_neg


def get_user_top_stats(df: pd.DataFrame, user: str, variable_list: list) -> pd.DataFrame:
    """
    Finds the top 5 averages for a list of columns,
    where the top 5 is determined by the ratio between the user's
    average compared to all other players in the dataframe

    Parameters:
    -----------
    df: Pandas dataframe
        The dataframe of interest
    user: str
        The user to find the averages for
    variable_list: list of strings
        Variables to consider the averages for

    Returns:
    -------
    Pandas dataframe
        Contains the top 5 averages for the ratio
        user / non-user
    """

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

def get_user_bottom_stats(df: pd.DataFrame, user: str, variable_list: list) -> pd.DataFrame:
    """
    Finds the bottom 5 averages for a list of columns,
    where the bottom 5 is determined by the ratio between the user's
    average compared to all other players in the dataframe

    Parameters:
    -----------
    df: Pandas dataframe
        The dataframe of interest
    user: str
        The user to find the averages for
    variable_list: list of strings
        Variables to consider the averages for

    Returns:
    -------
    Pandas dataframe
        Contains the bottom 5 averages for the ratio
        user / non-user
    """

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

def get_column_cumulative(df: pd.DataFrame, col_name: str) -> list:
    """
    Finds the cumulative values for a column at each row

    Parameters:
    -----------
    df: Pandas dataframe:
        Dataframe of interest
    col_name: str
        string of the column of interest
    Returns:
    --------
        A list of the cumulative values
    """

    sum_list = []

    for i in range(len(df.index)):
        cumulative_point = df[col_name].iloc[:i].sum()
        sum_list.append(cumulative_point)

    return sum_list

def get_wr_cumulative(df):
    """
    Finds the cumulative win rates at each row for a df containing
    a "WinLoss" column

    Parameters:
    -----------
    df: Pandas dataframe:
        Dataframe of interest

    Returns:
    --------
        A list of the cumulative values
    """
    sum_list = []

    for i in range(1, len(df.index)):
        cumulative_df = df.iloc[:i]
        wr = overall_win_ratio(cumulative_df)
        sum_list.append(wr)

    return sum_list


def win_ratio_str(df: pd.DataFrame, col_name: str, target: str) -> float:
    """
    Finds the winrate for a given column and target
    Must be used on a column with string values 

    Parameters
    ----------
    df: Pandas dataframe
        Dataframe of interest
    col_name: str
        A string of the column name to find the win rate for
    target: str 
        A string of the attribute to find the win rate for
    Returns
    -------
    Float
        A two decimal floating point number
    """
    win_df = df[(df["WinLoss"] == 1) & (df[col_name] == target)]
    total_df = df[df[col_name] == target]

    wins = len(win_df)
    total = len(total_df)

    win_rate = wins / total * 100

    win_rate = round(win_rate,2)

    return win_rate

def win_ratio_str_formatted(df: pd.DataFrame, col_name: str, target: str) -> str:
    """
    Finds the winrate for a given column and target and formats
    the value with a percent sign (%)
    Must be used on a column with string values 

    Parameters:
    -----------
    df: Pandas dataframe
        The dataframe of interest
    col_name: str
        A string of the column name to find the win rate for
    target: str
        A string of the attribute to find the win rate for
    Returns:
    --------
    str
        A two decimal point number in sting format with a % sign at 
        the end
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

def overall_win_ratio(df: pd.DataFrame):
    """
    Finds the overall win rate for the given df

    Parameters
    ----------
    df: Pandas dataframe
        Dataframe of interest
    Returns
    -------
    Float
        A two decimal floating point number
    """

    wins = df["WinLoss"]
    total_wins = sum(wins)
    total = len(df)

    win_rate = total_wins / total * 100
    win_rate = round(win_rate,2)

    return win_rate

    
def user_win_loss_wr(df: pd.DataFrame, user: str) -> tuple:
    """
    Finds the total wins, losses, and the winrate for a given summoner

    Parameters:
    ----------
    df: Pandas dataframe
        The dataframe of interest
    user : str
        The summoner name of interest
    Returns:
    -------
    Tuple:
        Tuple of length 3:
            0 : Wins (int)
            1: Losses (int)
            2: winrate (float)
    """

    win_df = df[(df["WinLoss"] == 1) & (df["SummonerName"] == user)]
    loss_df = df[(df["WinLoss"] == 0) & (df["SummonerName"] == user)]
    wr_df = df[df["SummonerName"] == user]

    wins = len(win_df)
    losses = len(loss_df)
    wr =  round(100*wins / len(wr_df),2)

    return wins, losses, wr


def top_champs_by_wr(df: pd.DataFrame,n: int, user: str) -> list:
    """
    Finds the top n champions by descending win-rate. Champion must
    have been played at least 5 times in a given lane to be considered

    Parameters:
    -----------
    df: Pandas dataframe
        A pandas dataframe with a Champion column
    n: Int 
        An integer for how many champions to return
    Returns:
    --------
        A list of dictionaries where Name is the champion and Win Rate is the win rate
    """

    df = df[df["SummonerName"] == user]
    counts = df["Champion"].value_counts()

    #Counts is equal to all champs with at least 5 games
    counts = counts[counts >= 5]
    
    wr_list = []
    
    for champ in counts.index:
        entry = {"Name" : champ, "Win Rate":win_ratio_str(df,"Champion", champ)}
        wr_list.append(entry)
    
    sorted_wr = sorted(wr_list, key=lambda d: d['Win Rate'], reverse=True)
    sorted_wr = sorted_wr[:n] 

    return sorted_wr



def get_user_avg(df: pd.DataFrame, user: str, col_name: str) -> float:
    """
    Gets the avg for a column where the SummonerName column equals user

    Parameters:
    -----------  
    df : Pandas dataframe 
        The pandas dataframe of interest
    user : str 
        string for summonername within the df 
    col_name : str
        the column name of interest
    Returns:
    --------
    Float:
        a float average rounded to 2 decimal places
            
    """

    df = df[df["SummonerName"] == user]
    avg = df[col_name].mean()
    avg = round(avg,2)
    return avg

def get_non_user_avg(df: pd.DataFrame, user: str, col_name: str) -> float:
    """
    Gets the avg for a column where summonername is NOT the user

    Parameters:
    -----------  
    df : Pandas dataframe
        Dataframe of interest
    user : str
        string for summonername within the df
    col_name : str 
        the column name of interest
    Returns:
    --------
    float:
        a float average rounded to 2 decimal places
            
    """

    df = df[df["SummonerName"] != user]
    avg = df[col_name].mean()
    avg = round(avg,2)
    return avg
    
def get_user_stats(df: pd.DataFrame, user: str, variables_list: list) -> dict:
    """
    Gets the averages for a list of columns where SummonerName
    is equal to user

    Parameters:
    -----------  
    df : Pandas dataframe
        dataframe of interest
    user : str
        string for summonername within the df
    varibale_list : list 
        list of column names of interest
        columns should contain numerical values
    Returns:
    --------
    Dictionary:
        Variable name : average
    """

    user_stats = {}
    for variable in variables_list:
        avg = get_user_avg(df, user, variable)
        user_stats[variable] = avg
    
    return user_stats

def get_non_user_stats(df: pd.DataFrame, user: str, variables_list: list) -> dict:
    """
    Gets the averages for a list of columns where SummonerName
    is NOT equal to user

    Parameters:
    -----------  
    df : Pandas dataframe
        dataframe of interest
    user : str
        string for summonername within the df
    varibale_list : list 
        list of column names of interest
        columns should contain numerical values
    Returns:
    --------
    Dictionary:
        Variable name : average
    """
    user_stats = {}
    for variable in variables_list:
        avg = get_non_user_avg(df, user, variable)
        user_stats[variable] = avg
    
    return user_stats


def role_wins(df: pd.DataFrame, role: str) -> int:
    """
    Finds the number of wins for a specific role

    Parameters:
    ----------
    df: Pandas dataframe
        Dataframe of interest
    role: str
        The role of interest :
            TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY
    Returns:
    --------
    int:
        Count of the number of wins for the role
    """
    df = df[(df[role] == 1) & (df["WinLoss"] == 1)]
    count = len(df)
    return count       

def role_losses(df: pd.DataFrame, role: str) -> int:
    """
    Finds the number of losses for a specific role

    Parameters:
    ----------
    df: Pandas dataframe
        Dataframe of interest
    role: str
        The role of interest :
            TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY
    Returns:
    --------
    int:
        Count of the number of losses for the role
    """

    df = df[(df[role] == 1) & (df["WinLoss"] == 0)]
    count = len(df)
    return count   

def add(row: pd.Series) -> pd.Series:
    """
    Finds the ratio between the first and second column
    of a row

    Parameters:
    -----------
    row: Pandas series
        The row to find the ratio of
    Returns:
    --------
    Pandas series:
        A new column of the ratio between the specified columns
    """

    ratio = (row[0] / row[1])
    return ratio







    

    
    
    
    

    


    
  
  
    
   
    
    
