import os
import sys
from urllib.request import urlopen
import urllib.request
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import get_directory_name
from utils.logger import Logger

cwd_path = get_directory_name('/Users/ericklopez/Desktop/ML_Powered_Credit_Card_Fraud_Detection_A_Docker_FastAPI_And_Streamlit_Approach/empirical/src/i_staging_raw_data.py')
inspector_gadget = Logger(cwd_path)

 
def download_data_from_url(url:str, absolute_path:str, target_dir:str) -> None:
    '''
    Fetches data from specified url and saves it to specified absolute path.

    Parameters:
    :url:(str): The specified web url where data is located.
    :absolute_path:(str): The absolute path where the fetched data will be stored.
    :target_dir:(str): The absolute path where the CSV file will be stored, including the desired filename for the CSV. Format should be '/path/to/save/specified_file_name.csv'


    Return:
    :None:
    '''
    if not os.path.exists(str(absolute_path)):
        os.makedirs(str(absolute_path))
    
    try:
        urllib.request.urlretrieve(url, target_dir) #used to download a file from the internet and save it to a specified location on your local file system.
        inspector_gadget.get_log().info(f'download_data_from_url() successful. Data downloaded to {absolute_path}')
        

    except Exception as e:
        inspector_gadget.get_log().error(f'download_data_from_url() unsuccessful,{e}. Make sure you provide the absolute path for parameters absolute_path and target_dir.')
        traceback.print_exc()




def main():
    pass





if __name__ == '__main__':
    main()