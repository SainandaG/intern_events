from fastapi import APIRouter, Depends
from typing import List
from app.schemas.analytics_schema import RevenueTrendItem, CategoryRevenueItem

router = APIRouter(prefix="/api/admin/analytics", tags=["Admin Analytics"])

@router.get("/revenue-trends", response_model=List[RevenueTrendItem])
def get_revenue_trends():
    """
    Returns monthly revenue vs target data for the Area Chart.
    Reference: Intern 1 - Revenue Analytics Dashboard
    """
    # MOCK DATA - To be replaced with DB queries by interns or in next iteration
    return [
        {"month": "Jan", "revenue": 185000, "target": 180000},
        {"month": "Feb", "revenue": 220000, "target": 200000},
        {"month": "Mar", "revenue": 198000, "target": 210000},
        {"month": "Apr", "revenue": 248000, "target": 230000},
        {"month": "May", "revenue": 235000, "target": 240000},
        {"month": "Jun", "revenue": 284000, "target": 250000},
    ]

@router.get("/revenue-by-category", response_model=List[CategoryRevenueItem])
def get_revenue_by_category():
    """
    Returns revenue breakdown by category for the Pie Chart.
    Reference: Intern 1 - Revenue Analytics Dashboard
    """
    return [
        {"category": "Weddings", "revenue": 1240000, "percentage": 44},
        {"category": "Corporate", "revenue": 850000, "percentage": 30},
        {"category": "Birthdays", "revenue": 420000, "percentage": 15},
        {"category": "Conferences", "revenue": 310000, "percentage": 11},
    ]
