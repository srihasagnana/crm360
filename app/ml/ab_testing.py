import numpy as np
import requests
import pandas as pd
from scipy import stats

response=requests.get("http://127.0.0.1:8000/api/customer/customers")
df=response.json()
df=pd.DataFrame(df)

group_a=df[df['segment']=='SMB']['annual_spend']
group_b=df[df['segment']=='Individual']['annual_spend']
t_stat,p_stat=stats.ttest_ind(group_a,group_b,equal_var=False)

print(t_stat,p_stat)

if p_stat<0.05:
    print("significant")
else:
    print("not significant")

# save result
ab_df=pd.DataFrame({
    'group': ['SMB', 'Individual'],
    'avg annual spend':[group_a.mean(),group_b.mean()],
})

ab_df.to_csv("../model_trained/ab_testing.csv",index=False)