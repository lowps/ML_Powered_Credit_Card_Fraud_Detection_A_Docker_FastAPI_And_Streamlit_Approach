import os
import sys
from fastapi import FastAPI, File, Query, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, PlainTextResponse
import uvicorn
import joblib
import numpy as np
from pydantic import BaseModel
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import get_directory_name
from utils.logger import Logger

cwd_path = get_directory_name('/Users/ericklopez/Desktop/ML_Powered_Credit_Card_Fraud_Detection_A_Docker_FastAPI_And_Streamlit_Approach/empirical/src/iii_backend.py')
inspector_gadget = Logger(cwd_path)

file_path = '/Users/ericklopez/Desktop/ML_Powered_Credit_Card_Fraud_Detection_A_Docker_FastAPI_And_Streamlit_Approach/empirical/data/final/RandomForestClassifier.pkl'



app = FastAPI(
    title = "Credit Card Detection via Random Forest Classifier API",
    description = '''Developed an API that leverages a Machine Learning model to detect fraudulent credit card transactions. The model analyzes features such as transaction time, amount, transaction type, etc to determine the likelihood of fraud.''',
    version = '1.0.0',
    debug = True
    )

try:
    model = joblib.load(file_path)
    inspector_gadget.get_log().info("Succesfully loaded Random Forest Classifier model")
except Exception as e:
    if not os.path.isfile(file_path):
        inspector_gadget.get_log().error("Random Forest Classifier model not found. The model at {file_path} does not exist. {e}")
        raise FileNotFoundError({e})
    

@app.get("/", response_class=PlainTextResponse)
async def running():
    note = '''
    Credit Card Fraud Detection API  🙌🏻

    Note: test, test, test
    
    '''
    return note

class FraudDetection(BaseModel):
    step:int
    types:int
    amount:float
    oldbalanceorig:float
    newbalanceorig:float
    oldbalancedest:float
    newbalancedest:float
    isflaggedfraud:float

def predict(data: FraudDetection):

    features = np.array([[data.step, data.types, data.amount, data.oldbalanceorig, data.newbalanceorig, data.oldbalancedest, data.newbalancedest, data.isflaggedfraud]])
    model = joblib.load(file_path)

    predictions = model.predict(features)
    if predictions == 1:
        return{"Fraudulent"}
    elif predictions == 0:
        return {"Not Fraudulent"}
    


def main():
    uvicorn.run("iii_backend:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == '__main__':
    main()





    
    
    

    