# 📊 Master Project Plan & Intern Guide

**Project**: Evination Analytics Portal
**Tech Stack**: FastAPI (Backend) + Streamlit (Frontend) + MySQL

---

## 1. 🏗️ High-Level Architecture
The system consists of a centralized API handling all data aggregation, consumed by a multi-page Streamlit application.

*   **Backend (`app/`)**: Exposes REST endpoints returning JSON data strictly adhering to [analytics_schema.py](file:///d:/evination/app/schemas/analytics_schema.py).
*   **Frontend (`dashboards/`)**: Streamlit pages that fetch JSON and render Charts (Altair/Recharts style) and KPI cards.

---

## 2. 👨‍💻 Intern 1: Admin Dashboard (The "Business" View)
**Responsibility**: Replicate the UI logic from `admin.tsx` into `1_Admin_Overview.py`.

### Detailed Instructions

#### A. KPI Grid (Top Section)
*   **UI Requirement**: 8 Cards (Total Events, Active Vendors, Revenue, Pending Bids, etc.).
*   **Backend Task**: Update `get_admin_stats` in [admin_dashboard_api.py](file:///d:/evination/app/routes/admin_dashboard_api.py).
    *   *Logic*: Return a list of [StatItem](file:///d:/evination/app/schemas/analytics_schema.py#7-14).
    *   *Schema*: [AdminStatsResponse](file:///d:/evination/app/schemas/analytics_schema.py#23-25).
*   **Frontend Task**: Use `st.metric` or custom HTML cards to display these 8 values.

#### B. Charts Section
1.  **Revenue Trend** (Area Chart)
    *   *Endpoint*: `GET /api/admin/revenue-analytics` ([trends](file:///d:/evination/dashboards/utils/api_client.py#7-17) field).
    *   *Visual*: X-Axis=Month, Y-Axis=Revenue vs Target.
2.  **Revenue by Category** (Donut Chart)
    *   *Endpoint*: `GET /api/admin/revenue-analytics` ([by_category](file:///d:/evination/app/routes/admin_dashboard_api.py#23-35) field).
3.  **Event Status Breakdown** (Bar Chart)
    *   *Endpoint*: `GET /api/admin/event-analytics` (`status_breakdown` field).
    *   *Visual*: Statuses: Upcoming, Ongoing, Completed, Cancelled.

#### C. Data Lists
1.  **Top Vendors**:
    *   *Endpoint*: `GET /api/admin/vendor-analytics`.
    *   *Display*: A sorted table or list of top 5 vendors by revenue.
2.  **Upcoming Events**:
    *   *Endpoint*: `GET /api/admin/event-analytics` (`upcoming_events` field).

---

## 3. 👩‍💻 Intern 2: Vendor Dashboard (The "Operations" View)
**Responsibility**: Replicate `VendorDashboard.tsx` into `5_Vendor_Dashboard.py`.

### Detailed Instructions

#### A. Notification Center (Critical Feature)
*   **UI Requirement**: A feed distinguishing "Urgent" vs "Regular" alerts.
*   **Backend Task**: Implement `GET /api/vendor/notifications` in [vendor_dashboard_api.py](file:///d:/evination/app/routes/vendor_dashboard_api.py).
    *   *Logic*: Fetch pending orders (`VendorOrder`) and new invites (`VendorBid`).
    *   *Mapping*: Urgent = Pending Orders < 24h or New Invites.
*   **Frontend Task**: Iterate through the list. Use `st.error` for urgent and `st.info` for regular notifications.

#### B. Performance Metrics
1.  **KPIs**: Active Bids, Won Contracts, Monthly Revenue.
    *   *Endpoint*: `GET /api/vendor/stats`.
2.  **Revenue Chart** (Area Chart):
    *   *Endpoint*: `GET /api/vendor/charts` ([revenue_trend](file:///d:/evination/dashboards/utils/api_client.py#7-17)).
3.  **Bids by Category** (Bar Chart):
    *   *Endpoint*: `GET /api/vendor/charts` (`bids_by_category`).

---

## 4. 👤 Phase 3: Customer Dashboard (Future/Bonus)
**Responsibility**: Replicate `Dashboard.tsx` (Welcome Back screen).

*   **Endpoint**: `GET /api/consumer/dashboard/favorites` (Top rated events).
*   **Endpoint**: `GET /api/consumer/dashboard/suggested` (Trending categories).
*   **Endpoint**: `GET /api/consumer/dashboard/history` (Previous orders).

---

## 5. ⚙️ Technical Setup & Rules

### Setup Commands
1.  `python setup_db.py` (Initialize DB)
2.  `alembic upgrade head` (Run Migrations)
3.  `python -m uvicorn app.main:app --reload --port 8000` (Start Backend)
4.  `streamlit run dashboards/app.py --server.port 8502` (Start Frontend)

### Golden Rules
1.  **Do NOT Change Schemas**: [app/schemas/analytics_schema.py](file:///d:/evination/app/schemas/analytics_schema.py) is the source of truth.
2.  **Mock First**: Hardcode response data first to verify UI, then connect SQL queries.
3.  **Port Conflict**: Use port `8502` for Streamlit if `8501` is busy.
