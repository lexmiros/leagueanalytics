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

def top_n_occurences(df, col_name, user ,n = 3, to_dict = False):
    """
    Returns the top n occurnces of a column in a data frame
    Arguments:
        df: A pandas dataframe
        col_name: The column name for the results of interest in the dataframe
        n: An integer value for how many of the top occurences you want returned 
        to_dict : False to return pandas dataframe, True to return a list of dictionaries
    Returns:
        A pandas data frame or list of dictionaries 
    """
    df = df[df["SummonerName"] == user]
    values = df[col_name].value_counts()
    nlargest = values.nlargest(n)

    #Turns df to dictionary
    if to_dict:
        names_list = []
        values_list = []
        dictionary_list = []

        for names in nlargest.index:
            names_list.append(names)
        for values in nlargest:
            values_list.append(values)
        
        for i in range(0, len(names_list)):
            entry = {"Name" : names_list[i], "Games" : values_list[i]}
            dictionary_list.append(entry)
        return dictionary_list

    return nlargest

def champ_list_invalid(df):
    """
    Finds a unique list of champion names where there is at least one instance
    of the champion having a lane of 'Invalid'
    Arguments:
        df: A pandas dataframe with columns "Lane" and "Champion"
    Returns:
        A list of unique champion names
    """
    invalid_list = df.loc[df["Lane"] == "Invalid","Champion"]
    invalid_list = invalid_list.unique()

    return invalid_list

def impute_mode_lane(df):
    """
    Changes all "Invalid" lanes to the most common lane type, based on the champion
    If "Invalid" is the most common lane type for said champion change to second most
    common type, if exists
    Arguments:
        df: A pandas dataframe with columns "Lane" and "Champion"
    Returns:
        A pandas dataframe 
    """
    invalid_list = champ_list_invalid(df)
    
    for champ in invalid_list:
        df_champ = df[df["Champion"] == champ] 
        lane_mode = df_champ['Lane'].value_counts().index.tolist()
        
        if lane_mode[0] != "Invalid":
            df.loc[(df["Lane"] == "Invalid") & (df["Champion"] == champ),"Lane"] = lane_mode[0]
        elif len(lane_mode) > 1 and lane_mode[1] != "Invalid":
            df.loc[(df["Lane"] == "Invalid") & (df["Champion"] == champ),"Lane"] = lane_mode[1]
        else:
            df.drop(df[(df["Lane"] == "Invalid") & (df["Champion"] == champ)].index, inplace=True)

    return df
 

