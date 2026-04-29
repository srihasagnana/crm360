# generate_crm_dataset.py — Faker + NumPy synthetic data generator
import pandas as pd, numpy as np
from faker import Faker
fake = Faker('en_IN')
np.random.seed(42)
N = 2000 # number of customers
segments = ['Enterprise', 'SMB', 'Startup', 'Individual']
states = ['AP', 'TS', 'KA', 'TN', 'MH', 'DL', 'GJ', 'RJ']
stages = ['Lead', 'Qualified', 'Proposal', 'Negotiation', 'Won', 'Lost']
customers = pd.DataFrame({
 'customer_id' : range(1, N+1),
 'name' : [fake.company() for _ in range(N)],
 'email' : [fake.company_email() for _ in range(N)],
 'city' : [fake.city() for _ in range(N)],
 'state' : np.random.choice(states, N),
 'segment' : np.random.choice(segments, N, p=[.15, .40, .25, .20]),
 'doj' : pd.date_range('2020-01-01', periods=N, freq='8h'),
 'annual_spend': np.round(np.random.exponential(85000, N), 2),
 'churn' : np.random.choice([0, 1], N, p=[0.80, 0.20])
})
customers.loc[customers.sample(frac=0.08).index, 'email'] = None
customers.loc[customers.sample(frac=0.05).index, 'annual_spend'] = None
# Introduce 3% duplicates for cleaning practice
dups = customers.sample(frac=0.03).copy()
dups['name'] = dups['name'].str.replace(' ', ' ') # double space
customers = pd.concat([customers, dups]).reset_index(drop=True)
customers.loc[customers.sample(frac=0.01).index, 'annual_spend'] *= 50

contacts = pd.DataFrame({
    'contact_id': range(1, 4001),
    'customer_id': np.random.choice(customers['customer_id'], 4000),
    'phone': [fake.phone_number() for _ in range(4000)],
    'whatsapp': [fake.phone_number() for _ in range(4000)],
    'preferred_channel': np.random.choice(['Email', 'Phone', 'WhatsApp'], 4000),
    'last_contact': [fake.date_between(start_date='-1y', end_date='today') for _ in range(4000)]
})

contacts.loc[contacts.sample(frac=0.1).index, 'phone'] = None
contacts = pd.concat([contacts, contacts.sample(frac=0.03)])

deals = pd.DataFrame({
    'deal_id': range(1, 3501),
    'customer_id': np.random.choice(customers['customer_id'], 3500),
    'stage': np.random.choice(stages, 3500),
    'value': np.round(np.random.uniform(5000, 200000, 3500), 2),
    'created_date': [fake.date_between(start_date='-2y', end_date='today') for _ in range(3500)],
    'closed_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(3500)],
    'deal_owner': [fake.name() for _ in range(3500)]
})

deals = pd.concat([deals, deals.sample(frac=0.03)])

products = pd.DataFrame({
    'product_id': range(1, 151),
    'name': [fake.word().title() for _ in range(150)],
    'category': np.random.choice(['Software', 'Hardware', 'Service'], 150),
    'unit_price': np.round(np.random.uniform(1000, 50000, 150), 2),
    'cost': np.round(np.random.uniform(500, 30000, 150), 2),
    'stock_qty': np.random.randint(0, 500, 150)
})

orders = pd.DataFrame({
    'order_id': range(1, 8001),
    'customer_id': np.random.choice(customers['customer_id'], 8000),
    'product_id': np.random.choice(products['product_id'], 8000),
    'qty': np.random.randint(1, 10, 8000),
    'amount': np.round(np.random.uniform(1000, 100000, 8000), 2),
    'order_date': [fake.date_between(start_date='-2y', end_date='today') for _ in range(8000)],
    'status': np.random.choice(['Delivered', 'Pending', 'Cancelled'], 8000)
})

orders.loc[orders.sample(frac=0.05).index, 'product_id'] = None
orders['amount'] = orders['amount'].astype(object)
orders.loc[orders.sample(frac=0.02).index, 'amount'] = '₹5000'
orders['order_date'] = orders['order_date'].astype(str)

complaints = pd.DataFrame({
    'complaint_id': range(1, 1201),
    'customer_id': np.random.choice(customers['customer_id'], 1200),
    'category': np.random.choice(['Delivery', 'Product', 'Service'], 1200),
    'severity': np.random.choice(['Low', 'Medium', 'High'], 1200),
    'raised_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(1200)],
    'resolved_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(1200)]
})

interactions = pd.DataFrame({
    'interaction_id': range(1, 15001),
    'customer_id': np.random.choice(customers['customer_id'], 15000),
    'type': np.random.choice(['Call', 'Email', 'Meeting'], 15000),
    'channel': np.random.choice(['Phone', 'Email', 'WhatsApp'], 15000),
    'outcome': np.random.choice(['Positive', 'Neutral', 'Negative'], 15000),
    'interaction_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(15000)]
})


customers.to_csv('raw_datasets/customers.csv', index=False)
contacts.to_csv('raw_datasets/contacts.csv', index=False)
deals.to_csv('raw_datasets/deals.csv', index=False)
orders.to_csv('raw_datasets/orders.csv', index=False)
complaints.to_csv('raw_datasets/complaints.csv', index=False)
interactions.to_csv('raw_datasets/interactions.csv', index=False)
products.to_csv('raw_datasets/products.csv', index=False)
print(f'Generated {len(customers)} customer records')