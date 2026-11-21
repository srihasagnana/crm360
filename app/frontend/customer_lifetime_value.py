import pandas as pd
import requests
import streamlit as st
import os
BACKEND_URL = os.getenv("BACKEND_URL", "https://crm360-3.onrender.com")
st.set_page_config(
    layout="wide"
)
def customer_lifetime_value_function():
    st.title("Customer lifetime value")
    responses=requests.get(f"{BACKEND_URL}/api/analytics/customer_lifetime_value")
    data=responses.json()
    data=pd.DataFrame(data)
    max_clv=data.loc[data['clv'].idxmax()]
    with st.container(border=True):
        st.metric("highest clv:",max_clv["clv"])
        st.write("customer name:",max_clv["customer_name"])

    col1,col2=st.columns(2)
    with col1:
        st.metric("total_clv",data["clv"].sum())
    with col2:
        st.metric("total_customers:",data['customer_id'].count())

    st.subheader("Customer CLV Table")
    st.dataframe(data,hide_index=True)

    st.subheader("Top Customers by CLV")
    top_n=st.slider("top n cutomers:",5,25,5)
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(x='customer_name',y='clv',data=data.nlargest(top_n,'clv'))
    with col2:
        st.write(data.nlargest(top_n,'clv'))

    labels = ["0-10K","10K-50K","50K-100K","100K+"]
    data['clv_range']=pd.cut(data['clv'],bins=4,labels=labels)
    st.subheader("Customer Distribution by CLV Range")
    st.bar_chart(x='clv_range',y='customer_id',data=data)


def customer_top10_by_revenue_func():
    st.write("top 10 customers by revenue")
    responses = requests.get("http://127.0.0.1:8000/api/analytics/customer_top10_by_revenue")
    data = responses.json()
    data = pd.DataFrame(data)
    st.dataframe(data,hide_index=True)
