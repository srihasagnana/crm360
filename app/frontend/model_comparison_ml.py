import pandas as pd
import streamlit as st

def churn_model_comparison():
    st.subheader("Accuracy, Recall and F1 Score Comparison")
    df=pd.read_csv("app/model_trained/churn_random_forest_comparison.csv")
    st.dataframe(df)
    st.bar_chart(df.set_index('model'))