import joblib
import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

def revenue_forecast():
    st.title("Next Month Revenue Forecast")

    if st.button("predict next month revenue"):
        response1=requests.get("http://127.0.0.1:8000/api/order/orders")
        df=response1.json()
        df=pd.DataFrame(df)

        print(df.columns)

        df['order_date']=pd.to_datetime(df['order_date'])
        df['year_month']=df['order_date'].dt.to_period('M')
        monthly_df=df.groupby('year_month').agg({
            'qty':'sum',
            'amount':'sum',
            'order_id':'count'
        }).reset_index()

        monthly_df['lag_1']=monthly_df['amount'].shift(1)
        monthly_df['lag_2']=monthly_df['amount'].shift(2)
        monthly_df['lag_3']=monthly_df['amount'].shift(3)

        monthly_df['rolling_mean']=monthly_df['amount'].rolling(3).mean()
        monthly_df.dropna(inplace=True)
        monthly_df.drop('year_month',axis=1,inplace=True)

        x_new=monthly_df.drop("amount",axis=1).tail(1)
        model=joblib.load('app/model_trained/revenue_forest.pkl')
        prediction=model.predict(x_new)

        last_month=monthly_df['amount'].tail(1).values[0]
        col1,col2=st.columns(2)
        with col1:
            st.metric("last month revenue",last_month)
        with col2:
            st.metric("forecast revenue",prediction)

        change_pct=(abs(prediction-last_month)/last_month) * 100
        if last_month>prediction:
            st.success(f"Revenue Expected to Decrease by {change_pct}")
        else:
            st.success(f"Revenue Expected to Increase by {change_pct}")

        st.header("Recent Revenue History")
        st.dataframe(monthly_df)

