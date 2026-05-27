import calendar
import pandas as pd
import requests
import streamlit as st
import plotly.express as px

def seasonal_demand_index_func():
    st.title("Seasonal Demand Index")
    responses = requests.get("http://127.0.0.1:8000/api/analytics/monthly_revenue")
    data = responses.json()
    data = pd.DataFrame(data)
    data['month']=data['month'].apply(lambda x:calendar.month_name[x])

    highest_month=data.loc[data['total_revenue'].idxmax()]
    lowest_month=data.loc[data['total_revenue'].idxmin()]

    col1,col2=st.columns(2)
    with col1:
        with st.container(border=True):
            st.metric("Highest Demand Month",highest_month['month'])
            st.write(f"Revenue: {highest_month['total_revenue']}")
    with col2:
        with st.container(border=True):
            st.metric("Lowest Demand Month",lowest_month['month'])
            st.write(f"Revenue: {lowest_month['total_revenue']:,.0f}")
    st.dataframe(data)
    st.subheader("Seasonal Revenue Data")
    st.dataframe(data,hide_index=True,use_container_width=True)
    st.subheader("Monthly Seasonal Revenue Trend")
    fig = px.line(data,x='month',y='total_revenue',markers=True,title='Seasonal Demand Trend')
    st.plotly_chart(fig)
    st.subheader("Monthly Revenue Comparison")
    fig2 = px.bar(data,x='month',y='total_revenue',title='Monthly Demand Comparison')

    st.plotly_chart(fig2)