from datetime import timedelta, datetime
import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.customer_model import Customer
from app.models.deal_model import Deal
from app.models.order_model import Order
from app.models.product_model import Product

def monthly_revenue(db:Session):
    monthly_revenue_kpi=(
        db.query(
            func.month(Order.order_date).label('month'),
            func.sum(Order.amount).label('total_revenue'),
            func.avg(Order.amount).label('avg_revenue'),
            func.sum(Order.qty).label('total_orders'),
        )
    .group_by(func.month(Order.order_date))
    .all())
    monthly_revenue_kpi=pd.DataFrame(monthly_revenue_kpi,columns=['month','total_revenue','avg_revenue','total_orders'])
    return monthly_revenue_kpi.reset_index().to_dict(
        orient="records"
    )

def customer_lifetime_value(db:Session):
    customer_lifetime_kpi=(
        db.query(
            Customer.name.label('customer_name'),
            Order.customer_id.label('customer_id'),
            func.sum(Order.amount).label('clv'),
        )
        .join(Order,Customer.customer_id==Order.customer_id)
        .group_by(Customer.name,Order.customer_id)
        .all()
    )
    customer_lifetime_kpi=pd.DataFrame(customer_lifetime_kpi,columns=['customer_name','customer_id','clv'])
    return customer_lifetime_kpi.reset_index().to_dict(
        orient="records"
    )

def sales_funnel_rate(db:Session):
    sales_funnel_rate_kpi=(
        db.query(
            Deal.stage.label('stage'),
            func.count(Deal.customer_id).label('deal count'),
        )
        .group_by(Deal.stage)
        .all()
    )
    sales_funnel_rate_kpi=pd.DataFrame(sales_funnel_rate_kpi,columns=['stage','deal count'])
    return sales_funnel_rate_kpi.reset_index().to_dict(
        orient="records"
    )

def customer_top10_by_revenue(db:Session):
    last_90_days=datetime.now()-timedelta(days=90)
    customer_top10_by_revenue_kpi=(
        db.query(
            Customer.name.label('customer_name'),
            Order.customer_id.label('customer_id'),
            func.sum(Order.amount).label('total_revenue'),
        )
        .join(Order,Customer.customer_id==Order.customer_id)
        .filter(Order.order_date >= last_90_days)
        .group_by(Customer.name,Order.customer_id)
        .order_by(func.sum(Order.amount).desc())
        .limit(10)
        .all()
    )
    customer_top10_by_revenue_kpi=pd.DataFrame(customer_top10_by_revenue_kpi,columns=['customer_name','customer_id','total_revenue'])
    return customer_top10_by_revenue_kpi.reset_index().to_dict(
        orient="records"
    )

def cohort_retention_matrix(db: Session):
    cohort_retention_matrix_kpi = (
        db.query(
            Customer.name.label('customer_name'),
            Order.customer_id.label('customer_id'),
            func.min(Order.order_date)
            .over(partition_by=Order.customer_id)
            .label('first_order'),
            Order.order_date.label('another_orders')
        )
        .join(Order,Customer.customer_id==Order.customer_id)
        .all()
    )
    df=pd.DataFrame(
        cohort_retention_matrix_kpi,
        columns=['customer_name','customer_id','first_order','another_orders']
    )
    df['cohort_index']=(
        (df['another_orders'].dt.year - df['first_order'].dt.year) * 12+
        (df['another_orders'].dt.month - df['first_order'].dt.month)
    )
    df['cohort_month']=(df['first_order'].dt.to_period('M').astype(str))
    cohort_table=df.pivot_table(
        index='cohort_month',
        columns='cohort_index',
        values='customer_id',
        aggfunc='nunique',
        fill_value=0
    )
    cohort_table=cohort_table.reset_index()
    return cohort_table.to_dict(orient='records')

def aov(db:Session):
    aov_kpi=(
        db.query(
            func.month(Order.order_date).label('order_month'),
            func.avg(Order.amount).label('aov'),
        )
        .group_by(func.month(Order.order_date))
        .all()
    )
    aov_kpi=pd.DataFrame(aov_kpi,columns=['order_month','aov'])
    return aov_kpi.reset_index().to_dict(
        orient="records"
    )

def region_product(db:Session):
    result=(
        db.query(
            Order.order_id.label('order_id'),
            Customer.city.label('city'),
            Product.category.label('category'),
            Order.amount.label('amount'),
        )
        .join(Customer,Order.customer_id==Customer.customer_id)
        .join(Product,Order.product_id==Product.product_id)
        .all()
    )
    df=pd.DataFrame(result,columns=['order_id','city','category','amount'])
    result_pivot=df.pivot_table(
        index='city',
        columns='category',
        values='amount',
        aggfunc='sum',
        fill_value=0
    )
    return result_pivot.reset_index().to_dict(
        orient="records"
    )

def deal_stage_velocity(db:Session):
    deal_stage_velocity_kpi=(
        db.query(
            Deal.stage.label('stage'),
            func.avg(func.datediff(Deal.closed_date,Deal.created_date)).label('avg_days')
        )
        .group_by(Deal.stage)
        .all()
    )
    deal_stage_velocity_kpi=pd.DataFrame(deal_stage_velocity_kpi,columns=['stage','avg_days'])
    return deal_stage_velocity_kpi.reset_index().to_dict(
        orient="records"
    )

def seasonal_demand_index(db:Session):
    seasonal_demand_index_kpi=(
        db.query(
            func.month(Order.order_date).label('order_month'),
            Product.category.label('category'),
            func.sum(Order.amount).label('order_amount'),
        )
        .join(Product,Order.product_id==Product.product_id)
        .group_by(func.month(Order.order_date),Product.category)
        .all()
    )
    df=pd.DataFrame(seasonal_demand_index_kpi,columns=['month','category','order_amount'])
    seasonal_demand_index_pivot=df.pivot_table(
        index='month',
        columns='category',
        values='order_amount',
        aggfunc='sum',
        fill_value=0
    )
    return seasonal_demand_index_pivot.reset_index().to_dict(
        orient="records"
    )
