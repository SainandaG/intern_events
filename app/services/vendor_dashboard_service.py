from sqlalchemy.orm import Session
from app.schemas.vendor_dashboard_schema import (
    VendorDashboardResponse,
    VendorStats,
    RevenuePoint,
    CategoryBid,
)

def get_vendor_dashboard(db: Session, vendor_id: int) -> VendorDashboardResponse:

    # TODO replace these static values later using real queries
    stats = VendorStats(
        active_bids=12,
        won_contracts=8,
        monthly_revenue=2400000,
    )

    revenue_chart = [
        RevenuePoint(month="Jan", revenue=18000),
        RevenuePoint(month="Feb", revenue=21000),
        RevenuePoint(month="Mar", revenue=19500),
        RevenuePoint(month="Apr", revenue=23000),
        RevenuePoint(month="May", revenue=22000),
        RevenuePoint(month="Jun", revenue=24000),
    ]

    bid_categories = [
        CategoryBid(category="Catering", count=5),
        CategoryBid(category="Decoration", count=3),
        CategoryBid(category="Photography", count=2),
        CategoryBid(category="Music", count=2),
    ]

    notifications = [
        {"id": 1, "type": "bid-opportunity", "message": "New bid opportunity"},
        {"id": 2, "type": "order-confirmed", "message": "New confirmed order"},
    ]

    return VendorDashboardResponse(
        stats=stats,
        revenue_chart=revenue_chart,
        bid_categories=bid_categories,
        notifications=notifications,
    )
