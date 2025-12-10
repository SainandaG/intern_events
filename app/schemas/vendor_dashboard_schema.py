# app/schemas/vendor_dashboard_schema.py

from pydantic import BaseModel
from typing import List, Optional


class VendorStats(BaseModel):
    active_bids: int
    won_contracts: int
    monthly_revenue: float


class RevenuePoint(BaseModel):
    month: str
    revenue: float


class CategoryBid(BaseModel):
    category: str
    count: int


class NotificationModel(BaseModel):
    id: int
    category: str
    type: str
    title: str
    message: str
    time: str
    urgent: Optional[bool] = False
    orderId: Optional[str] = None


class VendorDashboardResponse(BaseModel):
    stats: VendorStats
    revenue_chart: List[RevenuePoint]
    bid_categories: List[CategoryBid]
    notifications: List[NotificationModel]

    class Config:
        from_attributes = True
