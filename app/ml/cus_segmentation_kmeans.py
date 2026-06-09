import joblib
import matplotlib.pyplot as plt
import pandas as pd
import requests
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder

response1=requests.get("http://127.0.0.1:8000/api/deal/deals")
response2=requests.get("http://127.0.0.1:8000/api/customer/customers")
response3=requests.get("http://127.0.0.1:8000/api/interaction/interactions")
response4=requests.get("http://127.0.0.1:8000/api/contact/contacts")
response5=requests.get("http://127.0.0.1:8000/api/order/orders")
df1=response1.json()
df2=response2.json()
df3=response3.json()
df4=response4.json()
df5=response5.json()
df1=pd.DataFrame(df1)
df2=pd.DataFrame(df2)
df3=pd.DataFrame(df3)
df4=pd.DataFrame(df4)
df5=pd.DataFrame(df5)
deals=df1.groupby("customer_id").agg({
    'value':'sum',
    'stage':'count'
}).reset_index()
deals.columns = ['customer_id','total_deal_value','deal_count']
interaction=df3.groupby("customer_id").agg({
    'type':'count',
    'channel':'count',
    'outcome':'count'
}).reset_index()
interaction.columns = ['customer_id','interaction_type_count','interaction_channel_count','interaction_outcome_count']

contact=df4.groupby("customer_id").agg({
    'preferred_channel':'count',
}).reset_index()
contact.columns = ['customer_id','contact_count']

order=df5.groupby("customer_id").agg({
    'qty':'sum',
    'amount':'sum',
    'status':'count'
}).reset_index()
order.columns = ['customer_id','total_qty','total_amount','order_count']

df2=df2.merge(deals,on='customer_id',how='left')\
    .merge(interaction,on='customer_id',how='left')\
    .merge(contact, on='customer_id', how='left')\
    .merge(order, on='customer_id', how='left')

df=pd.DataFrame(df2)
print(df.columns)

df['doj']=pd.to_datetime(df['doj'])
df['doj_year']=df['doj'].dt.year
df['doj_month']=df['doj'].dt.month

df['avg_order_value'] = df['total_amount'] / df['order_count']
df['deal_value_per_deal'] = df['total_deal_value'] / df['deal_count']

df=df.drop(['doj','email'],axis=1)
categorical_col=['city', 'state', 'segment','churn']

ohe=OneHotEncoder(handle_unknown='ignore')
encoded=ohe.fit_transform(df[categorical_col])
encoded=pd.DataFrame(encoded.toarray(),columns=ohe.get_feature_names_out(categorical_col))
df=pd.concat([df.drop(categorical_col,axis=1),encoded],axis=1)
df.fillna(0, inplace=True)
X=df.drop('customer_id',axis=1)
scaler=StandardScaler()
X_scaled=scaler.fit_transform(X)

wcss=[]
for i in range(1,10):
    kmeans=KMeans(n_clusters=i,random_state=7)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(1,10),wcss)
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans=KMeans(n_clusters=2)
clusters=kmeans.fit_predict(X_scaled)
print(clusters)

print(silhouette_score(X_scaled,clusters))

plt.figure(figsize=(8,6))
pca=PCA(n_components=2)
pca.fit_transform(X_scaled)
plt.scatter(X_scaled[:,0],X_scaled[:,1],c=clusters)
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.show()

joblib.dump(kmeans,"../model_trained/customer_segmentation.pkl")
joblib.dump(scaler,"../model_trained/customer_scaler.pkl")
joblib.dump(pca,"../model_trained/customer_pca.pkl")

df['cluster']=clusters

df.to_csv("../model_trained/customer_segments.csv",index=False)