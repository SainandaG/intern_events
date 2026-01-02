import requests
import streamlit as st

# In production, this would be managed via cookies or a proper Auth provider
# For this demo/ MVP, we store the full token string in session_state

BASE_URL = "http://localhost:8000"

# Mock Tokens (Ideally, these should be fetched via a /login UI)
# We will trust the user to have valid tokens in the 'tokens' dict for now 
# or implement a simple login form.

class APIClient:
    
    @staticmethod
    def get_token():
        return st.session_state.get('auth_token', None)

    @staticmethod
    def get_headers():
        token = APIClient.get_token()
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    # ------------------ ADMIN ------------------
    @staticmethod
    def get_admin_stats(time_range="month"):
        try:
            # Requires Admin Token - not strictly enforced in this demo client unless configured
            # Assuming Admin endpoints are public/protected for this phase
            res = requests.get(f"{BASE_URL}/api/admin/analytics/stats?time_range={time_range}", headers=APIClient.get_headers())
            return res.json() if res.status_code == 200 else None
        except: return None

    @staticmethod
    def get_admin_revenue_trends(time_range="month"):
        try:
            res = requests.get(f"{BASE_URL}/api/admin/analytics/revenue-trends?time_range={time_range}", headers=APIClient.get_headers())
            return res.json() if res.status_code == 200 else []
        except: return []
        
    @staticmethod
    def get_admin_event_analytics(time_range="month"):
        try:
            res = requests.get(f"{BASE_URL}/api/admin/analytics/event-analytics?time_range={time_range}", headers=APIClient.get_headers())
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def get_admin_revenue_by_category():
        try:
            res = requests.get(f"{BASE_URL}/api/admin/analytics/revenue-by-category", headers=APIClient.get_headers())
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def get_admin_top_vendors():
        try:
            res = requests.get(f"{BASE_URL}/api/admin/analytics/top-vendors", headers=APIClient.get_headers())
            return res.json() if res.status_code == 200 else []
        except: return []

    # ------------------ VENDOR ------------------
    @staticmethod
    def get_vendor_stats(time_range="month"):
        try:
            res = requests.get(f"{BASE_URL}/api/vendor/analytics/stats?time_range={time_range}", headers=APIClient.get_headers())
            return res.json() if res.status_code == 200 else None
        except: return None

    @staticmethod
    def get_vendor_notifications():
        try:
            res = requests.get(f"{BASE_URL}/api/vendor/analytics/notifications", headers=APIClient.get_headers())
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def get_vendor_charts(time_range="month"):
        try:
            res = requests.get(f"{BASE_URL}/api/vendor/analytics/charts?time_range={time_range}", headers=APIClient.get_headers())
            if res.status_code == 200:
                return res.json()
            return {"revenue_trend": [], "bids_by_category": []}
        except: return {"revenue_trend": [], "bids_by_category": []}

    # ------------------ CONSUMER ------------------
    @staticmethod
    def get_consumer_favorites():
        try:
            res = requests.get(f"{BASE_URL}/api/consumer/dashboard/favorites", headers=APIClient.get_headers())
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def get_consumer_suggested():
        try:
            res = requests.get(f"{BASE_URL}/api/consumer/dashboard/suggested", headers=APIClient.get_headers())
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def get_consumer_history():
        try:
            res = requests.get(f"{BASE_URL}/api/consumer/dashboard/history", headers=APIClient.get_headers())
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def login_vendor(username, password):
        """Simulate obtaining a token"""
        # Call the real login endpoint
        try:
            payload = {
                "username": username,
                "password": password
            }
            res = requests.post(f"{BASE_URL}/api/auth/vendor/token", data=payload) # Use form data or json depending on endpoint
            if res.status_code == 200:
                return res.json().get("access_token")
            return None
        except Exception as e:
            print(e)
            return None
