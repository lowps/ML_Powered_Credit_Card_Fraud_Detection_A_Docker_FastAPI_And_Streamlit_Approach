import os
import sys
import pandas as pd
import numpy as np
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.logger import Logger
from utils.helpers import get_directory_name

absolute_path = 'Developing_and_Deploying_a_Predictive_Analytics_Platform_Using_FastAPI_Streamlit_and_Docker/empirical/src/ii_data_preprocessing.py'
inspector_gadget = get_directory_name(absolute_path)
inspector_gadget = Logger(inspector_gadget)


def csv_to_df(absolute_path:str) -> pd.DataFrame:
    '''
    Fetches the CSV file from the specified absolute path and converts it to a pandas DataFrame.

    Parameters:
    :absolute_path:(str): The specified absolute path where the CSV file is located.

    Returns:
    :pd.DataFrame:
    '''
    #check if the file has a '.csv' extension
    if not absolute_path.lower().endswith('.csv'):
        inspector_gadget.get_log().error(f'csv_to_df() unsuccessful. The file at {absolute_path} is not a .csv file.')
        raise ValueError(f'The file at {absolute_path} is not a .csv file.')
    
    #check if the file exists
    if not os.path.isfile(absolute_path):
        inspector_gadget.get_log().error(f"The file at {absolute_path} does not exist. Verify if absolute path was provided.")
        raise FileNotFoundError(f"csv_to_df() unsuccessful. The file at {absolute_path} does not exist.")
   
    #convert csv file into pandas.DataFrame
    df = pd.read_csv(absolute_path)
    inspector_gadget.get_log().info("csv_to_df() success, csv file successfully converted to dataframe.")
    return df 


def feature_engineering_string_extraction(df:pd.DataFrame, target_col:str, new_col:str, delimiter:str = " ", position:int = 0) -> pd.DataFrame:
    '''
    Extracts string elements from a specified column wtihin a Dataframe. The extracted string is based on parameters
    delimiter and position. The delimiter and position will map the string within the column and extract its string value.
    The extracted string value will be the row values of the newly generated column specified with new_col parameter.

    Parameters
    :df:(pd.DataFrame): The Dataframe containing the data.
    :target_col:(str): The column(s) to which the function will be applied. Can be one or more column names.
    :new_col:(str): The new column generated. It holds the extracted data.
    :delimiter:(str): The delimiter specified to split the strings in the target column. Default is a space (" ")
    :position:(int): The position of the element in the split string to extract. Default is the first element (position = 0).
    
    Returns:
    :pd.DataFrame: The Dataframe with the new column added.
    '''
    try:
        df[new_col] = df[target_col].apply(lambda x: x.split(delimiter)[position] if isinstance(x, str) else None)
        inspector_gadget.get_log().info("feature_engineering_string_extraction() successful.")
    except Exception as e:
        inspector_gadget.get_log().error(f"feature_engineering_string_extraction() unsuccessful, {e}.")
    return df


def remove_alphabetic_chars(df, *target_col):
    '''
    Removes all alphabetic characters.

    Parameters
    :df:(pd.DataFrame): The Dataframe containing the data.
    :target_col:(str): The column(s) to which the function will be applied. Can be one or more column names.
    
    Returns:
    :pd.DataFrame: 
    '''
    try:
        for col in target_col:
            df[col] = df[col].str.replace('[a-zA-Z]', '', regex=True)
        inspector_gadget.get_log().info('remove_alphabetic_chars() successful')
    except Exception as e:
        inspector_gadget.get_log().error(f'remove_alphabetic_chars() unsuccessful, {e}')
        raise Exception
    return df


def remove_all_non_alphanumeric_characters(df, *target_col):
    '''
    Removes all non alphanumeric characters.

    Parameters
    :df:(pd.DataFrame): The Dataframe containing the data.
    :target_col:(str): The column(s) to which the function will be applied. Can be one or more column names.
    
    Returns:
    :pd.DataFrame: 
    '''
    try:
        for col in target_col:
            df[col] = df[col].str.replace('[^a-zA-Z0-9]', '', regex=True)
        inspector_gadget.get_log().info('remove_all_non_alphanumeric_characters() successful')
    except Exception as e:
        inspector_gadget.get_log().error(f'remove_all_non_alphanumeric_characters() unsuccessful, {e}')
        raise Exception
    return df 


def replace_empty_cells_to_NaN(df, *target_col):
    '''
    Replace any columns holding empty values within their cells with NaN data type.

    Parameters
    :df:(pd.DataFrame): The Dataframe containing the data.
    :target_col:(str): The column(s) to which the function will be applied. Can be one or more column names.
    
    Returns:
    :pd.DataFrame: 
    '''
    try:
        for col in target_col:
            df[col] = df[col].replace('', np.nan)
        inspector_gadget.get_log().info("replace_empty_cells_to_NaN() successful")
    except Exception as e:
        inspector_gadget.get_log().error(f"replace_empty_cells_to_NaN() unsuccessful, {e}.")
    return df 


def int_converter(df:pd.DataFrame, *target_col:str):
    '''
    Converts specified columns data type to int data type.

    Parameters:
    :df:(pd.DataFrame): The Dataframe containing the data.
    :target_col:(str): The column(s) to which the function will be applied. Can be one or more column names.

    Returns:
    :pd.DataFrame:
    '''
    try:
        [df.__setitem__(col, pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)) for col in target_col]
        inspector_gadget.get_log().info("int_converter() successful.")
            #df.__setitem__(col, value) is equivalent to df[col] = value. It sets the column col in the DataFrame df to value.
            #Non-numeric values are turned into NaN because of errors='coerce'.
    except Exception as e:
        inspector_gadget.get_log().error(f"int_converter() unsuccessful, {e}.")  
    return df


def generate_miles_driven_column(df, target_col, new_col):
    '''
    Inserts a new column to dataframe containing 'miles driven' information

    Parameters:
    :df:(pd.DataFrame): The Dataframe containing the data.
    :target_col:(str): The column to which the function will be applied.
    :new_col:(str): The name of the newly generated column.

    Returns:
    :pd.DataFrame:
    '''
    try:
        for col in target_col:
            df[new_col] = round(df[target_col] * 0.621371, 0)
        inspector_gadget.get_log().info(f"generate_miles_driven_column() successful")
    except Exception as e:
        inspector_gadget.get_log().error(f"generate_miles_driven_column() unsuccessful, {e}.") 
    return df 


def truncate_column_values(df:pd.DataFrame, start:int, stop:int, *target_col:str) -> pd.DataFrame:
    '''
    shortens the values in a column by slicing them according to specified start and stop positions.

    Parameters:
    :df:(pd.DataFrame): The DataFrame containing the columns to be processed.
    :start:(int): The starting index for slicing.
    :stop:(stop): The ending index for slicing.
    :target_col:(str): The column(s) in the DataFrame that you want to apply the truncation to. Can be one or more column names.

    Returns:
    :pd.DataFrame:
    '''
    try:
        for col in target_col:
            df[col] = df[col].str.split().str.slice(start = start, stop = stop).str.join(' ')
        inspector_gadget.get_log().info("truncate_column_values() successful")
    except Exception as e:
        inspector_gadget.get_log().error(f"truncate_column_values() unsuccessful, {e}")
    return df


def save_processed_data_to_csv(df, absolute_path):
    '''
    Converts a pandas DataFrame into a CSV file and stores it at the specified absolute path. The name of the newly generated
    CSV file is the last element of the absolute path. 
    ex: '/Users/bobs_laptop/Desktop/.../generated_file_name.CSV'

    Parameters:
    :df:(pd.DataFrame): The pandas DataFrame that will be converted into a CSV file.
    :absolute_path:(str): The specified absolute path where the CSV file will be stored.

    Returns:
    :None:(None):
    '''
    try:
        df.to_csv(absolute_path)
        inspector_gadget.get_log().info("save_processed_data_to_csv() successful")
    except Exception as e:
        inspector_gadget.get_log().error(f"save_processed_data_to_csv() unsuccessful, {e}")



def convert_currency(df, price_column, conversion_rate= 0):
    """
    Converts the Price column from one currency to another using a specified conversion rate.

    Parameters:
    :df:(pd.DataFrame): DataFrame containing the price column.
    :price_column:(float or int): Name of the column with prices in the original currency.
    conversion_rate (float): Conversion rate from the original currency to the target currency.

    Returns:
    :pd.DataFrame: DataFrame with an additional column for prices in the target currency.
    """
    if not isinstance(conversion_rate, (float, int)):
        raise TypeError("Conversion rate must be a float or an int.")

    df[f'{price_column}_converted'] = df[price_column] / conversion_rate
    return df

def drop_columns(df, *args):
    """
    Drop specified columns from a DataFrame.
    
    Parameters:
    :df:(pd.DataFrame): DataFrame.
    :**args: Arbitrary variable length arguments where the values represent the names of columns to drop.

    Returns:
    :pd.DataFrame: DataFrame with an additional column for prices in the target currency.
    """
    try:
        df = df.drop(columns=list(args), inplace = True)
        return df 
    except Exception as e:
        inspector_gadget.get_log().error(f"drop_columns() unsuccessful, {e}")

def rename_columns(df, **kwargs):
    '''
    rename specified columns from a DataFrame.

    Parameters:
    :df:(pd.DataFrame): DataFrame.
    :**kwargs: Arbitrary length keyword arguments where the key represent the names of columns and values are the new names of the specified columns.

    Returns:
    pd.DataFrame: DataFrame with renamed columns.
    '''

    try:
        df = df.rename(columns = kwargs, copy = False, inplace = True)
        return df
    except Exception as e:
        inspector_gadget.get_log().error(f"rename_columns() unsuccessful, {e}")





def main():
    pass


if __name__ == '__main__':
    main()
