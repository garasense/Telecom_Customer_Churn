import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
import numpy as np
import joblib
import json
import tensorflow

# Load All Files
with open('final_pipeline.pkl', 'rb') as file_1:
  model_pipeline = joblib.load(file_1)

from tensorflow.keras.models import load_model
model_ann = load_model('customer_churn_model.h5')

def run():
    # Membuat Title
    st.title('Telco Customer Churn Prediction')

    # Menambahkan Gambar
    image = Image.open('telco.png')
    st.image(image,width=800)

    col1, col2= st.columns(2)
    with st.form(key='form_parameters'):
    
        with col1:
            st.header("Customer Information")
            customerid = st.text_input('customerID', value='')
            tenure = st.number_input('tenure', min_value=0, max_value=500, value=1)
            monthlycharges = st.number_input('MonthlyCharges', min_value=0, max_value=100000, value=0)
            totalcharges = st.number_input('TotalCharges', min_value=0, max_value=100000, value=0)
            st.markdown('---')
            st.header("Services")
            phoneservice = st.selectbox('PhoneService', ('Yes', 'No'), index=1)
            multiplelines = st.selectbox('MultipleLines', ('Yes', 'No', 'No Phone'), index=1)
            internetservice = st.selectbox('InternetService', ('DSL', 'Fiber Optic', 'No'), index=1)
            onlinesecurity = st.selectbox('OnlineSecurity', ('Yes', 'No', 'No Internet'), index=1)
            st.markdown('---')
            streamingmovie = st.selectbox('StreamingMovies', ('Yes', 'No', 'No Internet'), index=1)
            contract = st.selectbox('Contract', ('Monthly', '2 Year', '1 Year'), index=1)
            st.markdown('---')


        with col2:
            st.header("-")
            gender = st.selectbox('gender', ('Male', 'Female'), index=1)
            seniorcitizen = st.selectbox('SeniorCitizen', ('0', '1'), index=1)
            partner = st.selectbox('Partner', ('Yes', 'No'), index=1)
            dependents = st.selectbox('Dependents', ('Yes', 'No'), index=1)
            st.markdown('---')
            st.header("-")
            onlinebackup = st.selectbox('OnlineBackup', ('Yes', 'No', 'No Internet'), index=1)
            deviceprotection = st.selectbox('DeviceProtection', ('Yes', 'No', 'No Internet'), index=1)
            techsupport = st.selectbox('TechSupport', ('Yes', 'No', 'No Internet'), index=1)
            streamingtv = st.selectbox('StreamingTV', ('Yes', 'No', 'No Internet'), index=1)
            st.markdown('---')
            paperlessbilling = st.selectbox('PaperLessBilling', ('Yes', 'No'), index=1)
            paymentmethod = st.selectbox('PaymentMethod', ('Electronic Check', 'Credit Card', 'Bak Transfer', 'Mailed Check'), index=1)
            st.markdown('---')

        submitted = st.form_submit_button('Predict')

        data_inf = {
            'customerid' : customerid,
            'tenure' : tenure,
            'monthlycharges' : monthlycharges,
            'totalcharges' : totalcharges,
            'phoneservice' : phoneservice,
            'multiplelines' : multiplelines,
            'internetservice' : internetservice,
            'onlinesecurity' : onlinesecurity,
            'streamingmovies' : streamingmovie,
            'contract' : contract,
            'gender' : gender,
            'seniorcitizen' : seniorcitizen,
            'partner' : partner,
            'dependents' : dependents,
            'onlinebackup': onlinebackup,
            'deviceprotection' : deviceprotection,
            'techsupport' : techsupport,
            'streamingtv' : streamingtv,
            'paperlessbilling' : paperlessbilling,
            'paymentmethod' : paymentmethod
        }

        data_inf = pd.DataFrame([data_inf])
        st.dataframe(data_inf)

        if submitted:

            data_inf_transform = model_pipeline.transform(data_inf)
            y_pred_inf = model_ann.predict(data_inf_transform)
            y_pred_inf = np.where(y_pred_inf >= 0.5, 1, 0)
            st.write('# Churn :', np.where(y_pred_inf = 0, "No", "Yes"))

if __name__ == '__main__':
    run()