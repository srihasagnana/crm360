import requests
import streamlit as st
import pandas as pd
import joblib

def churn_model():
    st.title("Churn Prediction")
    with st.form("user_form"):
        customer_id=st.number_input("Customer ID")
        amount=st.number_input("Amount")
        qty=st.number_input("Quantity")
        status=st.selectbox("Status",['Delivered','Cancelled','Pending'])
        segment=st.selectbox("Segment",['Individual','SMB','Startup','Enterprise'])
        annual_spend=st.number_input("Annual Spend")
        doj=st.date_input("DoJ")
        order=st.date_input("Order")
        total_orders = st.number_input("Total Orders")
        avg_order_value = st.number_input("Average Order Value")
        tenure_days = st.number_input("Tenure Days")
        days_since_last_order = st.number_input("Days Since Last Order")
        submit=st.form_submit_button("Submit")

    if submit:
        doj_year=doj.year
        doj_month=doj.month
        order_year=order.year
        order_month=order.month
        order_day=order.day

        input_df=pd.DataFrame({
            'customer_id':[customer_id],
            'qty':[qty],
            'amount':[amount],
            'status':[status],
            'segment':[segment],
            'annual_spend':[annual_spend],
            'doj_year':[doj_year],
            'doj_month':[doj_month],
            'order_year':[order_year],
            'order_month':[order_month],
            'order_day':[order_day],
            'total_orders': [total_orders],
            'avg_order_value': [avg_order_value],
            'tenure_days': [tenure_days],
            'days_since_last_order': [days_since_last_order],
            }
        )
        input_df['status_Cancelled']=0
        input_df['status_Pending']=0
        input_df['status_Delivered']=0
        input_df['status_nan']=0
        input_df[f'status_{status}']=1

        input_df['segment_Enterprise']=0
        input_df['segment_SMB']=0
        input_df['segment_Startup']=0
        input_df['segment_Individual']=0
        input_df[f'segment_{segment}']=1

        input_df.drop(['status','segment'],axis=1,inplace=True)
        st.write(input_df)
        expected_cols = ['customer_id','qty', 'amount', 'annual_spend', 'order_year', 'order_month', 'order_day',
                         'doj_year', 'doj_month', 'total_orders', 'avg_order_value', 'tenure_days',
                         'days_since_last_order', 'status_Cancelled', 'status_Delivered', 'status_Pending',
                         'status_nan', 'segment_Enterprise', 'segment_Individual', 'segment_SMB',
                         'segment_Startup'
        ]
        input_df = input_df[expected_cols]
        model=joblib.load('app/model_trained/churn_rf.pkl')
        prediction=model.predict(input_df)
        prob = model.predict_proba(input_df)

        st.write(prob)
        st.write(prediction)

        # threshold prob
        if prob[0][1]<0.35:
            st.success('low risk')
            risk='low'
        elif prob[0][1]<0.7:
            st.warning("medium risk")
            risk='medium'
        else:
            st.error("high risk")
            risk='high'

        response1 = requests.get("http://127.0.0.1:8000/api/order/orders")
        response2 = requests.get("http://127.0.0.1:8000/api/customer/customers")
        df1 = response1.json()
        df2 = response2.json()
        df1 = pd.DataFrame(df1)
        df2 = pd.DataFrame(df2)

        df = df1.merge(df2, on="customer_id", how="outer")
        customer_df=[]
        for data in df:
            customer_df.append({
                'customer_id':data[0],
                'risk':model.predict_proba(df[data[0]])[0][1],
            })
        risk_df=pd.DataFrame(customer_df)
        st.dataframe(risk_df)