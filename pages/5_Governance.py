import streamlit as st
import plotly.express as px
from utils.queries import action_dashboard, top_actions, policy_breakdown, governance_queue
from utils.formatting import money, number

st.set_page_config(page_title="Governance", layout="wide")
st.title("📊 Governance & FinOps Intelligence")

dash = action_dashboard()
if not dash.empty:
    d = dash.iloc[0]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Actions", number(d.get("total_actions", 0)))
    c2.metric("Open", number(d.get("open_actions", 0)))
    c3.metric("In Progress", number(d.get("in_progress_actions", 0)))
    c4.metric("Implemented", number(d.get("implemented_actions", 0)))
    c5.metric("Verified", number(d.get("verified_actions", 0)))

    c1, c2, c3 = st.columns(3)
    c1.metric("Current Monthly Cost", money(d.get("current_monthly_cost_usd", 0)))
    c2.metric("Estimated Monthly Savings", money(d.get("estimated_monthly_savings_usd", 0)))
    c3.metric("Estimated Annual Savings", money(d.get("estimated_annual_savings_usd", 0)))

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Savings by Policy")
    policy = policy_breakdown()
    if not policy.empty:
        fig = px.bar(policy.sort_values("estimated_annual_savings_usd"), x="estimated_annual_savings_usd", y="policy_id", orientation="h", text="estimated_annual_savings_usd")
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Governance Opportunity Queue")
    queue = governance_queue(limit=100)
    if not queue.empty and "policy_group" in queue.columns:
        grouped = queue.groupby("policy_group", dropna=False)["bookable_savings_opportunity_90d_usd"].sum().reset_index()
        fig = px.pie(grouped, names="policy_group", values="bookable_savings_opportunity_90d_usd", hole=0.45)
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Action Queue")
actions = top_actions(limit=500)
if not actions.empty:
    status_values = ["ALL"] + sorted(actions["action_status"].dropna().unique().tolist()) if "action_status" in actions else ["ALL"]
    status = st.selectbox("Filter by status", status_values)

    df = actions.copy()
    if status != "ALL" and "action_status" in df:
        df = df[df["action_status"] == status]

    cols = [
        c for c in [
            "action_id", "policy_id", "object_level", "object_name", "attributed_user",
            "team_name", "environment", "finding_type", "current_monthly_cost_usd",
            "estimated_monthly_savings_usd", "estimated_annual_savings_usd",
            "recommended_action", "what_to_change", "where_to_change", "how_to_change",
            "action_status", "assigned_owner", "due_date"
        ] if c in df.columns
    ]
    st.dataframe(df[cols], use_container_width=True, hide_index=True)
else:
    st.info("No action queue data found.")
