import streamlit as st
import plotly.express as px
from utils.queries import workload_spend_31d, policy_breakdown, daily_spend_trend

st.set_page_config(page_title="Spend Analysis", layout="wide")
st.title("💰 Spend Analysis")

workload = workload_spend_31d()
policy = policy_breakdown()
trend = daily_spend_trend()

left, right = st.columns(2)

with left:
    st.subheader("Workload Spend 31D")
    if not workload.empty:
        fig = px.pie(workload, names="finops_workload_category", values="cost_usd_31d", hole=0.45)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(workload, use_container_width=True, hide_index=True)

with right:
    st.subheader("Policy Savings Exposure")
    if not policy.empty:
        fig = px.bar(
            policy.sort_values("estimated_annual_savings_usd"),
            x="estimated_annual_savings_usd",
            y="policy_id",
            orientation="h",
            text="estimated_annual_savings_usd"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(policy, use_container_width=True, hide_index=True)

st.divider()
st.subheader("90-Day Daily Spend Trend")
if not trend.empty:
    fig = px.line(trend, x="usage_date", y="cost_usd", color="finops_workload_category", markers=True)
    st.plotly_chart(fig, use_container_width=True)
