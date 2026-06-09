import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def customer_segmentation():
    st.header("Customer Segmentation Dashboard")
    df=pd.read_csv("app/model_trained/customer_segments.csv")
    st.subheader("Cluster Distribution")
    st.bar_chart(df['cluster'].value_counts())

    st.write(df['cluster'].value_counts())

    scaler=joblib.load("app/model_trained/customer_scaler.pkl")
    kmeans=joblib.load("app/model_trained/customer_segmentation.pkl")
    pca=joblib.load("app/model_trained/customer_pca.pkl")
    X = df.drop(["customer_id","cluster"], axis=1)
    X_scaled=scaler.transform(X)
    clusters = kmeans.predict(X_scaled)
    pca_data=pca.transform(X_scaled)
    st.subheader("PCA Cluster Visualization")
    fig, ax = plt.subplots(figsize=(6,4))
    ax.scatter(pca_data[:,0],pca_data[:,1],c=clusters)
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    st.pyplot(fig)
