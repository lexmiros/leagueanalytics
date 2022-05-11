from src import *
import pandas as pd


from CleanData import champ_list_invalid

if __name__ == "__main__":
    """
    """
    df = pd.read_csv('./TestData')
    df = pd.DataFrame(df)
    invalid_list = champ_list_invalid(df)
    print(invalid_list)
    
    
    