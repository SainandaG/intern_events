import streamlit as st
import pandas as pd
import altair as alt
from utils.api_client import APIClient

st.set_page_config(page_title="Revenue Analytics", page_icon="💰", layout="wide")

st.title("💰 Revenue Analytics")
st.caption("Intern 1 - Task 2")

# Fetch Data
with st.spinner("Fetching live data..."):
    trend_data = APIClient.get_revenue_trends()
    cat_data = APIClient.get_revenue_by_category()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Revenue vs Target Trend")
    if trend_data:
        df_trend = pd.DataFrame(trend_data)
        
        # Area Chart for Revenue
        area = alt.Chart(df_trend).mark_area(opacity=0.3, color='#fdb913').encode(
            x=alt.X('month', sort=None),
            y='revenue',
            tooltip=['month', 'revenue', 'target']
        )
        
        # Line Chart for Target
        line = alt.Chart(df_trend).mark_line(color='#94a3b8', strokeDash=[5, 5]).encode(
            x=alt.X('month', sort=None),
            y='target'
        )
        
        st.altair_chart((area + line).interactive(), use_container_width=True)
    else:
        st.warning("No trend data available.")

with col2:
    st.subheader("Revenue by Category")
    if cat_data:
        df_cat = pd.DataFrame(cat_data)
        
        pie = alt.Chart(df_cat).mark_arc(innerRadius=50).encode(
            theta=alt.Theta("revenue", stack=True),
            color=alt.Color("category"),
            tooltip=["category", "revenue", "percentage"]
        )
        st.altair_chart(pie, use_container_width=True)
        
        # Legend table
        st.dataframe(df_cat[['category', 'revenue', 'percentage']], hide_index=True)
    else:
        st.warning("No category data available.")
