import pandas as pd
from app.db.connection import engine

customers_df=pd.read_csv('../raw_datasets/customers.csv')
contacts_df=pd.read_csv('../raw_datasets/contacts.csv')
deals_df=pd.read_csv('../raw_datasets/deals.csv')
orders_df=pd.read_csv('../raw_datasets/orders.csv')
products_df=pd.read_csv('../raw_datasets/products.csv')
complaints_df=pd.read_csv('../raw_datasets/complaints.csv')
interactions_df=pd.read_csv('../raw_datasets/interactions.csv')

# missing values
print("customers dataframe missing values:",customers_df.isnull().sum())
print("contacts dataframe missing values:",contacts_df.isnull().sum())
print("deals dataframe missing values:",deals_df.isnull().sum())
print("orders dataframe missing values:",orders_df.isnull().sum())
print("products dataframe missing values:",products_df.isnull().sum())
print("interactions dataframe missing values:",interactions_df.isnull().sum())

# handle missing values
customers_df['email']=customers_df['email'].fillna('unknown@gmail.com')
customers_df['annual_spend']=pd.to_numeric(customers_df['annual_spend'],errors='coerce')
customers_df['annual_spend'] = customers_df['annual_spend'].fillna(
    customers_df['annual_spend'].mean()
)
contacts_df=contacts_df.dropna(subset=['phone'])
orders_df=orders_df.dropna(subset=['product_id'])

# find duplicates
print("duplicated of customers data:",customers_df.duplicated().sum())
print("duplicated of contacts data:",contacts_df.duplicated().sum())
print("duplicated of orders data:",orders_df.duplicated().sum())
print("duplicated of products data:",products_df.duplicated().sum())
print("duplicated of interactions data:",interactions_df.duplicated().sum())
print("duplicated of complaints data:",complaints_df.duplicated().sum())

# handle duplicated
contacts_df=contacts_df.drop_duplicates()

# outliers
q1=customers_df['annual_spend'].quantile(0.25)
q3=customers_df['annual_spend'].quantile(0.75)
iqr=q3-q1
lower=q1-1.5*iqr
upper=q3+1.5*iqr

outliers = customers_df[
    (customers_df['annual_spend'] < lower) |
    (customers_df['annual_spend'] > upper)
]
customers_df['annual_spend']=customers_df['annual_spend'].clip(lower,upper)

# data consistency
customers_df['city']=customers_df['city'].str.strip().str.title()
customers_df['state']=customers_df['state'].str.strip().str.title()
contacts_df['preferred_channel']=contacts_df['preferred_channel'].str.strip().str.lower()
deals_df['stage']=deals_df['stage'].str.lower()
products_df['category']=products_df['category'].str.lower()
interactions_df['type']=interactions_df['type'].str.lower()
interactions_df['channel']=interactions_df['channel'].str.lower()
interactions_df['outcome']=interactions_df['outcome'].str.lower()

# data handling
customers_df['doj']=pd.to_datetime(customers_df['doj'])
customers_df['churn'] = customers_df['churn'].astype(str)
contacts_df['phone'] = (
    contacts_df['phone']
    .astype(str)
    .str.replace('.0', '', regex=False)
)
contacts_df['last_contact'] = pd.to_datetime(
    contacts_df['last_contact']
)
deals_df['created_date']=pd.to_datetime(deals_df['created_date'])
deals_df['closed_date']=pd.to_datetime(deals_df['closed_date'])
orders_df['order_date']=pd.to_datetime(orders_df['order_date'])
interactions_df['interaction_date']=pd.to_datetime(interactions_df['interaction_date'])

customers_df.to_csv('../cleaned_data/customers_data.csv',index=False)
contacts_df.to_csv('../cleaned_data/contacts_data.csv',index=False)
deals_df.to_csv('../cleaned_data/deals_data.csv',index=False)
orders_df.to_csv('../cleaned_data/orders_data.csv',index=False)
interactions_df.to_csv('../cleaned_data/interactions_data.csv',index=False)
complaints_df.to_csv('../cleaned_data/complaints_data.csv',index=False)


# load data to mysql
customers_df = customers_df.drop_duplicates(subset=['customer_id'])
customers_df.to_sql('customer',con=engine,if_exists="append",index=False)

contacts_df.to_sql('contact',con=engine,if_exists="append",index=False)
deals_df = deals_df.drop_duplicates(subset=['deal_id'])
deals_df.to_sql('deal',con=engine,if_exists="append",index=False)
products_df = products_df.drop_duplicates(subset=['product_id'])
products_df.to_sql('product',con=engine,if_exists="append",index=False)
orders_df['product_id'] = orders_df['product_id'].astype(int)

orders_df['amount'] = pd.to_numeric(
    orders_df['amount'],
    errors='coerce'
)

orders_df = orders_df.dropna(subset=['amount'])
orders_df = orders_df.drop_duplicates(subset=['order_id'])
orders_df.to_sql('order',con=engine,if_exists="append",index=False)
interactions_df.to_sql('interation',con=engine,if_exists="append",index=False)
complaints_df.to_sql('complaint',con=engine,if_exists="append",index=False)