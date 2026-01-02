import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

class APIClient:
    @staticmethod
    def get_revenue_trends():
        """Fetches revenue trend data for the Area Chart."""
        try:
            response = requests.get(f"{BASE_URL}/api/admin/analytics/revenue-trends")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching revenue trends: {e}")
            return []

    @staticmethod
    def get_revenue_by_category():
        """Fetches revenue by category for the Pie Chart."""
        try:
            response = requests.get(f"{BASE_URL}/api/admin/analytics/revenue-by-category")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching category revenue: {e}")
            return []
