import joblib
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import requests
import pandas as pd

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

X=monthly_df.drop("amount",axis=1)
y=monthly_df["amount"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)

# ridge regression
pipeline_ridge=Pipeline([
    ('Imputer',SimpleImputer(strategy='mean')),
    ('Scaler',StandardScaler(with_mean=False)),
    ('Ridge',RidgeCV(alphas=[0.1,0.5,10,100])),
])

pipeline_ridge.fit(X_train,y_train)
y_predict_ridge=pipeline_ridge.predict(X_test)
print("Ridge prediction:",y_predict_ridge)
print("mae:",mean_absolute_error(y_test,y_predict_ridge))
error=abs(y_test-y_predict_ridge)/y_test

result=pd.DataFrame({
    'actual':y_test,
    'predicted':y_predict_ridge,
    'error':error
})
print('result error:',result)

joblib.dump(pipeline_ridge,'../model_trained/revenue_forest.pkl')