import streamlit as st 
import json
import requests 
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import get_directory_name
from utils.logger import Logger

cwd_path = get_directory_name('/Users/ericklopez/Desktop/ML_Powered_Credit_Card_Fraud_Detection_A_Docker_FastAPI_And_Streamlit_Approach/empirical/src/iv_frontend.py')
inspector_gadget = Logger(cwd_path)

def run():
    '''Creates front end web interface via Streamlit for client interaction'''

    st.title("Credit Card Fraud Detection Web Application")

    st.image("v_fraud_image.png")

    st.write("""## About
             Credit card fraud is a type of identity theft where someone illegally obtains and uses another person's credit card information to make unauthorized purchases or withdraw funds.
             
             **This Streamlit app leverages a Machine Learning API to detect fraudulent credit card transactions based on criteria such as transaction time, type, amount, and account balance before and after the transaction.

             **Made by Erick X Lopez**
             """)
    
    st.sidebar.header("Transaction Details to Consider")

    sender_name = st.sidebar.text_input("""Input Sender ID""")
    receiver_name = st.sidebar.text_input("""Input Receiver ID""")
    step = st.sidebar.slider("""Time Taken to Complete the Transaction (hrs):""")
    types = st.sidebar.subheader(f"""
                                 Enter Type of Transfer Made:\n\n\n\n
                                 0: For 'Cash In' Transaction\n 
                                 1: For 'Cash Out' Transaction\n 
                                 2: For 'Debit' Transaction\n
                                 3: For 'Payment' Transaction\n  
                                 4: For 'Transfer' Transaction\n""")
    types = st.sidebar.selectbox("",(0,1,2,3,4))
    x = ''
    if types == 0:
        x = 'Cash in'
    if types == 1:
        x = 'Cash Out'
    if types == 2:
        x = 'Debit'
    if types == 3:
        x = 'Payment'
    if types == 4:
        x =  'Transfer'

    amount = st.sidebar.number_input("Amount in $",min_value=0, max_value=110000)
    oldbalanceorg = st.sidebar.number_input("""Original Balance Before Transaction was made""",min_value=0, max_value=110000)
    newbalanceorg= st.sidebar.number_input("""New Balance After Transaction was made""",min_value=0, max_value=110000)
    oldbalancedest= st.sidebar.number_input("""Old Balance""",min_value=0, max_value=110000)
    newbalancedest= st.sidebar.number_input("""New Balance""",min_value=0, max_value=110000)
    isflaggedfraud = st.sidebar.selectbox("""Specify if this was flagged as Fraud by your System: """,(0,1))

    if st.button("Detection Result"):
        values = {
        "step": step,
        "types": types,
        "amount": amount,
        "oldbalanceorig": oldbalanceorg,
        "newbalanceorig": newbalanceorg,
        "oldbalancedest": oldbalancedest,
        "newbalancedest": newbalancedest,
        "isflaggedfraud": isflaggedfraud
        }

        st.write(f"""### These are the transaction details:\n
        Sender ID: {sender_name}
        Receiver ID: {receiver_name}
        1. Time Taken to Complete the Transaction (hrs): {step}\n
        2. Type of Transaction: {x}\n
        3. Amount Sent: {amount}\n
        4. Sender Previous Balance Before Transaction: {oldbalanceorg}\n
        5. Sender New Balance After Transaction: {newbalanceorg}\n
        6. Recepient Balance Before Transaction: {oldbalancedest}\n
        7. Recepient Balance After Transaction: {newbalancedest}\n
        8. System Flag Fraud Status: {isflaggedfraud}
                    """)


        response = requests.post(f"http://127.0.0.1:8000/predict",json=values)
        # json_str = json.dumps(response.json())
        resp = response.json()

        if sender_name=='' or receiver_name == '':
            st.write("Error! Please input Transaction ID or Names of Sender and Receiver!")
        else:
            st.write(f"""### The '{x}' transaction that took place between {sender_name} and {receiver_name} is {resp}.""")


def main():
    run()

if __name__ == '__main__':
    main()


