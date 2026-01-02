# 📡 Analytics Endpoints Specification

This file lists all the API endpoints required to power the Analytics Dashboards.

## 1. 👑 Admin Dashboard APIs
**File**: [app/routes/admin_dashboard_api.py](file:///d:/evination/app/routes/admin_dashboard_api.py)
**Prefix**: `/api/admin`

| Method | Endpoint | Description | Response Schema |
| :--- | :--- | :--- | :--- |
| `GET` | `/stats` | **KPI Cards**: Total Events, Revenue, Active Vendors, etc. | [AdminStatsResponse](file:///d:/evination/app/schemas/analytics_schema.py#23-25) |
| `GET` | `/analytics/revenue-trends` | **Revenue Chart**: Monthly revenue vs target. | `List[RevenueTrendItem]` |
| `GET` | `/analytics/revenue-by-category` | **Pie Chart**: Revenue split by Wedding, Corporate, etc. | `List[CategoryRevenueItem]` |
| `GET` | `/analytics/event-analytics` | **Bar Chart**: Breakdown of events by status (Upcoming, etc.) | `List[EventStatusItem]` |
| `GET` | `/analytics/vendor-analytics` | **Leaderboard**: Top 5 vendors by revenue. | `List[VendorPerformanceResponse]` |

---

## 2. 🏪 Vendor Dashboard APIs
**File**: [app/routes/vendor_dashboard_api.py](file:///d:/evination/app/routes/vendor_dashboard_api.py)
**Prefix**: `/api/vendor`

| Method | Endpoint | Description | Response Schema |
| :--- | :--- | :--- | :--- |
| `GET` | `/stats` | **KPI Grid**: Active Bids, Won Contracts, Monthly Revenue. | [VendorStatsResponse](file:///d:/evination/app/schemas/analytics_schema.py#55-57) |
| `GET` | `/notifications` | **Feed**: Urgent orders and new bid opportunities. | `List[NotificationItem]` |
| `GET` | `/charts` | **Visuals**: Revenue trend (Area) + Bids by Category (Bar). | [VendorChartsResponse](file:///d:/evination/app/schemas/analytics_schema.py#58-61) |

---

## 3. 👤 Customer Dashboard APIs (Phase 3)
**File**: [app/routes/consumer_dashboard_api.py](file:///d:/evination/app/routes/consumer_dashboard_api.py)
**Prefix**: `/api/consumer/dashboard`

| Method | Endpoint | Description | Response Schema |
| :--- | :--- | :--- | :--- |
| `GET` | `/favorites` | **Top Picks**: List of favorite/top-rated events. | `List[CustomerFavoriteItem]` |
| `GET` | `/suggested` | **Trending**: Suggested categories or events. | `List[CustomerSuggestedItem]` |
| `GET` | `/history` | **My Events**: Past booking history. | `List[CustomerHistoryItem]` |
