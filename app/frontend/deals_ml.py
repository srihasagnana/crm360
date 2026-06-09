import streamlit as st
import joblib
import pandas as pd


def deals_model_func():
    with st.form("deals form"):
        customer_id=st.number_input("Customer ID")
        value=st.number_input("Value")
        annual_spend=st.number_input("Annual Spending")
        churn=st.number_input("Churn")
        created_date=st.date_input("Created Date")
        closed_date=st.date_input("Closed Date")
        doj_date=st.date_input("DOJ Date")
        customer_tenure_days=st.number_input("Customer Tenure Days")
        deals_duration=st.number_input("Deals Duration")
        state=st.selectbox("State",['Gj','Tn','Mh','Ka','Rj','Ts','Dl','Ap'])
        segment = st.selectbox("Segment", ['Individual', 'SMB', 'Startup', 'Enterprise'])
        channel=st.selectbox("channel",['WhatsApp','Phone','Email'])
        type=st.selectbox("type",['Meeting','Call','Email'])
        outcome=st.selectbox("Outcome",['Positive','Negative','Neutral'])
        interaction_date=st.date_input("Interaction Date")
        submit=st.form_submit_button("Submit")

    if submit:
        doj_year=doj_date.year
        doj_month=doj_date.month
        created_date_year=created_date.year
        created_date_month=created_date.month
        closed_date_year=closed_date.year
        closed_date_month=closed_date.month
        interaction_date_year=interaction_date.year
        interaction_date_month=interaction_date.month

        input_df=pd.DataFrame({
            'customer_id':[customer_id],
            'value':[value],
            'annual_spend':[annual_spend],
            'doj_year':[doj_year],
            'doj_month':[doj_month],
            'created_date_year':[created_date_year],
            'created_date_month':[created_date_month],
            'closed_date_year':[closed_date_year],
            'closed_date_month':[closed_date_month],
            'interaction_date_year':[interaction_date_year],
            'interaction_date_month':[interaction_date_month],
            'churn':[churn],
            'segment':[segment],
            'channel':[channel],
            'type':[type],
            'outcome':[outcome],
            'customer_tenure_days':[customer_tenure_days],
            'deals_duration':[deals_duration],
            'state':[state],
        })

        input_df['state_Ap']=0
        input_df['state_Dl']=0
        input_df['state_Gj']=0
        input_df['state_Ka']=0
        input_df['state_Mh']=0
        input_df['state_Rj']=0
        input_df['state_Tn']=0
        input_df['state_Ts']=0
        input_df[f'state_{state}']=1

        input_df['segment_Enterprise'] = 0
        input_df['segment_SMB'] = 0
        input_df['segment_Startup'] = 0
        input_df['segment_Individual'] = 0
        input_df[f'segment_{segment}'] = 1

        input_df['channel_Email'] = 0
        input_df['channel_Phone'] = 0
        input_df['channel_WhatsApp'] = 0
        input_df[f'channel_{channel}'] = 1

        input_df['type_Call'] = 0
        input_df['type_Meeting'] = 0
        input_df['type_Email'] = 0
        input_df[f'type_{type}'] = 1

        input_df['outcome_Negative'] = 0
        input_df['outcome_Neutral'] = 0
        input_df['outcome_Positive'] = 0
        input_df[f'outcome_{outcome}'] = 1

        input_df.drop(['state','segment','channel','type','outcome'],axis=1,inplace=True)

        expected_columns=['customer_id',  'value', 'annual_spend', 'churn',
       'created_date_year', 'created_date_month', 'closed_date_year',
       'closed_date_month', 'doj_year', 'doj_month', 'interaction_date_year',
       'interaction_date_month', 'customer_tenure_days', 'deals_duration',
       'state_Ap', 'state_Dl', 'state_Gj', 'state_Ka', 'state_Mh', 'state_Rj',
       'state_Tn', 'state_Ts', 'segment_Enterprise', 'segment_Individual',
       'segment_SMB', 'segment_Startup', 'channel_Email', 'channel_Phone',
       'channel_WhatsApp', 'type_Call', 'type_Email', 'type_Meeting',
       'outcome_Negative', 'outcome_Neutral', 'outcome_Positive']

        input_df=input_df[expected_columns]
        model=joblib.load('app/model_trained/deals_model.pkl')
        pred=model.predict(input_df)
        prob=model.predict_proba(input_df)

        st.write(prob)
        st.write(pred)