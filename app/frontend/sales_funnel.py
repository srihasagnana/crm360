import requests
import streamlit as st
import pandas as pd
import plotly.express as px

def sales_funnel_func():
    responses=requests.get("http://127.0.0.1:8000/api/analytics/sales_funnel_rate")
    data=responses.json()
    data=pd.DataFrame(data)
    st.title("Sales Funnel Stage Data")
    st.dataframe(data,hide_index=True)
    col1,col2=st.columns(2)
    with col1:
        st.subheader("Sales Funnel Distribution")
        fig=px.pie(data,values='deal count',names='stage')
        st.plotly_chart(fig)
    with col2:
        st.subheader("Stage-wise Deal Count")
        st.bar_chart(x='stage',y='deal count',data=data)

def deal_stage_velocity_func():
    responses = requests.get("http://127.0.0.1:8000/api/analytics/deal_stage_velocity")
    data = responses.json()
    data = pd.DataFrame(data)
    col1, col2 = st.columns(2)
    with col1:
        highest_stage = data.loc[data['avg_days'].idxmax()]
        st.metric("Slowest Stage",highest_stage['stage'])
        st.write(f"Avg Days: {highest_stage['avg_days']}")
    with col2:
        fastest_stage  = data.loc[data['avg_days'].idxmin()]
        st.metric("Fastest Stage", fastest_stage ['stage'])
        st.write(f"Avg Days: {fastest_stage['avg_days']}")
    st.subheader("Deal Stage Velocity Data")
    st.dataframe(data, hide_index=True)
