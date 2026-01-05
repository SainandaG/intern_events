import requests
import json

BASE_URL = "http://localhost:8000/api"
HEADERS = {"Authorization": "Bearer ADMIN_DEMO_TOKEN"}

endpoints = [
    # ADMIN DASHBOARD
    "/api/admin/dashboard/financials",
    "/api/admin/dashboard/activity",
    
    # VENDOR DASHBOARD
    "/vendor/dashboard",
    
    # ADMIN ANALYTICS
    "/admin/analytics/stats",
    "/admin/analytics/revenue-trends",
    "/admin/analytics/event-analytics",
    "/admin/analytics/revenue-by-category",
    "/admin/analytics/top-vendors",
    
    # VENDOR ANALYTICS
    "/vendor/analytics/stats",
    "/vendor/analytics/notifications",
    "/vendor/analytics/charts",
    
    # CONSUMER ANALYTICS
    "/consumer/dashboard/favorites",
    "/consumer/dashboard/suggested",
    "/consumer/dashboard/history"
]

results = []

print("🧪 Final Dashboard & Analytics Audit...")

for ep in endpoints:
    url = f"{BASE_URL}{ep}"
    try:
        res = requests.get(url, headers=HEADERS)
        print(f"[{res.status_code}] {ep}")
        results.append({
            "endpoint": ep,
            "status": res.status_code,
            "working": res.status_code == 200
        })
    except Exception as e:
        print(f"[ERROR] {ep}: {str(e)}")
        results.append({
            "endpoint": ep,
            "status": "ERROR",
            "error": str(e)
        })

working_count = sum(1 for r in results if r.get('working'))
print(f"\n📊 Audit Result: {working_count}/{len(endpoints)} endpoints working.")
