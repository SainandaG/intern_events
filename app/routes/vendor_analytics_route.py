from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics_schema import VendorPerformanceResponse
from app.dependencies_vendor import get_current_vendor

router = APIRouter(prefix="/api/vendor/analytics", tags=["Vendor Analytics"])

@router.get("/performance", response_model=VendorPerformanceResponse)
def get_vendor_performance(
    db: Session = Depends(get_db),
    vendor = Depends(get_current_vendor)
):
    return AnalyticsService.get_vendor_performance(db, vendor.id)
