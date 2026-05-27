import streamlit as st
import pandas as pd
import requests
import calendar
import plotly.express as px

def monthly_revenue():
    responses=requests.get("http://127.0.0.1:8000/api/analytics/monthly_revenue")
    data=responses.json()
    data=pd.DataFrame(data)
    data['month']=data['month'].apply(lambda x: calendar.month_name[x])
    st.title("Monthly Revenue")
    col1,col2=st.columns(2)
    with col1:
        st.metric("Total Revenue",data['total_revenue'].sum())
    with col2:
        st.metric("Total orders",data['total_orders'].sum())

    with st.container(border=True):
        max_revenue_row=data.loc[data['total_revenue'].idxmax()]
        st.metric("highest revenue:",max_revenue_row['total_revenue'])
        st.write(f"month:{max_revenue_row['month']}")

    st.dataframe(data,hide_index=True)
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(x='month',y='total_revenue',data=data)
    with col2:
        st.bar_chart(x='month',y='total_orders',data=data)

def aov_func():
    responses = requests.get("http://127.0.0.1:8000/api/analytics/aov")
    data = responses.json()
    data = pd.DataFrame(data)
    highest_aov=data.loc[data['aov'].idxmax()]
    st.subheader("Key Performance Indicators")
    with st.container(border=True):
        st.metric("highest aov",highest_aov['aov'])
        st.write(f"month:{highest_aov['order_month']}")
    data['order_month']=data['order_month'].apply(lambda x: calendar.month_name[x])
    st.subheader("Monthly Average Order Value Data")
    st.dataframe(data,hide_index=True)
    st.subheader("Average Order Value Trend")
    st.line_chart(x='order_month',y='aov',data=data)

def region_product_func():
    st.title("Region Product Analysis Dashboard")
    responses = requests.get("http://127.0.0.1:8000/api/analytics/region_product")
    data = responses.json()
    data = pd.DataFrame(data)
    st.subheader("Top Cities by Product Category")
    col1,col2,col3=st.columns(3)
    with col1:
        highest_hardware = data.loc[data['hardware'].idxmax()]
        with st.container(border=True):
            st.metric("highest hardware",highest_hardware['hardware'])
            st.write(f"city:{highest_hardware['city']}")
    with col2:
        highest_software = data.loc[data['software'].idxmax()]
        with st.container(border=True):
            st.metric("highest software", highest_software['software'])
            st.write(f"city:{highest_software['city']}")
    with col3:
        highest_services = data.loc[data['service'].idxmax()]
        with st.container(border=True):
            st.metric("highest service", highest_services['service'])
            st.write(f"city:{highest_services['city']}")
    st.subheader("Region-wise Product Revenue Table")
    st.dataframe(data,hide_index=True)
    st.subheader("Interactive Product Sector Analysis")
    top_n=st.slider("top n cities",5,25,5)
    data['total']=data['hardware']+data['software']+data['service']
    top_cities=data.nlargest(top_n,'total')


    pg=st.selectbox("all sectors",['all',"hardware",'software','service'])
    if pg=='all':
        st.write(top_cities)
        fig = px.bar(top_cities, x='city', y=['hardware', 'software', 'service'], barmode='group')
        st.plotly_chart(fig)
    if pg == 'hardware':
        st.dataframe(top_cities[['city','hardware']],hide_index=True)
        fig = px.bar(top_cities, x='city', y='hardware', barmode='group')
        st.plotly_chart(fig)
    if pg == 'software':
        st.dataframe(top_cities[['city','software']],hide_index=True)
        fig = px.bar(top_cities, x='city', y='software', barmode='group')
        st.plotly_chart(fig)
    if pg == 'service':
        st.dataframe(top_cities[['city','service']],hide_index=True)
        fig = px.bar(top_cities, x='city', y='service', barmode='group')
        st.plotly_chart(fig)

