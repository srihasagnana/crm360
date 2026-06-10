import pandas as pd
import streamlit as st

def ab_test_func():
    st.header("A/B Testing Analysis")
    df=pd.read_csv('app/model_trained/ab_testing.csv')
    st.dataframe(df)

    max_ab=df.loc[df['avg annual spend'].idxmax()]
    with st.container(border=True):
        st.metric("max value:",max_ab['avg annual spend'])
        st.write(max_ab['group'])
    st.bar_chart(df.set_index('group'))