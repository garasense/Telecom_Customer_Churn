import streamlit as st
import eda
import backend

navigation = st.sidebar.selectbox('Select Page : ', ('EDA', 'Predict A Customer'))

if navigation == 'EDA':
    eda.run()
else:
    backend.run()