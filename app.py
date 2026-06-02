import streamlit as st
import plotly.express as px
from utils.queries import executive_scorecard, action_dashboard, daily_spend_trend, workload_spend_31d, top_actions
from utils.formatting import money, number

st.set_page_config(
    page_title="Databricks FinOps Command Center",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Databricks FinOps & Governance Command Center")
st.caption("Databricks-native app using Spark session. No SQL warehouse token/HTTP path required.")

score = executive_scorecard()
actions = action_dashboard()

if score.empty:
    st.error("No data found in dbx_finops_executive_scorecard_v. Run the FinOps SQL framework first.")
    st.stop()

s = score.iloc[0]
a = actions.iloc[0] if not actions.empty else None

st.subheader("Executive Scorecard")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("31D Cost", money(s.get("current_cost_usd_31d", 0)))
c2.metric("90D Forecast", money(s.get("forecast_90d_usd", 0)))
c3.metric("365D Forecast", money(s.get("forecast_365d_usd", 0)))
c4.metric("Savings Opp. 90D", money(s.get("bookable_savings_opportunity_90d_usd", 0)))
c5.metric("Users in Scope", number(s.get("users_in_scope", 0)))

if a is not None:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Actions", number(a.get("total_actions", 0)))
    c2.metric("Open", number(a.get("open_actions", 0)))
    c3.metric("In Progress", number(a.get("in_progress_actions", 0)))
    c4.metric("Implemented", number(a.get("implemented_actions", 0)))
    c5.metric("Est. Annual Savings", money(a.get("estimated_annual_savings_usd", 0)))

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Spend by Workload Category")
    workload = workload_spend_31d()
    if not workload.empty:
        fig = px.pie(workload, names="finops_workload_category", values="cost_usd_31d", hole=0.45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No workload data found.")

with right:
    st.subheader("Daily Spend Trend")
    trend = daily_spend_trend()
    if not trend.empty:
        fig = px.line(trend, x="usage_date", y="cost_usd", color="finops_workload_category", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No spend trend found.")

st.divider()

st.subheader("Top FinOps Actions")
ta = top_actions(limit=25)
if not ta.empty:
    cols = [
        c for c in [
            "policy_id", "object_level", "object_name", "attributed_user",
            "team_name", "environment", "finding_type", "current_monthly_cost_usd",
            "estimated_monthly_savings_usd", "estimated_annual_savings_usd",
            "recommended_action", "what_to_change", "where_to_change",
            "how_to_change", "action_status", "assigned_owner", "due_date"
        ] if c in ta.columns
    ]
    st.dataframe(ta[cols], use_container_width=True, hide_index=True)
else:
    st.info("No action queue records found.")
