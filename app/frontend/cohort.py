import pandas as pd
import requests
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import os
BACKEND_URL = os.getenv("BACKEND_URL", "https://crm360-3.onrender.com")

def cohort_retention_matrix_func():
    responses = requests.get(f"{BACKEND_URL}/api/analytics/cohort_retention_matrix")
    data=responses.json()
    data=pd.DataFrame(data)
    st.title("Cohort Retention Matrix")
    st.dataframe(data)
    heatmap_data=data.set_index('cohort_month')
    fig,ax=plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data,annot=True)
    st.pyplot(fig)
