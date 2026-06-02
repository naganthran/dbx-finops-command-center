CATALOG = "sandbox"
SCHEMA = "data_eng_dev"

TABLES = {
    "executive": f"{CATALOG}.{SCHEMA}.dbx_finops_executive_scorecard_v",
    "action_dashboard": f"{CATALOG}.{SCHEMA}.dbx_finops_action_dashboard_v",
    "top_actions": f"{CATALOG}.{SCHEMA}.dbx_finops_top_actions_v",
    "policy_breakdown": f"{CATALOG}.{SCHEMA}.dbx_finops_policy_breakdown_v",
    "owner_breakdown": f"{CATALOG}.{SCHEMA}.dbx_finops_owner_breakdown_v",
    "governance_queue": f"{CATALOG}.{SCHEMA}.dbx_finops_governance_action_queue_v",
    "billing_fact": f"{CATALOG}.{SCHEMA}.dbx_finops_billing_usage_90d_fact",
    "user_spend": f"{CATALOG}.{SCHEMA}.dbx_finops_user_spend_31d_mart",
    "cluster_opportunity": f"{CATALOG}.{SCHEMA}.dbx_finops_cluster_opportunity_31d_mart",
    "sql_candidates": f"{CATALOG}.{SCHEMA}.dbx_finops_expensive_sql_candidates_31d",
    "serverless": f"{CATALOG}.{SCHEMA}.dbx_finops_serverless_governance_31d_mart",
    "jobs": f"{CATALOG}.{SCHEMA}.dbx_finops_jobs_cost_31d_mart",
}
