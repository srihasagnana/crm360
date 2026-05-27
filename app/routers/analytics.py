from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.services.analytics import monthly_revenue, customer_lifetime_value, sales_funnel_rate, \
    customer_top10_by_revenue, cohort_retention_matrix, aov, region_product, deal_stage_velocity, seasonal_demand_index

router = APIRouter(prefix="/analytics", tags=["analytics"])
@router.get("/monthly_revenue")
def monthly_revenue_router(db:Session=Depends(get_db)):
    return monthly_revenue(db)

@router.get("/customer_lifetime_value")
def customer_lifetime_value_router(db:Session=Depends(get_db)):
    return customer_lifetime_value(db)

@router.get("/sales_funnel_rate")
def sales_funnel_rate_router(db:Session=Depends(get_db)):
    return sales_funnel_rate(db)

@router.get("/customer_top10_by_revenue")
def customer_top10_router(db:Session=Depends(get_db)):
    return customer_top10_by_revenue(db)

@router.get("/cohort_retention_matrix")
def cohort_retention_matrix_router(db:Session=Depends(get_db)):
    return cohort_retention_matrix(db)

@router.get("/aov")
def aov_router(db:Session=Depends(get_db)):
    return aov(db)

@router.get("/region_product")
def region_product_router(db:Session=Depends(get_db)):
    return region_product(db)

@router.get("/deal_stage_velocity")
def dealstage_velocity_router(db:Session=Depends(get_db)):
    return deal_stage_velocity(db)

@router.get("/seasonal_demand_index")
def seasonal_demand_index_router(db:Session=Depends(get_db)):
    return seasonal_demand_index(db)