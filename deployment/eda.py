import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
import numpy as np

st.set_page_config(
    page_title='Telco Customer Churn - EDA',
    layout='wide',
    initial_sidebar_state='expanded'
)

def run():
    # Membuat Title
    st.title('Telco Customer Churn Prediction')

    # Menambahkan Gambar
    image = Image.open('telco.png')
    st.image(image,width=800)

    # Membuat Garis Lurus
    st.markdown('---')

    # Magic Syntax
    '''
    PT. Telcom merupakan perusahaan yang memiliki produk dan layanan berupa telepon, internet, keamanan online, pencadangan online, perlindungan perangkat, dukungan teknis, serta streaming TV dan film. Dalam menghadapi kompetisi layanan dipasar, perusahaan perlu mengetahui prilaku dari pelanggannya yang telah berlangganan dan bagaimana dapat mempertahankan pelanggan.
    Customer churn didefinisikan sebagai ketika pelanggan berhenti berlayanan dengan perusahaan. Pelanggan di industri telekomunikasi memiliki sejumlah penyedia layanan untuk dipilih dan dapat secara aktif beralih dari satu ke yang berikutnya. Di sektor yang sangat kompetitif ini, industri telekomunikasi memiliki tingkat churn tahunan 15-25%. Penghentian pelanggan di industri telekomunikasi menimbulkan salah satu risiko paling signifikan terhadap hilangnya pendapatan. Karena biaya untuk memperoleh pelanggan baru mencapai 25 kali lebih tinggi daripada biaya untuk mempertahankan mereka, memupuk loyalitas pelanggan adalah kuncinya.
    '''

    st.write('### Dataset')

    # Show DataFrame
    data = pd.read_csv('https://raw.githubusercontent.com/garasense/Hacktv8-Challenge-1-SQL/main/Telco-Customer-Churn.csv')
    st.dataframe(data)
    data.TotalCharges = pd.to_numeric(data.TotalCharges, errors='coerce')

    st.write('#### Churn')
    fig = plt.figure(figsize=(10,4))
    sns.set(style='darkgrid')
    sns.countplot(data=data, x='Churn')
    st.pyplot(fig)
    st.markdown('---')

    st.write('#### Plot Total Charges With Churn')
    fig = plt.figure(figsize=(18,7))
    sns.set(style='darkgrid')
    plt.subplot(1,2,1)
    sns.histplot(data=data, x='TotalCharges', hue='Churn', kde=True)
    plt.subplot(1,2,2)
    data.groupby('Churn')['TotalCharges'].sum().plot(kind ='pie', autopct = '%1.2f%%')
    st.pyplot(fig)
    st.markdown('---')

    # Membuat Histogram
    st.write('#### Histogram of Tenure')
    fig = plt.figure(figsize=(8, 4))
    plt.xlabel("Tenure")
    plt.ylabel("Jumlah Pelanggan")
    plt.title("Customer Churn")
    sns.histplot(data=data, x='tenure', hue='Churn', alpha=1, kde=True)
    st.pyplot(fig)
    st.markdown('---')

    no_churn = data.groupby(['Churn','tenure']).count().transpose()['No']
    yes_churn = data.groupby(['Churn','tenure']).count().transpose()['Yes']
    churn_rate = 100 * yes_churn / (no_churn+yes_churn)

    st.write('#### Churn Percentage by Tenure')
    fig = plt.figure(figsize=(8,4), dpi=150)
    churn_rate.iloc[0].plot(kind='line')
    plt.ylabel('Churn Percentage');
    st.pyplot(fig)
    st.markdown('---')

    def segment_tenure(tenure):
        if tenure < 13:
            return '0-12 Months'
        elif tenure < 25:
            return '12-24 Months'
        elif tenure < 49:
            return '24-48 Months'
        else:
            return "Over 48 Months"

    data['segment_tenure'] = data['tenure'].apply(segment_tenure)

    st.write('#### Churn by Months')
    fig = plt.figure(figsize=(10,4),dpi=150)
    sns.scatterplot(data=data,x='MonthlyCharges',y='TotalCharges',hue='segment_tenure', linewidth=0.5,alpha=0.5,palette='Dark2')
    st.pyplot(fig)
    fig = plt.figure(figsize=(10,4),dpi=120)
    sns.countplot(data=data, x='segment_tenure', hue='Churn')
    st.pyplot(fig)

    st.markdown('---')
    col1, col2 = st.columns(2)
    
    with col1:
        st.write('#### Barplot')
        pilihan = st.selectbox('Select: ', ('gender', 'SeniorCitizen', 'Partner', 'Dependents', 
        'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
        'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling','PaymentMethod'))
        fig = plt.figure(figsize=(8, 5))
        sns.countplot(data=data, x=data[pilihan], hue="Churn")
        st.pyplot(fig)

    with col2:
        st.write('#### Pie Plot')
        fig = plt.figure(figsize=(6, 4))
        data[pilihan].value_counts().plot(kind ='pie', autopct = '%1.2f%%', fontsize=6)
        st.pyplot(fig)