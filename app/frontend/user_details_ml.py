import plt
import streamlit as st
import pandas as pd
import joblib

def churn_model():
    st.header("RFM scoring and segment labeling")
    df = pd.read_csv("app/model_trained/customer_orders.csv")
    df=df.groupby('customer_id').agg({
        'total_orders':'sum',
        'amount':'sum',
        'tenure_days':'first',
        'churn':'first',
        'days_since_last_order':'first',
        'annual_spend':'first'
    }).reset_index()

    df['r_score']=pd.qcut(df['days_since_last_order'],5,labels=[5,4,3,2,1])
    df['f_score']=pd.qcut(df['total_orders'],5,labels=[1,2,3,4,5],duplicates='drop')
    df['m_score']=pd.qcut(df['amount'],5,labels=[1,2,3,4,5])


    def seg(row):
        if row['r_score']>4 and row['f_score']>4 and row['m_score']>4:
            return "Champions"
        else:
            return "At Risk"

    df['segment_name']=df.apply(seg,axis=1)

    st.write(df)
    st.bar_chart(df['segment_name'].value_counts())
    st.header("Churn Prediction")
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
        elif prob[0][1]<0.7:
            st.warning("medium risk")
        else:
            st.error("high risk")


        importance_df=pd.read_csv('app/model_trained/churn_random_forest_importance.csv')
        importance_df = importance_df.sort_values('importance', ascending=False)
        top_features = importance_df.head(10)
        st.dataframe(top_features)

        fig,ax=plt.subplots(figsize=(8,5))
        ax.barh(top_features['features'],top_features['importance'])
        ax.set_title("Top 10 Churn Drivers")
        ax.set_xlabel("Importance")
        ax.set_ylabel("Features")
        st.pyplot(fig)

