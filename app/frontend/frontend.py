import streamlit as st
from cohort import cohort_retention_matrix_func
from customer_lifetime_value import customer_lifetime_value_function, customer_top10_by_revenue_func
from revenue import monthly_revenue,aov_func,region_product_func
from sales_funnel import sales_funnel_func,deal_stage_velocity_func
from seasonal_demand import seasonal_demand_index_func
from user_details_ml import churn_model
from forecast_ml import revenue_forecast

pg=st.sidebar.selectbox(
    "select dashboards",
    [
        "Revenue Analysis",
        "Customer Analytics",
        "Sales Funnel",
        "Cohort Analysis",
        "Seasonal Demand",
        "Churn Model",
        "Revenue Forecast",
    ]
)
if pg=="Revenue Analysis":
    monthly_revenue()
    aov_func()
    region_product_func()
if pg=="Customer Analytics":
    customer_lifetime_value_function()
    customer_top10_by_revenue_func()
if pg=="Sales Funnel":
    sales_funnel_func()
    deal_stage_velocity_func()
if pg=="Cohort Analysis":
    cohort_retention_matrix_func()
if pg=="Seasonal Demand":
    seasonal_demand_index_func()
if pg=='Churn Model':
    churn_model()
if pg=='Revenue Forecast':
    revenue_forecast()