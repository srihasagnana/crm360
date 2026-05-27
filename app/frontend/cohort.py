import pandas as pd
import requests
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def cohort_retention_matrix_func():
    responses = requests.get("http://127.0.0.1:8000/api/analytics/cohort_retention_matrix")
    data=responses.json()
    data=pd.DataFrame(data)
    st.title("Cohort Retention Matrix")
    st.dataframe(data)
    heatmap_data=data.set_index('cohort_month')
    fig,ax=plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data,annot=True)
    st.pyplot(fig)