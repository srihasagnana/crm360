import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split,cross_val_score,GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report, recall_score, f1_score
import joblib
from imblearn.over_sampling import SMOTE

response1=requests.get("http://127.0.0.1:8000/api/order/orders")
response2=requests.get("http://127.0.0.1:8000/api/customer/customers")
df1=response1.json()
df2=response2.json()
df1=pd.DataFrame(df1)
df2=pd.DataFrame(df2)

df=df1.merge(df2,on="customer_id",how="outer")

df['order_date']=pd.to_datetime(df['order_date'])
df['order_year']=df['order_date'].dt.year
df['order_month']=df['order_date'].dt.month
df['order_day']=df['order_date'].dt.day
df['doj']=pd.to_datetime(df['doj'])
df['doj_year']=df['doj'].dt.year
df['doj_month']=df['doj'].dt.month
df['first_day']=df.groupby('customer_id')['order_date'].transform('min')
df['total_orders']=df.groupby('customer_id')['qty'].transform('sum')
df['last_order']=df.groupby('customer_id')['order_date'].transform('max')
df['avg_order_value']=df.groupby('customer_id')['amount'].transform('mean')
df['tenure_days']=(pd.Timestamp.today()-df['first_day']).dt.days
df['days_since_last_order']=(pd.Timestamp.today()-df['last_order']).dt.days

df.drop(['order_date','doj','order_id','product_id','email','city','state','first_day','last_order'],axis=1,inplace=True)
categorical_cols=['status','segment']
ohe=OneHotEncoder(handle_unknown='ignore',sparse_output=False)
encoder=ohe.fit_transform(df[categorical_cols])
encoder=pd.DataFrame(encoder,columns=ohe.get_feature_names_out(categorical_cols))
df=pd.concat([df.drop(categorical_cols,axis=1),encoder],axis=1)

df['churn']=df['churn'].astype(int)
X=df.drop("churn",axis=1)
y=df["churn"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)

# use case-1(logistic and random forest)
pipeline=Pipeline([
    ('Imputer',SimpleImputer(strategy='mean')),
    ('Scaler',StandardScaler(with_mean=False)),
    ('LogisticRegression',LogisticRegression()),
])

rf_pipeline=Pipeline([
    ('Imputer',SimpleImputer(strategy='mean')),
    ('Scaler',StandardScaler(with_mean=False)),
    ('RandomForest',RandomForestClassifier(class_weight='balanced',random_state=42)),
])

# smote
imputer=SimpleImputer(strategy='mean')
X_train_imp=imputer.fit_transform(X_train)
X_test_imp=imputer.transform(X_test)
smote=SMOTE(random_state=42)
X_train_smote,y_train_smote=smote.fit_resample(X_train_imp,y_train)
rf_pipeline.fit(X_train_smote,y_train_smote)

y_predict_smote=rf_pipeline.predict(X_test_imp)
accuracy_smote=accuracy_score(y_test,y_predict_smote)
print("smote:",accuracy_smote)

pipeline.fit(X_train,y_train)
y_predict_logistic=pipeline.predict(X_test)
accuracy=accuracy_score(y_test,y_predict_logistic)
print("logistic:",accuracy)

rf_pipeline.fit(X_train,y_train)
y_predict_rf=rf_pipeline.predict(X_test)
accuracy_rf=accuracy_score(y_test,y_predict_rf)
print("random forest:",accuracy_rf)
print("smote classification score:",classification_report(y_test,y_predict_smote))
print("random forest classification score:",classification_report(y_test,y_predict_rf))

# grid_search_cv
param_grid={
    'RandomForest__n_estimators':[50,100,200],
    'RandomForest__max_depth':[5,10,None],
}

grid_pipeline=GridSearchCV(
    rf_pipeline,
    param_grid=param_grid,
    cv=5,
    scoring='f1',
)
grid_pipeline.fit(X_train,y_train)
print("grid pipeline:",grid_pipeline.best_params_)

score=cross_val_score(rf_pipeline,X_train,y_train,cv=10,scoring='accuracy')
print("cross value score:",score)

joblib.dump(rf_pipeline,'../model_trained/churn_rf.pkl')
joblib.dump(pipeline,'../model_trained/churn_lg.pkl')

row = df[df['customer_id']==3].head(1)
X_row = row.drop('churn',axis=1)

print("Actual:", row['churn'].values)
print("Prediction:", rf_pipeline.predict(X_row))
print("Probability:", rf_pipeline.predict_proba(X_row))

row = df[df['customer_id']==3].head(1)
print(row.T)


rf=rf_pipeline.named_steps['RandomForest']
importance_df=pd.DataFrame({
    "features":X.columns,
    "importance":rf.feature_importances_,
})

importance_df.to_csv('../model_trained/churn_random_forest_importance.csv',index=False)
df.to_csv("../model_trained/customer_orders.csv",index=False)

comparison_df=pd.DataFrame({
    'model':['RandomForest','LogisticRegression','random_forest_smote'],
    'accuracy':[accuracy_rf,accuracy,accuracy_smote],
    'recall':[recall_score(y_test,y_predict_rf),recall_score(y_test,y_predict_logistic),recall_score(y_test,y_predict_smote)],
    'f1_score': [f1_score(y_test, y_predict_rf), f1_score(y_test, y_predict_logistic),
               f1_score(y_test, y_predict_smote)]
})
comparison_df.to_csv('../model_trained/churn_random_forest_comparison.csv',index=False)