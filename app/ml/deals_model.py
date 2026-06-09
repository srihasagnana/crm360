import joblib
import pandas as pd
import seaborn as sns
import requests
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score, \
    average_precision_score

response1=requests.get("http://127.0.0.1:8000/api/deal/deals")
response2=requests.get("http://127.0.0.1:8000/api/customer/customers")
response3=requests.get("http://127.0.0.1:8000/api/interaction/interactions")
df1=response1.json()
df2=response2.json()
df3=response3.json()
df1=pd.DataFrame(df1)
df2=pd.DataFrame(df2)
df3=pd.DataFrame(df3)
df1=df1.merge(df2,on='customer_id',how='inner')
df=df1.merge(df3,on='customer_id',how='inner')

print(df.columns)

df['stage']=df['stage'].apply(lambda x:1 if x=='Won' else 0)
print(df['stage'].value_counts())
print(df.isnull().sum())

df['created_date']=pd.to_datetime(df['created_date'])
df['created_date_year']=df['created_date'].dt.year
df['created_date_month']=df['created_date'].dt.month
df['closed_date']=pd.to_datetime(df['closed_date'])
df['closed_date_year']=df['closed_date'].dt.year
df['closed_date_month']=df['closed_date'].dt.month
df['doj']=pd.to_datetime(df['doj'])
df['doj_year']=df['doj'].dt.year
df['doj_month']=df['doj'].dt.month
df['interaction_date']=pd.to_datetime(df['interaction_date'])
df['interaction_date_year']=df['interaction_date'].dt.year
df['interaction_date_month']=df['interaction_date'].dt.month
df['customer_tenure_days']=(pd.Timestamp.today()-df['doj']).dt.days
df['deals_duration']=(df['closed_date']-df['created_date']).dt.days

df.drop(['deal_id','deal_owner','email','doj','created_date','closed_date','interaction_date','city'],axis=1,inplace=True)

ohe=OneHotEncoder()
categorical_col=['state','segment','channel','type','outcome']
encoded=ohe.fit_transform(df[categorical_col])
encoded=pd.DataFrame(encoded.toarray(),columns=ohe.get_feature_names_out(categorical_col))
df=pd.concat([df.drop(categorical_col,axis=1),encoded],axis=1)

pipeline=Pipeline([
    ("imputer", SimpleImputer(strategy="median") ),
    ("scaler", StandardScaler()),
(   'DecisionTreeClassifier', DecisionTreeClassifier(class_weight='balanced',max_depth=10,random_state=42)),
])

print(df.columns)

X=df.drop("stage",axis=1)
y=df["stage"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

pipeline.fit(X_train,y_train)
y_predict_decision_tree=pipeline.predict(X_test)
acc=accuracy_score(y_test,y_predict_decision_tree)
print(acc)
conf_matrix=confusion_matrix(y_test,y_predict_decision_tree)
sns.heatmap(conf_matrix,annot=True,fmt="g")

print("classification_report:",classification_report(y_test,y_predict_decision_tree))
print("roc auc score:",roc_auc_score(y_test,y_predict_decision_tree))
print("precision auc:",average_precision_score(y_test,y_predict_decision_tree))


joblib.dump(pipeline,"../model_trained/deals_model.pkl")