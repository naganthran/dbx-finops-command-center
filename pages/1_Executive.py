import streamlit as st
import plotly.express as px
from utils.queries import executive_scorecard, action_dashboard, workload_spend_31d, daily_spend_trend
from utils.formatting import money, number

st.set_page_config(page_title="Executive", layout="wide")
st.title("🏠 Executive Summary")

score = executive_scorecard()
actions = action_dashboard()

if score.empty:
    st.error("No executive scorecard data found.")
    st.stop()

s = score.iloc[0]
a = actions.iloc[0] if not actions.empty else None

c1, c2, c3, c4 = st.columns(4)
c1.metric("Current 31D Cost", money(s.get("current_cost_usd_31d", 0)))
c2.metric("90D Forecast", money(s.get("forecast_90d_usd", 0)))
c3.metric("365D Forecast", money(s.get("forecast_365d_usd", 0)))
c4.metric("Users in Scope", number(s.get("users_in_scope", 0)))

c1, c2, c3, c4 = st.columns(4)
c1.metric("Opportunities", number(s.get("opportunities", 0)))
c2.metric("High Confidence", number(s.get("high_confidence_opportunities", 0)))
c3.metric("Governance Opps", number(s.get("governance_opportunities", 0)))
c4.metric("Optimization Opps", number(s.get("optimization_opportunities", 0)))

if a is not None:
    st.subheader("Action Queue Summary")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Open", number(a.get("open_actions", 0)))
    c2.metric("Acknowledged", number(a.get("acknowledged_actions", 0)))
    c3.metric("In Progress", number(a.get("in_progress_actions", 0)))
    c4.metric("Implemented", number(a.get("implemented_actions", 0)))
    c5.metric("Verified", number(a.get("verified_actions", 0)))

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Spend by Workload")
    df = workload_spend_31d()
    if not df.empty:
        fig = px.bar(df, x="finops_workload_category", y="cost_usd_31d", text="cost_usd_31d")
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Daily Cost Trend")
    trend = daily_spend_trend()
    if not trend.empty:
        fig = px.area(trend, x="usage_date", y="cost_usd", color="finops_workload_category")
        st.plotly_chart(fig, use_container_width=True)
