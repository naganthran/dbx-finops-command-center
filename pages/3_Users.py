import streamlit as st
import plotly.express as px
from utils.queries import user_spend, owner_breakdown

st.set_page_config(page_title="User & Team Attribution", layout="wide")
st.title("👥 User & Team Attribution")

users = user_spend()
owners = owner_breakdown()

left, right = st.columns(2)

with left:
    st.subheader("Top Users by Cost")
    if not users.empty:
        top = users.head(25).sort_values("total_cost_usd_31d")
        fig = px.bar(top, x="total_cost_usd_31d", y="attributed_user", orientation="h", text="total_cost_usd_31d")
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Team / Owner Savings Exposure")
    if not owners.empty:
        top = owners.head(25).sort_values("estimated_annual_savings_usd")
        fig = px.bar(top, x="estimated_annual_savings_usd", y="team_name", color="environment", orientation="h", text="estimated_annual_savings_usd")
        st.plotly_chart(fig, use_container_width=True)

st.subheader("User Spend Detail")
if not users.empty:
    st.dataframe(users, use_container_width=True, hide_index=True)

st.subheader("Owner / Team Detail")
if not owners.empty:
    st.dataframe(owners, use_container_width=True, hide_index=True)
