import streamlit as st
import plotly.express as px
from utils.queries import cluster_opportunities, jobs_cost, serverless_governance, sql_candidates

st.set_page_config(page_title="Compute & Workloads", layout="wide")
st.title("🖥 Compute & Workload Analysis")

tabs = st.tabs(["Clusters", "Jobs", "SQL", "Serverless / AI"])

with tabs[0]:
    st.subheader("Cluster Opportunities")
    clusters = cluster_opportunities()
    if not clusters.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Clusters", f"{clusters['cluster_id'].nunique():,.0f}" if "cluster_id" in clusters else "0")
        if "cost_usd_31d" in clusters:
            c2.metric("31D Cost", f"${clusters['cost_usd_31d'].sum():,.0f}")
        if "estimated_idle_cost_usd_31d" in clusters:
            c3.metric("Idle Cost", f"${clusters['estimated_idle_cost_usd_31d'].sum():,.0f}")
        if "bookable_savings_opportunity_90d_usd" in clusters:
            c4.metric("90D Savings Opp.", f"${clusters['bookable_savings_opportunity_90d_usd'].sum():,.0f}")
        st.dataframe(clusters, use_container_width=True, hide_index=True)
    else:
        st.info("No cluster opportunities found.")

with tabs[1]:
    st.subheader("Jobs Cost")
    jobs = jobs_cost()
    if not jobs.empty:
        fig = px.bar(jobs.head(25).sort_values("cost_usd_31d"), x="cost_usd_31d", y="job_name", orientation="h")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(jobs, use_container_width=True, hide_index=True)
    else:
        st.info("No jobs cost data found.")

with tabs[2]:
    st.subheader("SQL Optimization Candidates")
    sql = sql_candidates()
    if not sql.empty:
        fig = px.bar(sql.head(25).sort_values("sql_cost_usd_31d"), x="sql_cost_usd_31d", y="executed_by", orientation="h", color="sql_problem_type")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(sql, use_container_width=True, hide_index=True)
    else:
        st.info("No SQL candidates found.")

with tabs[3]:
    st.subheader("Serverless / Vector / AI Governance")
    srv = serverless_governance()
    if not srv.empty:
        fig = px.bar(srv.head(25).sort_values("cost_usd_31d"), x="cost_usd_31d", y="attributed_user", orientation="h", color="finops_workload_category")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(srv, use_container_width=True, hide_index=True)
    else:
        st.info("No serverless governance data found.")
